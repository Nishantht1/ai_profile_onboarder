import json
from langchain_openai  import ChatOpenAI
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from profiles.models import JobSeekerProfile
from profiles.models import Skill
from profiles.models import ProjectHistory
from profiles.models import Certification
from profiles.models import Award
from django.core.mail import send_mail
from django.conf import settings

llm=ChatOpenAI()

required_keys = [
    "personal_details",
    "professional_details",
    "projects",
    "skills",
    "certifications",
    "awards",
]

def parse_resume_with_llm(resume_text):

    prompt = f"""
You are an AI assistant that extracts structured information from resumes.

ROLE:
- You are a highly accurate resume‑parsing engine.
- You convert unstructured resume text into clean, valid JSON.

TASK:
- Read the resume text provided below.
- Extract all relevant information.
- Return ONLY valid JSON that matches the schema exactly.

RULES:
- Do NOT add fields that are not in the schema.
- Do NOT change field names.
- Do NOT include commentary, explanation, or markdown.
- Output ONLY the JSON object.
- If information is missing, return null or an empty list.
- Dates must be strings.
- Lists must contain only strings or objects as defined.
- If multiple projects, certifications, or awards exist,
return all of them in the corresponding array.

STRICT JSON SCHEMA:
{{
    "personal_details": {{
        "first_name": null,
        "last_name": null,
        "surname": null,
        "dob": null,
        "mobile_number": null,
        "email_id": null,
        "aadhar_number": null
    }},
    "professional_details": {{
        "experience_type": null,
        "experience_years": null,
        "current_company": null,
        "role": null,
        "current_city": null,
        "preferred_city": null,
        "experience_summary": null
    }},
    "projects": [
        {{
            "title": null,
            "description": null,
            "duration_from": null,
            "duration_to": null,
            "role": null,
            "activities": null
        }}
    ],
    "skills": [],
    "certifications": [
        {{
            "name": null,
            "issued_by": null,
            "year": null
        }}
    ],
    "awards": [
        {{
            "title": null,
            "description": null,
            "year": null
        }}
    ]
}}

RESUME TEXT:
{resume_text}
"""
    
    response= llm.invoke(prompt)
    json_string= response.content

    try:
        data=json.loads(json_string)
    except json.JSONDecoderError:
        raise ValueError("LLM returned invalid JSON")
    
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    return data

User = get_user_model()

def normalize_dob(dob_str):
    """Convert various DOB formats into YYYY-MM-DD."""
    if not dob_str:
        return None

    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(dob_str, fmt).date()
        except:
            pass

    return None  # fallback if nothing matches

def save_parsed_resume_data(parsed_data):

    # -------------------------
    # 1. Extract personal details
    # -------------------------
    personal = parsed_data.get("personal_details", {})
    email_id = personal.get("email_id")

    if not email_id:
        raise ValueError("Missing email_id in parsed resume data")

    first_name = personal.get("first_name") or ""
    last_name = personal.get("last_name") or ""
    mobile_number = personal.get("mobile_number")
    dob = normalize_dob(personal.get("dob"))
    surname = personal.get("surname")
    aadhar_number = personal.get("aadhar_number")

    prof = parsed_data.get("professional_details") or {}
    if isinstance(prof, list):
        prof = {}

        
    # -------------------------
    # 2. Create or get User
    # -------------------------
    user, created = User.objects.get_or_create(
        username=email_id,
        defaults={
            "email": email_id,
            "first_name": first_name,
            "last_name": last_name,
        }
    )

    raw_password = None

    if created:
        raw_password = get_random_string(12)
        user.set_password(raw_password)
        user.save()

    # -------------------------
    # 3. Create or update JobSeekerProfile
    # -------------------------
    profile, created_profile = JobSeekerProfile.objects.get_or_create(
        user=user,
        defaults={
            "mobile_number": mobile_number,
            "dob": dob,
            "surname": surname,
            "aadhar_number": aadhar_number,
        }
    )

    # Update missing fields if profile already exists
    updated = False

    if mobile_number and not profile.mobile_number:
        profile.mobile_number = mobile_number
        updated = True

    if dob and not profile.dob:
        profile.dob = dob
        updated = True

    if surname and not profile.surname:
        profile.surname = surname
        updated = True

    if aadhar_number and not profile.aadhar_number:
        profile.aadhar_number = aadhar_number
        updated = True

    if updated:
        profile.save()

    if prof.get("experience_type"):
        profile.experience_type = prof["experience_type"]

    if prof.get("experience_years"):
        profile.experience_years = prof["experience_years"]

    if prof.get("current_company"):
        profile.current_company = prof["current_company"]

    if prof.get("role"):
        profile.role = prof["role"]

    if prof.get("current_city"):
        profile.current_city = prof["current_city"]

    if prof.get("preferred_city"):
        profile.preferred_city = prof["preferred_city"]

    if prof.get("experience_summary"):
        profile.experience_summary = prof["experience_summary"]

    profile.save()

    # -------------------------
    # 4. Save Skills
    # -------------------------
     
    skills_list = parsed_data.get("skills") or []

    seen = set()
    for skill in skills_list:
        clean = str(skill).strip()
        if not clean:
            continue
        key = clean.lower()
        if key in seen:
            continue
        seen.add(key)
        Skill.objects.get_or_create(profile=profile, name=clean)

    # -------------------------
    # 5. Save Projects
    # -------------------------
    projects = parsed_data.get("projects", []) or []
    for project in projects:
        title = project.get("title")
        if not title:
            continue
        ProjectHistory.objects.get_or_create(
            profile=profile,
            title=title.strip(),
            defaults={
                "description": project.get("description"),
                "duration_from": project.get("duration_from"),
                "duration_to": project.get("duration_to"),
                "role": project.get("role"),
                "activities": project.get("activities"),
            }
        )

    # -------------------------
    # 6. Save Certifications
    # -------------------------
    certifications = parsed_data.get("certifications", []) or []
    for cert in certifications:
        name = cert.get("name")
        if not name:
            continue
        Certification.objects.get_or_create(
            profile=profile,
            name=name.strip(),
            defaults={
                "issued_by": cert.get("issued_by"),
                "year": cert.get("year"),
            }
        )

    # -------------------------
    # 7. Save Awards
    # -------------------------
    awards = parsed_data.get("awards", []) or []
    for award in awards:
        title = award.get("title")
        if not title:
            continue
        Award.objects.get_or_create(
            profile=profile,
            title=title.strip(),
            defaults={
                "description": award.get("description"),
                "year": award.get("year"),
            }
        )

    return user, raw_password, profile

def send_welcome_email(user, raw_password):
    print("EMAIL CALLED:", user.email, raw_password)   

    if not raw_password:
        return

    if not raw_password:
        return

    subject = "Your Job Seeker Account Details"

    message = f"""
Hello {user.first_name},

Your job seeker profile has been created successfully.

Login details:

Username: {user.email}
Password: {raw_password}

Login here:
http://127.0.0.1:8000/

Please log in and update your profile if needed.

Thank you.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )