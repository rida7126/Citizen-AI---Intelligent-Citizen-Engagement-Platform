# Citizen AI Setup Guide

Complete installation and setup guide for the Citizen AI - Intelligent Citizen Engagement Platform.

## Prerequisites

- Python 3.9 or higher
- 4GB+ RAM (for AI model)
- Git (for cloning repository)
- Internet connection (for downloading models)

## Installation Options

### Option 1: Quick Demo (Recommended for Testing)

Run the simplified demo version without GPU dependencies:

```bash
# 1. Install basic dependencies
pip install fastapi uvicorn jinja2 python-multipart

# 2. Run the demo
python demo_app.py
```

Access at: http://localhost:8000

### Option 2: Full IBM Granite Model Version

For production deployment with the actual IBM Granite AI model:

#### Step 1: Create Virtual Environment
```bash
# Create project directory
mkdir citizen-ai
cd citizen-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
# Install core dependencies
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install jinja2==3.1.2
pip install python-multipart==0.0.6

# Install AI dependencies (requires significant disk space)
pip install transformers==4.36.0
pip install torch==2.1.0
pip install accelerate==0.25.0
pip install bitsandbytes==0.41.3
pip install safetensors==0.4.1
pip install tokenizers==0.15.0
pip install huggingface-hub==0.19.4
```

#### Step 3: Create Project Structure
```bash
# Create directories
mkdir -p app/routes app/templates app/static/css app/static/js
```

#### Step 4: Add Project Files
Copy all the provided files to their respective directories:

**Backend Files:**
- `app/main.py`
- `app/ai_model.py`
- `app/routes/__init__.py`
- `app/routes/auth.py`
- `app/routes/chat.py`
- `app/routes/feedback.py`
- `app/routes/concern.py`
- `app/routes/dashboard.py`

**Frontend Files:**
- `app/templates/base.html`
- `app/templates/index.html`
- `app/templates/chat.html`
- `app/templates/feedback.html`
- `app/templates/concern.html`
- `app/templates/login.html`
- `app/templates/dashboard.html`
- `app/static/css/style.css`
- `app/static/js/main.js`

#### Step 5: Run the Application
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Application URLs

Once running, access these features:

- **Home Page**: http://localhost:8000
- **AI Chat Assistant**: http://localhost:8000/chat/
- **Feedback System**: http://localhost:8000/feedback/
- **Report Concerns**: http://localhost:8000/concern/
- **Admin Dashboard**: http://localhost:8000/auth/login

## Admin Access

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

## API Endpoints

### Chat System
- `POST /chat/ask` - Submit question to AI assistant
- `GET /chat/history` - Retrieve chat history

### Feedback & Sentiment Analysis
- `POST /feedback/submit` - Submit feedback for analysis
- `GET /feedback/analyze?text=` - Analyze text sentiment

### Concern Management
- `POST /concern/submit` - Report new concern
- `GET /concern/list` - List all concerns
- `GET /concern/{id}` - Get specific concern details

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/logout` - Logout user

### Admin Dashboard
- `GET /dashboard/admin` - Dashboard interface
- `GET /dashboard/analytics` - Analytics data API

## Configuration

### Environment Variables (Optional)
```bash
# Create .env file for production
echo "ENVIRONMENT=production" > .env
echo "LOG_LEVEL=info" >> .env
```

### Model Configuration
The IBM Granite model will be automatically downloaded on first run:
- Model: `ibm-granite/granite-3.3-2b-instruct`
- Size: ~2GB download
- Requirements: 4GB+ RAM

## Features Overview

### 1. Real-Time Chat Assistant
- Powered by IBM Granite 3.3 2B Instruct model
- Government service inquiries
- 24/7 availability
- Natural language processing

**Example Questions:**
- "How do I apply for a ration card?"
- "What are the pension schemes available?"
- "How to get a driving license?"
- "How to file income tax returns?"

### 2. Sentiment Analysis
- Automatic classification: Positive, Negative, Neutral
- Real-time feedback processing
- Government service improvement insights

**Test Examples:**
- Positive: "The online portal is excellent and user-friendly!"
- Negative: "The waiting time is terrible and frustrating."
- Neutral: "The process is okay, could be improved."

### 3. Concern Reporting
- Issue categorization
- Priority levels (Low, Medium, High, Critical)
- Status tracking
- Automatic sentiment analysis

**Categories:**
- Infrastructure
- Public Services
- Healthcare
- Education
- Transportation
- Environment
- Safety & Security
- Administrative

### 4. Admin Dashboard
- Real-time statistics
- Sentiment distribution charts
- Concern category analysis
- Recent activity monitoring
- Interactive data visualization

## Troubleshooting

### Common Issues

**1. Model Loading Problems**
```bash
# Error: Model download failed
# Solution: Check internet connection and disk space
```

**2. Memory Issues**
```bash
# Error: Out of memory
# Solution: Reduce model parameters or use CPU inference
```

**3. Port Already in Use**
```bash
# Error: Address already in use
# Solution: Use different port
uvicorn app.main:app --port 8001
```

**4. Missing Dependencies**
```bash
# Error: Module not found
# Solution: Install missing packages
pip install [missing-package]
```

### Performance Optimization

**For Low-Resource Systems:**
1. Use the demo version (`demo_app.py`)
2. Enable model quantization
3. Reduce max_length parameters
4. Use CPU inference

**For Production:**
1. Use GPU acceleration if available
2. Enable model caching
3. Configure proper logging
4. Set up reverse proxy (nginx)

## Deployment

### Local Development
```bash
uvicorn app.main:app --reload
```

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r citizen_ai_requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment
Compatible with:
- IBM Cloud
- AWS
- Google Cloud Platform
- Azure
- Heroku

## Support

For technical issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure sufficient system resources
4. Review error logs for specific issues

New-Item -ItemType Directory -Path "app/routes","app/templates","app/static/css","app/static/js" -Force
# Install basic dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Run the demo application
python demo_app.py

# Create virtual environment
python -m venv citizen_ai_env
source citizen_ai_env/bin/activate  # On Windows: citizen_ai_env\Scripts\activate

# Install all dependencies
pip install -r citizen_ai_requirements.txt

# Create project structure
mkdir -p app/routes app/templates app/static/css app/static/js

# Run the full application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
The platform is designed to be robust and handle various deployment scenarios, from local development to cloud production environments.
