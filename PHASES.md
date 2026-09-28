# SmartBridge Phase/Activity Mapping

This implementation maps the supplied documentation to a working project.

## Milestone 1 – Model Selection and Architecture
- Activity 1.1: Gemini is used as the generative AI layer.
- Activity 1.2: Frontend → FastAPI routes → Gemini service → SQLAlchemy/SQLite.
- Activity 1.3: Python virtual environment + requirements.txt.

## Milestone 2 – Core Functionality
- Activity 2.1: Workout generation, nutrition/recovery tip, feedback update.
- Activity 2.2: FastAPI routing, form validation, Pydantic schemas.

## Milestone 3 – routes.py
- `/`
- `/generate-workout`
- `/submit-feedback`
- `/view-all-users`
- `/api/users`
- `/api/users/{user_id}`

## Milestone 4 – Frontend
- Jinja2 templates.
- Responsive CSS.
- Dynamic display of generated and updated plans.

## Milestone 5 – Deployment
- Local Uvicorn server.
- `.env` configuration.
- SQLite persistence.
- Automated smoke tests.
