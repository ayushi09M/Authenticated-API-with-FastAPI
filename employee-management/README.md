# Employee Management Web Service (FastAPI)

## Setup
1. Clone this project.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt


Set environment variables:

export EMP_API_KEY="my-secret"
export GMAIL_USER="your@gmail.com"
export GMAIL_PASS="your-app-password"


Run the service:

uvicorn app.main:app --reload --port 8080