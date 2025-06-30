from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import datetime
import uuid
import os

app = Flask(__name__)
app.secret_key = 'citizen-ai-secret-key-2025'

# In-memory storage
chat_history = []
feedback_data = []
concerns_data = []

def simulate_ai_response(question):
    """Simulate AI responses for government services"""
    responses = {
        "hello": "Hello! I'm your AI assistant for government services. How can I help you today?",
        "hi": "Hi there! I'm here to help you with government services and civic information.",
        "ration": "For ration card applications, you need: 1) Address proof 2) Identity proof 3) Income certificate. You can apply online at your state's food department portal.",
        "pension": "Available pension schemes include: Old Age Pension, Widow Pension, Disability Pension. Eligibility varies by state. Visit your nearest pension office or apply online.",
        "license": "For driving license: 1) Pass learner's test 2) Complete training 3) Pass driving test. Required documents: Age proof, Address proof, Medical certificate.",
        "driving": "For driving license: 1) Pass learner's test 2) Complete training 3) Pass driving test. Required documents: Age proof, Address proof, Medical certificate.",
        "tax": "For income tax filing: 1) Gather Form 16, bank statements 2) Login to income tax e-filing portal 3) Fill ITR form 4) Verify electronically or send signed copy.",
        "permit": "Building permits require: 1) Site plan approval 2) Architectural drawings 3) NOC from fire department 4) Environmental clearance (if needed).",
        "complaint": "To file a complaint: 1) Use our concern reporting system 2) Provide detailed description 3) Upload supporting documents 4) Track status with reference ID.",
        "help": "I can assist with: Ration cards, Pension schemes, Driving licenses, Tax filing, Building permits, Complaint registration, and general government service queries.",
        "ayushman": "Ayushman Bharat provides ₹5 lakh health insurance coverage. Check eligibility at nearest CSC or online portal.",
        "passport": "For passport: 1) Apply online at passportindia.gov.in 2) Book appointment 3) Visit PSK with documents 4) Police verification 5) Receive passport"
    }
    
    question_lower = question.lower()
    
    # Check for keywords in the question
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    # Default response
    return "I understand you're looking for information about government services. Could you please be more specific? I can help with ration cards, pensions, licenses, tax filing, permits, and complaint registration."

def analyze_sentiment(text):
    """Analyze sentiment of text"""
    positive_words = ['good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'love', 'like', 'happy', 'satisfied', 'pleased', 'helpful', 'efficient', 'fast', 'easy']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'frustrated', 'disappointed', 'poor', 'worst', 'useless', 'slow', 'difficult', 'confusing']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"

def is_logged_in():
    """Check if user is logged in"""
    return 'user' in session

def require_login():
    """Redirect to login if not authenticated"""
    if not is_logged_in():
        return redirect(url_for('login', next=request.url))
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    """Services page with all available government services"""
    return render_template('services.html')

@app.route('/chat/')
def chat():
    """Chat page - REQUIRES LOGIN"""
    # Check if user is logged in
    if not is_logged_in():
        flash('Please login to access the Chat Assistant', 'warning')
        return redirect(url_for('login', next=request.url))
    
    return render_template('chat.html', user=session['user'])

@app.route('/chat/ask', methods=['POST'])
def chat_ask():
    """Chat API - COMPLETELY BLOCKED without login"""
    # STRICT LOGIN CHECK - No exceptions!
    if not is_logged_in():
        return jsonify({
            'success': False, 
            'error': 'Authentication required',
            'message': 'You must be logged in to use the chat feature',
            'redirect': url_for('login')
        }), 401
    
    question = request.form.get('question')
    if not question:
        return jsonify({'success': False, 'error': 'No question provided'})
    
    response = simulate_ai_response(question)
    chat_entry = {
        'id': str(uuid.uuid4()),
        'question': question,
        'response': response,
        'timestamp': datetime.datetime.now().isoformat(),
        'user': session.get('user', 'Anonymous')
    }
    chat_history.append(chat_entry)
    
    return jsonify({
        'success': True, 
        'response': response,
        'user': session['user']
    })

@app.route('/feedback/')
def feedback():
    """Feedback page - REQUIRES LOGIN"""
    if not is_logged_in():
        flash('Please login to submit feedback', 'warning')
        return redirect(url_for('login', next=request.url))
    
    return render_template('feedback.html', user=session['user'])

@app.route('/feedback/submit', methods=['POST'])
def feedback_submit():
    """Feedback API - REQUIRES LOGIN"""
    if not is_logged_in():
        return jsonify({
            'success': False, 
            'error': 'Authentication required',
            'message': 'You must be logged in to submit feedback'
        }), 401
    
    feedback_text = request.form.get('feedback_text')
    if feedback_text:
        sentiment = analyze_sentiment(feedback_text)
        feedback_entry = {
            'id': str(uuid.uuid4()),
            'text': feedback_text,
            'sentiment': sentiment,
            'timestamp': datetime.datetime.now().isoformat(),
            'user': session.get('user', 'Anonymous')
        }
        feedback_data.append(feedback_entry)
        return jsonify({
            'success': True, 
            'sentiment': sentiment,
            'message': f'Thank you for your feedback! We analyzed it as {sentiment.lower()} sentiment.'
        })
    return jsonify({'success': False, 'error': 'No feedback provided'})

@app.route('/concern/')
def concern():
    """Concern page - REQUIRES LOGIN"""
    if not is_logged_in():
        flash('Please login to report concerns', 'warning')
        return redirect(url_for('login', next=request.url))
    
    return render_template('concern.html', user=session['user'])

@app.route('/concern/submit', methods=['POST'])
def concern_submit():
    """Concern API - REQUIRES LOGIN"""
    if not is_logged_in():
        return jsonify({
            'success': False, 
            'error': 'Authentication required',
            'message': 'You must be logged in to submit concerns'
        }), 401
    
    title = request.form.get('title')
    category = request.form.get('category')
    priority = request.form.get('priority')
    description = request.form.get('description')
    
    if title and category and priority and description:
        sentiment = analyze_sentiment(description)
        concern_id = f"CON{len(concerns_data) + 1001}"
        concern_entry = {
            'id': concern_id,
            'title': title,
            'category': category,
            'priority': priority,
            'description': description,
            'sentiment': sentiment,
            'status': 'Open',
            'timestamp': datetime.datetime.now().isoformat(),
            'user': session.get('user', 'Anonymous')
        }
        concerns_data.append(concern_entry)
        return jsonify({
            'success': True,
            'concern_id': concern_id,
            'message': 'Your concern has been submitted successfully and will be reviewed by the relevant department.'
        })
    return jsonify({'success': False, 'error': 'Please fill all required fields'})

@app.route('/concern/list')
def concern_list():
    """Concern list - REQUIRES LOGIN"""
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({'concerns': concerns_data})

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Demo users - you can add more here
        users = {
            "admin": "admin123",
            "citizen": "citizen123",
            "user": "password",
            "demo": "demo123"
        }
        
        if username in users and users[username] == password:
            session['user'] = username
            session['login_time'] = datetime.datetime.now().isoformat()
            
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect to the page they were trying to access
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('chat'))  # Default to chat after login
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/auth/logout')
def logout():
    user = session.get('user', 'User')
    session.clear()  # Clear all session data
    flash(f'Goodbye {user}! You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard/')
