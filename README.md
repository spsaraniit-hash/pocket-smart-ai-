# PocketSmart AI: Your Smart Budget & Recommendation Assistant

A full-stack GenAI budget planning project using:
- FastAPI
- Jinja2
- HTML/CSS/JavaScript
- Google Gemini API
- Python
- Optional image upload for jewelry planning

## Features
1. Home Interior Planner
2. Party Budget Planner
3. Jewelry Recommendation Planner
4. Gemini-powered recommendations
5. Budget allocation
6. Responsive UI
7. Demo mode when no Gemini API key is configured
8. Health-check API endpoint

## Project Structure

```text
PocketSmart_AI/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── gemini_service.py
│   ├── schemas.py
│   ├── utils.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── planner.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── uploads/.gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

## 1. Create environment

Windows:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

Never upload your `.env` file to GitHub.

## 3. Run

```bat
python run.py
```

Open:
```text
http://127.0.0.1:8000
```

API health:
```text
http://127.0.0.1:8000/api/health
```

## 4. Demo mode

If `GEMINI_API_KEY` is empty, the application still runs using built-in demo recommendations. This is useful for UI testing.

## 5. GitHub

```bat
git init
git add .
git commit -m "Initial PocketSmart AI project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Important

Product/vendor names such as Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO are shown as example platforms in the generated recommendation text. This project does not scrape or impersonate those platforms.
