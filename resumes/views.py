
from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .utils import extract_text_from_pdf
from .services import parse_resume_with_llm, save_parsed_resume_data, send_welcome_email

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # 1. Save uploaded resume file
            instance = form.save()

            # 2. Extract text from PDF
            pdf_path = instance.file.path
            extracted_text = extract_text_from_pdf(pdf_path)
            
            # Save extracted text BEFORE LLM call
            instance.parsed_text = extracted_text

            try:
                # 3. Parse using LLM → JSON
                parsed_data = parse_resume_with_llm(extracted_text)
                instance.llm_response = parsed_data

                # 4. Create/update User + Profile + related tables
                user, raw_password, profile = save_parsed_resume_data(parsed_data)
                if raw_password:
                    send_welcome_email(user, raw_password)


                # 5. Link resume to profile
                instance.profile = profile
                instance.parsing_status = "completed"
                instance.save()

            except Exception as e:
                # Any failure → mark as failed
                print("\n\n🔥🔥 ERROR IN PARSING 🔥🔥")
                print(e)
                print("--------------------------------------------------\n\n")
                instance.parsing_status = "failed"
                instance.save()

            return redirect('upload_resume')

    else:
        form = ResumeUploadForm()

    return render(request, 'resumes/upload_resume.html', {'form': form})
