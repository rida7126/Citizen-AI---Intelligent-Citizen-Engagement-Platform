# Citizen AI - Intelligent Citizen Engagement Platform

A generative AI web application that enables intelligent citizen-government interactions using IBM Granite AI model for real-time chat assistance, sentiment analysis, and concern management.

## Features

### 🤖 Real-Time Chat Assistant
- Powered by IBM Granite 3.3 2B Instruct model
- 24/7 availability for government service inquiries
- Natural language processing for citizen queries
- Contextual responses about ration cards, pension schemes, licenses, permits, and more

### 📊 Sentiment Analysis
- Real-time sentiment classification (Positive, Negative, Neutral)
- Feedback analysis using advanced NLP
- Helps government understand citizen satisfaction

### 📋 Concern Management
- Citizens can report issues and concerns
- Categorized tracking system
- Priority-based issue management
- Automatic sentiment analysis of reported concerns

### 📈 Admin Dashboard
- Real-time analytics and statistics
- Sentiment distribution visualization
- Concern category analysis
- Interactive charts and graphs
- Recent activity monitoring

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Core programming language
- **Uvicorn** - ASGI server for production

### AI/ML
- **IBM Granite 3.3 2B Instruct** - Core AI model from Hugging Face
- **Transformers** - Hugging Face transformers library
- **PyTorch** - Deep learning framework
- **Accelerate** - Model optimization
- **BitsAndBytes** - Model quantization

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

### Templates
- **Jinja2** - Server-side templating
- **Responsive Design** - Mobile-first approach

## Project Structure

```
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── ai_model.py            # IBM Granite model integration
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication routes
│   │   ├── chat.py            # Chat assistant endpoints
│   │   ├── feedback.py        # Feedback and sentiment analysis
│   │   ├── concern.py         # Concern reporting system
│   │   └── dashboard.py       # Admin dashboard analytics
│   ├── templates/
│   │   ├── base.html          # Base template
│   │   ├── index.html         # Home page
│   │   ├── chat.html          # Chat interface
│   │   ├── feedback.html      # Feedback form
│   │   ├── concern.html       # Concern reporting
│   │   ├── login.html         # Admin login
│   │   └── dashboard.html     # Admin dashboard
│   └── static/
│       ├── css/
│       │   └── style.css      # Custom styles
│       └── js/
│           └── main.js        # JavaScript utilities
├── README.md
└── pyproject.toml             # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- 4GB+ RAM (for AI model)
- Internet connection (for model download)

### 1. Clone/Setup Project
```bash
# Create project directory
mkdir citizen-ai
cd citizen-ai
```

### 2. Install Dependencies
```bash
# Install required Python packages
pip install fastapi uvicorn jinja2 python-multipart
pip install transformers torch accelerate bitsandbytes
pip install safetensors tokenizers huggingface-hub
```

### 3. Create Project Structure
```bash
# Create directories
mkdir -p app/routes app/templates app/static/css app/static/js
```

### 4. Add All Project Files
Copy all the provided Python files, HTML templates, CSS, and JavaScript files to their respective directories.

## Running the Application

### Development Mode
```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Run in production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Access the Application
- **Main Application**: http://localhost:8000
- **Chat Assistant**: http://localhost:8000/chat/
- **Feedback System**: http://localhost:8000/feedback/
- **Report Concerns**: http://localhost:8000/concern/
- **Admin Dashboard**: http://localhost:8000/auth/login

## Usage Guide

### For Citizens

1. **Chat Assistant**
   - Ask questions about government services
   - Get instant AI-powered responses
   - Available 24/7

2. **Provide Feedback**
   - Share experiences with government services
   - Automatic sentiment analysis
   - Help improve services

3. **Report Concerns**
   - Submit issues and problems
   - Track concern status
   - Categorized priority system

### For Administrators

1. **Login Credentials**
   - Username: `admin`
   - Password: `admin123`

2. **Dashboard Features**
   - View total interactions
   - Monitor sentiment trends
   - Analyze concern categories
   - Track recent activity

## API Endpoints

### Chat System
- `POST /chat/ask` - Submit question to AI
- `GET /chat/history` - Get chat history

### Feedback System
- `POST /feedback/submit` - Submit feedback
- `GET /feedback/analyze` - Analyze sentiment

### Concern Management
- `POST /concern/submit` - Report concern
- `GET /concern/list` - List all concerns
- `GET /concern/{id}` - Get specific concern

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/logout` - Logout

### Admin Dashboard
- `GET /dashboard/admin` - Dashboard page
- `GET /dashboard/analytics` - Analytics API

## AI Model Information

### IBM Granite 3.3 2B Instruct
- **Model Size**: 2 billion parameters
- **Capabilities**: Text generation, conversation, sentiment analysis
- **Optimization**: Supports quantization for efficient inference
- **Fallback**: Keyword-based responses when model unavailable

### Model Features
- Government service knowledge
- Sentiment classification
- Contextual understanding
- Multi-turn conversations

## Security Features

- Session-based authentication
- Input validation and sanitization
- CSRF protection
- Secure cookie handling
- Environment-based configuration

## Performance Optimizations

- Model quantization for memory efficiency
- Async request handling
- Static file serving
- Efficient template rendering
- Database connection pooling ready

## Deployment Options

### Local Development
- Run with `uvicorn --reload`
- Debug mode enabled
- Hot reloading

### Production Deployment
- Use production ASGI server
- Enable security features
- Set environment variables
- Configure logging

### Cloud Deployment
- Compatible with IBM Cloud
- Docker containerization ready
- Scalable architecture
- Load balancer compatible

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Troubleshooting

### Model Loading Issues
- Ensure sufficient RAM (4GB+)
- Check internet connection
- Verify Hugging Face access

### Performance Issues
- Enable model quantization
- Reduce max_length parameters
- Use CPU inference for development

### Dependencies
- Update pip: `pip install --upgrade pip`
- Install specific versions if conflicts occur
- Use virtual environment

## Live Demo
- https://citizen-ai.onrender.com/
- "Render Free Tier may show a short 502 during startup. This is expected behavior and resolves automatically."

## License

MIT License - see LICENSE file for details

## Support

For technical support or questions:
- Check troubleshooting section
- Review error logs
- Contact development team

---

**Powered by IBM Granite AI** | **Built with FastAPI & Python**