def dashboard():
    """Dashboard - REQUIRES LOGIN"""
    if not is_logged_in():
        flash('Please login to access the dashboard', 'warning')
        return redirect(url_for('login', next=request.url))
    
    # Calculate statistics
    total_chats = len(chat_history)
    total_feedback = len(feedback_data)
    total_concerns = len(concerns_data)
    
    # Sentiment statistics
    sentiment_stats = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for feedback in feedback_data:
        sentiment_stats[feedback['sentiment']] += 1
    
    # Add demo data if no real data
    if total_feedback == 0:
        sentiment_stats = {'Positive': 60, 'Neutral': 25, 'Negative': 15}
    else:
        # Calculate percentages
        total = sum(sentiment_stats.values())
        for key in sentiment_stats:
            sentiment_stats[key] = round((sentiment_stats[key] / total) * 100) if total > 0 else 0
    
    # Concern categories
    concern_categories = {}
    for concern in concerns_data:
        category = concern['category']
        concern_categories[category] = concern_categories.get(category, 0) + 1
    
    data = {
        'total_chats': total_chats,
        'total_feedback': total_feedback,
        'total_concerns': total_concerns,
        'sentiment_stats': sentiment_stats,
        'concern_categories': concern_categories,
        'recent_feedback': feedback_data[-5:],
        'recent_concerns': concerns_data[-5:]
    }
    
    return render_template('dashboard.html', data=data, user=session['user'])

@app.route('/dashboard/analytics')
def dashboard_analytics():
    """Analytics API - REQUIRES LOGIN"""
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'total_interactions': len(chat_history),
        'weekly_feedback_count': len(feedback_data),
        'concern_categories': {concern['category']: 1 for concern in concerns_data}
    })

# Error handlers for better user experience
@app.errorhandler(401)
def unauthorized(error):
    flash('You need to login to access this feature', 'warning')
    return redirect(url_for('login'))

@app.errorhandler(403)
def forbidden(error):
    flash('Access denied', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting CitizenAI Flask Application...")
    print("🔒 SECURITY: Login Required for ALL interactive features")
    print("📝 Demo Users:")
    print("   - admin / admin123 (Admin access)")
    print("   - citizen / citizen123 (Regular user)")
    print("   - user / password (Regular user)")
    print("   - demo / demo123 (Demo user)")
    print("🌐 Open your browser to: http://localhost:5000")
    print("⚠️  Chat, Feedback, and Concerns are COMPLETELY BLOCKED without login")
    app.run(debug=True, host='0.0.0.0', port=5000)