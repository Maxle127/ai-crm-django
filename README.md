# AI CRM
AI CRM is a Django-based CRM system for managing leads, notes, files, and AI-generated follow-up messages.

## Features
- Registration, login and logout
- Create, update and delete leads
- Filter leads
- Notes for leads
- Uploading files
- User profile
- Month activity and stats
- AI-generated follow-up based on lead data and notes

## Tech Stack
- Python
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript
- OpenAI API
- Render

## Project Pages
- Home page
- Dashboard
- Leads list
- Lead detail
- Create lead
- Update lead
- Delete lead
- Profile
- Login
- Register

## Local Setup
### 1. Clone the repository
```bash
git clone https://github.com/Maxle127/ai-crm-django.git
cd ai-crm-django
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
#### Windows
```bash
venv\Scripts\activate
```

#### macOS & Linux
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Create a .env file
Create a .env file in the project root and add:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=your_postgresql_database_url
OPENAI_API_KEY=your_openai_api_key
```

### 6. Apply migrations
```bash
python manage.py migrate
```

### 7. Run the development server
```bash
python manage.py runserver
```

## Live Demo
Live demo: https://ai-crm-django.onrender.com/

## Deployment Notes
The project is deployed on Render and uses Render PostgreSQL as the production database. Because it uses the free plan, the server may need a few seconds to wake up after inactivity.