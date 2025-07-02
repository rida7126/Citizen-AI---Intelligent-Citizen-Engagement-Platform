# Citizen AI - Complete Deployment Guide

## Prerequisites

- **Python 3.9+** (Required)
- **4GB+ RAM** (For AI model)
- **10GB+ Storage** (For model files)
- **Internet connection** (For downloading IBM Granite model)

## Quick Start (Recommended)

### Option 1: Demo Version (No GPU Required)
```bash
# Install basic dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Run demo application
python demo_app.py
```
Access at: http://localhost:8000

### Option 2: Full IBM Granite Model

## Step-by-Step Installation

### 1. Environment Setup

#### Create Virtual Environment
```bash
# Windows
python -m venv citizen_ai_env
citizen_ai_env\Scripts\activate

# macOS/Linux
python3 -m venv citizen_ai_env
source citizen_ai_env/bin/activate
```

#### Install Dependencies
```bash
# Core FastAPI dependencies
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install jinja2==3.1.2
pip install python-multipart==0.0.6

# AI Model dependencies (Large downloads)
pip install transformers==4.36.0
pip install torch==2.1.0
pip install accelerate==0.25.0
pip install bitsandbytes==0.41.3
pip install safetensors==0.4.1
pip install tokenizers==0.15.0
pip install huggingface-hub==0.19.4
```

### 2. Project Structure Setup

Create the following directory structure:
```
citizen-ai/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ai_model.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── feedback.py
│   │   ├── concern.py
│   │   └── dashboard.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── chat.html
│   │   ├── feedback.html
│   │   ├── concern.html
│   │   ├── login.html
│   │   └── dashboard.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── demo_app.py
└── requirements.txt
```

### 3. File Creation

#### Create requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
transformers==4.36.0
torch==2.1.0
accelerate==0.25.0
bitsandbytes==0.41.3
safetensors==0.4.1
tokenizers==0.15.0
huggingface-hub==0.19.4
```

#### Install from requirements
```bash
pip install -r requirements.txt
```

### 4. Running the Application

#### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Application Features

### 1. AI Chat Assistant
- **URL**: http://localhost:8000/chat/
- **Model**: IBM Granite 3.3 2B Instruct
- **Capabilities**: Government service inquiries, step-by-step procedures

**Example Questions:**
- "How do I apply for an Aadhaar card?"
- "What are the pension schemes available?"
- "How to get a driving license?"
- "Process for income tax filing?"

### 2. Sentiment Analysis
- **URL**: http://localhost:8000/feedback/
- **Accuracy**: Enhanced keyword-based analysis with IBM Granite
- **Classifications**: Positive, Negative, Neutral

**Test Cases:**
- Positive: "Excellent service, very satisfied with the portal"
- Negative: "Terrible experience, very disappointed with the process"
- Neutral: "How do I check my application status?"

### 3. Concern Management
- **URL**: http://localhost:8000/concern/
- **Categories**: Infrastructure, Public Services, Healthcare, Education
- **Features**: Automatic sentiment analysis, priority classification

### 4. Admin Dashboard
- **URL**: http://localhost:8000/auth/login
- **Credentials**: admin / admin123
- **Features**: Real-time analytics, sentiment distribution, category statistics

## Model Configuration

### IBM Granite Model Details
- **Model**: ibm-granite/granite-3.3-2b-instruct
- **Size**: ~2GB download
- **Hardware**: Works on CPU and GPU
- **Memory**: 4GB+ RAM recommended

### First Run Model Download
The model downloads automatically on first startup:
```
Loading IBM Granite model...
tokenizer_config.json: 100%|███████| 9.93k/9.93k
vocab.json: 100%|███████████████| 777k/777k
merges.txt: 100%|███████████████| 442k/442k
tokenizer.json: 100%|█████████████| 3.48M/3.48M
Model loaded successfully!
```

## Deployment Options

### Local Development
```bash
uvicorn app.main:app --reload
```

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t citizen-ai .
docker run -p 8000:8000 citizen-ai
```

### Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create citizen-ai-app
git push heroku main
```

#### AWS EC2
```bash
# Launch EC2 instance (t3.medium recommended)
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# Run with screen for persistence
screen -S citizen-ai
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Google Cloud Platform
```bash
# Create app.yaml
echo "runtime: python39" > app.yaml
echo "entrypoint: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" >> app.yaml

# Deploy
gcloud app deploy
```

## Performance Optimization

### For Low-Resource Systems
- Use demo version (`demo_app.py`)
- Enable model quantization
- Reduce max_length parameters
- Use CPU inference

### For Production
- Enable GPU acceleration if available
- Configure proper logging
- Set up reverse proxy (nginx)
- Enable model caching

## Monitoring and Logs

### Application Logs
```bash
# View logs in real-time
uvicorn app.main:app --log-level info

# Save logs to file
uvicorn app.main:app --log-file app.log
```

### Health Check Endpoint
```bash
curl http://localhost:8000/
```

### Model Performance Monitoring
- Response time tracking
- Memory usage monitoring
- Error rate analysis

## Troubleshooting

### Common Issues

#### 1. Model Loading Errors
```
Error: CUDA out of memory
Solution: Use CPU inference or reduce batch size
```

#### 2. Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
uvicorn app.main:app --port 8001
```

#### 3. Missing Dependencies
```bash
# Install missing packages
pip install [package-name]

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

#### 4. Model Download Issues
```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface/
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('ibm-granite/granite-3.3-2b-instruct')"
```

### Performance Issues

#### Slow Response Times
- Check system memory usage
- Monitor CPU utilization
- Consider GPU acceleration
- Reduce model parameters

#### High Memory Usage
- Enable model quantization
- Use smaller batch sizes
- Clear model cache periodically

## Security Considerations

### Authentication
- Change default admin credentials
- Implement proper session management
- Add rate limiting

### Data Protection
- Enable HTTPS in production
- Secure API endpoints
- Implement input validation

### Environment Variables
```bash
# Create .env file
export ENVIRONMENT=production
export LOG_LEVEL=info
export ADMIN_USERNAME=your_admin
export ADMIN_PASSWORD=secure_password
```

## Maintenance

### Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update model cache
rm -rf ~/.cache/huggingface/transformers/
```

### Backup Strategy
- Regular database backups (if using persistent storage)
- Configuration file backups
- Model checkpoint backups

### Monitoring Scripts
```bash
#!/bin/bash
# health_check.sh
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ $response != "200" ]; then
    echo "Application is down, restarting..."
    systemctl restart citizen-ai
fi
```

## Testing

### Unit Tests
```bash
# Install testing dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load tests
locust -f load_test.py --host http://localhost:8000
```

### API Testing
```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/chat/ask" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "question=How to apply for ration card?"

# Test sentiment analysis
curl -X POST "http://localhost:8000/feedback/submit" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "feedback_text=Excellent service, very satisfied!"
```

## Support and Documentation

### API Documentation
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

### Error Codes
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 500: Internal Server Error

### Contact Information
For technical support and issues:
- Check application logs first
- Verify all dependencies are installed
- Ensure sufficient system resources
- Review error messages for specific guidance

Your Citizen AI platform is now ready for deployment with comprehensive IBM Granite model integration, accurate sentiment analysis, and detailed government service information!