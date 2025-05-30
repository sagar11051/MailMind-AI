# Multi-Agent AI System for Flowbit Internship Assignment

## Objective
Build a multi-agent AI system that accepts PDF, JSON, or Email inputs, classifies format and intent, routes to specialized agents, and maintains shared context for traceability.

## Tech Stack
- Python 3.9+
- OpenAI API (GPT-4) for LLM tasks
- SQLite (or in-memory dict) for lightweight shared memory
- Minimal external dependencies (requests, pdfplumber for PDF parsing, email parser)

## System Architecture

### Agents
1. **Classifier Agent**
   - Input: Raw file/email/JSON
   - Output: Format (PDF/JSON/Email), Intent (Invoice, RFQ, Complaint, etc.)
   - Routes input to JSON Agent or Email Agent accordingly
   - Logs classification results to shared memory

2. **JSON Agent**
   - Input: JSON payload
   - Extracts and reformats data to target schema
   - Flags anomalies or missing fields

3. **Email Agent**
   - Input: Email text content
   - Extracts sender, intent, urgency
   - Formats data for CRM-style usage

### Shared Memory Module
- Stores source metadata (type, timestamp)
- Stores extracted fields and conversation/thread IDs
- Implemented via SQLite or Python in-memory dictionary
- Accessible by all agents for context sharing

## Example Flow
User sends email → Classifier Agent detects "Email + RFQ" → Routes to Email Agent → Extracts info → Logs to shared memory

## File and Folder Structure

```
multi_agent_ai_system/
│
├── README.md # Project overview, setup, usage instructions
├── requirements.txt # Python dependencies
├── sample_inputs/ # Sample input files for testing
│ ├── sample_invoice.pdf
│ ├── sample_request.json
│ └── sample_email.txt
│
├── outputs/ # Logs, extracted data, screenshots for demo
│ └── sample_output.log
│
├── agents/ # Agent modules
│ ├── __init__.py
│ ├── classifier_agent.py # Classifier agent implementation
│ ├── json_agent.py # JSON agent implementation
│ └── email_agent.py # Email agent implementation
│
├── memory/ # Shared memory module
│ ├── __init__.py
│ └── shared_memory.py # SQLite or in-memory context storage
│
├── utils/ # Utility modules
│ ├── __init__.py
│ ├── pdf_parser.py # PDF parsing utilities
│ ├── email_parser.py # Email parsing utilities
│ └── logger.py # Logging utilities
│
└── main.py # Entry point to run the system end-to-end
```

## Setup
1. Clone the repository or copy the folder structure.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
4. Place sample input files in `sample_inputs/`.

## Usage
Run the main script:
```bash
python main.py --input sample_inputs/sample_email.txt
```

## Notes
- Modular agent design for easy testing and debugging.
- Minimal dependencies for fast setup.
- See `outputs/` for logs and extracted data. 