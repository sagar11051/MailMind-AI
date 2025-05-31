# MailMind AI

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/sagar11051/MailMind-AI?style=social)](https://github.com/sagar11051/MailMind-AI/stargazers)

MailMind AI is an intelligent email processing system that leverages multi-agent AI architecture to classify, analyze, and respond to emails automatically. The system can understand email content, detect intent, suggest responses, and provide actionable insights.

## 🌟 Features

- **Smart Email Classification**: Automatically categorizes emails using machine learning
- **Intent Detection**: Identifies the purpose of the email (e.g., inquiry, support, demo request)
- **Automated Responses**: Generates context-aware suggested responses
- **Priority Handling**: Automatically detects and flags urgent emails
- **Interactive Dashboard**: User-friendly web interface for managing emails
- **Multi-Agent Architecture**: Specialized AI agents for different processing tasks
- **Extensible Design**: Easy to add new processing modules and agents

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, FastAPI
- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **AI/ML**: Hugging Face Transformers, scikit-learn
- **Database**: SQLite (for memory and logging)
- **Deployment**: Uvicorn ASGI server
- **Dependencies**: See `requirements.txt` for full list

## 🏗️ System Architecture

### 🤖 Agents

1. **Classifier Agent**
   - **Input**: Raw file/email/JSON
   - **Output**: Format (PDF/JSON/Email), Intent (Invoice, RFQ, Complaint, etc.)
   - Uses Hugging Face Transformers for intelligent classification
   - Routes input to appropriate specialized agents
   - Maintains classification history in shared memory

2. **Email Agent**
   - **Input**: Email text content
   - Extracts sender, subject, and body content
   - Detects intent (e.g., inquiry, support, demo request)
   - Determines email urgency and priority
   - Generates suggested responses
   - Provides actionable insights and next steps

3. **JSON Agent**
   - **Input**: JSON payload
   - Validates and parses JSON structure
   - Extracts and reformats data to target schema
   - Flags anomalies or missing fields
   - Processes structured data for further analysis

### 🧠 Shared Memory Module
- Centralized storage for agent communications
- Tracks conversation history and context
- Implements caching for improved performance
- Supports both transient and persistent storage modes
- Provides thread-safe access to shared resources

## Example Flow
User sends email → Classifier Agent detects "Email + RFQ" → Routes to Email Agent → Extracts info → Logs to shared memory

## 📁 File and Folder Structure

```
MailMind-AI/
├── agents/                  # AI agent implementations
│   ├── __init__.py
│   ├── classifier_agent.py  # Classifies input types
│   ├── email_agent.py       # Processes email content
│   └── json_agent.py        # Handles JSON data
│
├── static/                 # Frontend static files
│   ├── css/                # Stylesheets
│   │   └── styles.css
│   └── js/                 # JavaScript files
│       └── main.js
│
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── dashboard.html     # Main dashboard
│   └── memory.html        # Memory view
│
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
├── api.py                # FastAPI application
├── main.py               # Application entry point
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sagar11051/MailMind-AI.git
   cd MailMind-AI
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following content:
   ```
   HUGGINGFACE_TOKEN=your_huggingface_token_here
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

5. **Run the application**
   ```bash
   uvicorn api:app --reload
   ```

6. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8000/dashboard`

## 📚 API Documentation

### Endpoints

- `POST /process-email/` - Process an email
  - Request body: `{"subject": "Email subject", "body": "Email content"}`
  - Response: Processed email data with analysis and suggestions

- `GET /memory` - View system memory entries
- `GET /api/memory/entries` - API endpoint for memory entries

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Tailwind CSS](https://tailwindcss.com/)
- Uses [Hugging Face Transformers](https://huggingface.co/transformers/) for NLP tasks

## 📬 Contact

For any questions or feedback, please open an issue or contact the maintainers.

---

<div align="center">
  Made with ❤️ by the MailMind AI Team
</div> 