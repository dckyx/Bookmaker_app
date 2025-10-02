# Bookmaker_app 

A Django-based bookmaker web application with a **React** frontend. It includes user accounts, betting events, and odds management. The app is designed for local development and deployment on **Heroku** with PostgreSQL.  

## Tech stack
- **Backend:** Django + Django ORM  
- **Frontend:** React (`frontend/` folder, build served by Django)  
- **Database:** PostgreSQL in production, SQLite locally  
- **Deployment:** Heroku (Procfile, static files, logs, `.env`)  

## Project structure
```
Bookmaker_app/
├─ Bookmaker/        # Django app: models, views, urls, admin
├─ Bookmaker_app/    # Django project config (settings, urls, wsgi/asgi)
├─ frontend/         # React app (npm build → static files)
├─ staticfiles/      # collected static assets
├─ manage.py
├─ requirements.txt
├─ Procfile          # Heroku process definition
└─ .env              # environment variables (not in git)
```

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export DJANGO_SECRET_KEY=your-secret
export DATABASE_URL=sqlite:///db.sqlite3

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
App available at `http://127.0.0.1:8000/`.  

## Frontend build
```bash
cd frontend
npm install
npm run build
```
The build is collected into Django’s static files.  

