🚀 Overview
AI Profile Onboarder is an end‑to‑end automated onboarding system that converts uploaded resumes into structured job‑seeker profiles using Generative AI.
The system extracts text from resumes, parses them using an LLM, creates user accounts, links profiles, and sends automated welcome emails — all without manual intervention.

This project is ideal for recruitment platforms, HR automation tools, and AI‑powered onboarding workflows.

✨ Features
🔍 AI‑Powered Resume Parsing
Extracts text from PDF/DOCX resumes

Uses an LLM to convert raw text → structured JSON

Handles inconsistent resume formats gracefully

👤 Automated User & Profile Creation
Creates new user accounts with generated passwords

Updates existing profiles intelligently

Links parsed resume data to user profiles

📧 Email Notifications
Sends welcome emails with login credentials

Uses Gmail SMTP with App Password authentication

Secure .env‑based configuration

🗂️ Resume Management
Stores uploaded resumes in media/resumes/

Tracks parsing status (pending, completed, failed)

🧱 Clean Django Architecture
Modular service layer (services.py)

Clear separation of concerns

Error‑tolerant pipeline

Easy to extend and maintain

🏗️ Tech Stack
Python 3.x

Django 5.x

LLM Integration (OpenAI / Gemini / custom)

python‑dotenv

Gmail SMTP (App Password)

SQLite (local development)

📂 Project Structure
Code
ai_profile_onboarder/
│
├── ai_profile_onboarder/        # Django project settings
├── accounts/                    # User authentication
├── profiles/                    # Job seeker profiles
├── resumes/                     # Resume upload + parsing pipeline
│   ├── services.py              # Core logic (LLM, user creation)
│   ├── utils.py                 # Resume text extraction
│   ├── views.py                 # Upload + processing flow
│   └── templates/               # HTML templates
│
├── media/                       # Uploaded resumes (ignored in Git)
├── manage.py
├── db.sqlite3                   # Local database (ignored in Git)
└── .env                         # Secrets (ignored in Git)

⚙️ Setup Instructions
1️⃣ Clone the repository
Code
git clone <your-repo-url>
cd ai_profile_onboarder
2️⃣ Create & activate virtual environment
Code
python -m venv ai_on
ai_on\Scripts\activate
3️⃣ Install dependencies
Code
pip install -r requirements.txt
4️⃣ Create .env file
Code
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
SECRET_KEY=your_django_secret_key
5️⃣ Run migrations
Code
python manage.py migrate
6️⃣ Start the server
Code
python manage.py runserver
📧 Email Configuration
This project uses Gmail SMTP with App Passwords.

In settings.py:

python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
🔒 Important: Files Ignored in Git
Your .gitignore should include:

Code
# Environment variables
.env

# Database
db.sqlite3

# Uploaded resumes
media/
media/*

# Python cache
__pycache__/
*.pyc

# VS Code
.vscode/
This ensures no resumes, no personal data, no secrets ever get uploaded to GitHub.

🧪 How the Pipeline Works
User uploads a resume

Text is extracted (PDF/DOCX)

LLM parses text → structured JSON

User + profile are created/updated

Resume is linked to profile

Welcome email is sent (only for new users)

Parsing status is updated

📬 Email Logic
Emails are sent only when a new user is created:

python
if raw_password:
    send_welcome_email(user, raw_password)
Existing users do not receive new passwords.

📘 Future Enhancements
HTML email templates

Admin dashboard for parsed profiles

Multi‑LLM support (OpenAI, Gemini, Claude)

Resume scoring & ranking

ATS‑friendly profile export


🙌 Acknowledgements
Built with Django, LLMs, and a lot of debugging energy.
Special thanks to AI for making resume parsing actually enjoyable.