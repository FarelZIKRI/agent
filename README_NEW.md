# 🤖 Gemini AI Agent

Aplikasi AI Agent yang powerful menggunakan Google Gemini API dengan web interface yang modern dan user-friendly.

## ✨ Fitur Utama

- 🧠 **AI Agent Cerdas**: Menggunakan Google Gemini Pro model
- 💬 **Chat Interface**: Web interface yang responsive dan modern
- 🔄 **Memory Conversation**: Menyimpan riwayat percakapan
- 🎨 **UI/UX Modern**: Design yang clean dan intuitive
- 📱 **Responsive**: Berfungsi di desktop dan mobile
- ⚙️ **Konfigurasi Fleksibel**: Environment-based configuration
- 🔒 **Session Management**: Manajemen sesi yang aman

## 🚀 Quick Start

### 1. Persiapan Environment

```bash
# Clone repository
git clone <repository-url>
cd gemini-ai-agent

# Install dependencies
pip install -r requirements.txt

# Copy dan edit environment variables
cp .env.example .env
```

### 2. Setup Google Gemini API

1. Kunjungi [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Buat API key baru
3. Copy API key ke file `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### 3. Menjalankan Aplikasi

```bash
# Menggunakan script runner (recommended)
python run.py

# Atau langsung dengan Flask
python web_app.py

# Atau menggunakan command line agent
python gemini_agent.py
```

Buka browser dan akses `http://localhost:5000`

## 📁 Struktur Project

```
gemini-ai-agent/
├── gemini_agent.py      # Core AI Agent class
├── web_app.py           # Flask web application
├── run.py               # Application runner
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── templates/
│   └── index.html       # HTML template
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # JavaScript logic
└── README.md
```

## 🔧 Konfigurasi

### Environment Variables

| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `GEMINI_API_KEY` | - | **Required**: Google Gemini API key |
| `GEMINI_MODEL` | `gemini-pro` | Model Gemini yang digunakan |
| `FLASK_ENV` | `development` | Environment Flask |
| `FLASK_DEBUG` | `True` | Mode debug Flask |
| `PORT` | `5000` | Port aplikasi |
| `HOST` | `0.0.0.0` | Host aplikasi |
| `MAX_MESSAGE_LENGTH` | `4000` | Maksimal panjang pesan |
| `MAX_HISTORY_MESSAGES` | `100` | Maksimal history pesan |
| `SESSION_TIMEOUT` | `3600` | Timeout sesi (detik) |

### Konfigurasi Advanced

```python
# config.py
class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
```

## 💻 Penggunaan

### 1. Web Interface

- Akses `http://localhost:5000`
- Mulai chat dengan AI agent
- Gunakan tombol "Clear Chat" untuk reset percakapan
- Klik "Model Info" untuk melihat informasi model

### 2. Command Line Interface

```python
from gemini_agent import GeminiAgent

# Initialize agent
agent = GeminiAgent(api_key="your_api_key")

# Set system prompt
agent.add_system_prompt("Anda adalah assistant yang helpful.")

# Send message
response = agent.send_message("Halo, siapa kamu?")
print(response)

# Save conversation
agent.save_conversation("chat_history.json")
```

### 3. API Endpoints

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/` | GET | Main page |
| `/api/chat` | POST | Send message to AI |
| `/api/history` | GET | Get conversation history |
| `/api/clear` | POST | Clear conversation |
| `/api/model-info` | GET | Get model information |
| `/health` | GET | Health check |

## 🎨 Customization

### Mengubah System Prompt

```python
# web_app.py
agent.add_system_prompt(
    "Anda adalah AI assistant yang sangat helpful dan expert dalam programming. "
    "Jawab dengan detail dan berikan contoh kode jika diperlukan."
)
```

### Styling Custom

Edit `static/css/style.css` untuk mengubah tampilan:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-secondary-color;
}
```

### Menambah Fitur JavaScript

Edit `static/js/app.js` untuk menambah fungsionalitas:

```javascript
class GeminiChatApp {
    // Add your custom methods here
}
```

## 🚀 Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

### Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

### Traditional Server

```bash
# Install dependencies
pip install -r requirements.txt gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## 🔒 Security Best Practices

1. **API Key Security**: Jangan commit API key ke repository
2. **Environment Variables**: Gunakan `.env` file untuk development
3. **HTTPS**: Gunakan HTTPS di production
4. **Rate Limiting**: Implementasi rate limiting untuk API
5. **Input Validation**: Validasi semua input user

## 🐛 Troubleshooting

### Common Issues

**Error: GEMINI_API_KEY not found**
```bash
# Pastikan .env file ada dan berisi API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

**Error: ModuleNotFoundError**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Error: Port already in use**
```bash
# Ganti port di .env
echo "PORT=5001" >> .env
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run.py
```

## 📚 API Documentation

### Send Message

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI!"}'
```

Response:
```json
{
  "response": "Halo! Saya adalah AI assistant...",
  "timestamp": "2024-01-01T12:00:00",
  "session_id": "uuid-here"
}
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) untuk AI model
- [Flask](https://flask.palletsprojects.com/) untuk web framework
- [Font Awesome](https://fontawesome.com/) untuk icons

## 📞 Support

Jika ada pertanyaan atau issue:

1. Check [Issues](../../issues) yang sudah ada
2. Buat issue baru dengan detail yang jelas
3. Sertakan log error dan langkah reproduksi

---

**Happy Coding! 🚀**