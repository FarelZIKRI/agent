from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from gemini_agent import GeminiAgent
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Store active agents per session
agents = {}

def get_or_create_agent(session_id):
    """Get existing agent or create new one for session"""
    if session_id not in agents:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        agent = GeminiAgent(api_key)
        agent.add_system_prompt(
            "Anda adalah AI assistant yang helpful, harmless, dan honest. "
            "Jawab pertanyaan dengan informatif dan ramah dalam bahasa Indonesia. "
            "Berikan respons yang relevan dan mudah dipahami."
        )
        agents[session_id] = agent
    
    return agents[session_id]

@app.route('/')
def index():
    """Main page"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create agent for this session
        session_id = session.get('session_id')
        if not session_id:
            session['session_id'] = str(uuid.uuid4())
            session_id = session['session_id']
        
        agent = get_or_create_agent(session_id)
        
        # Get response from agent
        response = agent.send_message(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in agents:
            return jsonify({'history': []})
        
        agent = agents[session_id]
        history = agent.get_conversation_history()
        
        return jsonify({'history': history})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in agents:
            agents[session_id].clear_history()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            session['session_id'] = str(uuid.uuid4())
            session_id = session['session_id']
        
        agent = get_or_create_agent(session_id)
        info = agent.get_model_info()
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(agents)
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting Gemini AI Agent Web App on port {port}")
    print(f"🔗 Open http://localhost:{port} in your browser")
    
    app.run(host='0.0.0.0', port=port, debug=debug)