# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a FastAPI + Jinja2 + SQLite web application inspired by the supplied
SmartBridge project documentation. It collects user information, generates a
7-day general wellness activity plan with Gemini, generates a short wellness tip,
stores results in SQLite, accepts feedback, and revises the plan.

## Important implementation update

The original document describes the older `google-generativeai` SDK and Gemini 1.5
models. The current Google documentation recommends the `google-genai` SDK and
`from google import genai`. This project therefore uses the current SDK style and
configurable model names. See Google's current Gemini getting-started and generation
documentation for the latest available model names.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_generator.py
│   └── gemini_flash_generator.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── all_users.html
│   └── error.html
├── static/
│   └── css/
│       └── style.css
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup on Windows

1. Install Python 3.11+.
2. Open the `FitBuddy` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create the virtual environment:

```powershell
python -m venv venv
```

5. Activate it:

```powershell
venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

8. Put your Gemini API key in `.env`:

```text
GEMINI_API_KEY=your_real_key_here
```

For a first test, you can leave `DEMO_MODE=true`. The application will run without
a Gemini key and use deterministic demo content.

## Run

```powershell
uvicorn app.main:app --reload
```

Open:

- Home: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Admin/user view: http://127.0.0.1:8000/view-all-users

## Test

With the virtual environment active:

```powershell
pytest
```

## How the application works

1. `index.html` collects name, user ID, age, weight, goal and intensity.
2. `/generate-workout` validates the form.
3. `gemini_generator.py` calls Gemini for the 7-day activity plan.
4. `gemini_flash_generator.py` calls Gemini for a short wellness tip.
5. SQLAlchemy stores the user and generated results in SQLite.
6. `result.html` displays the plan and feedback form.
7. `/submit-feedback` sends the existing plan + feedback to Gemini and stores the revised plan.
8. `/view-all-users` displays stored users and whether their plan was updated.
9. `/docs` exposes FastAPI's interactive API documentation.

## Safety design

This educational implementation deliberately uses adult-only input validation,
low/medium intensity, and general wellness goals. It does not generate calorie
restriction, fasting, supplement prescriptions, weight-loss targets, or extreme
workout instructions. It is not medical advice.

## GitHub

Do not commit `.env` because it contains the API key. The `.gitignore` file already
excludes it.

Basic commands:

```powershell
git init
git add .
git commit -m "Initial FitBuddy project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
