# MailMind-AI

**MailMind-AI** is an email automation and classification project I built to streamline how we handle messages. It leverages a collection of specialized AI agents powered by Ollama's llama3.2 model to automatically detect the intent behind emails and JSON inputs, then take appropriate actions.

In practice, MailMind-AI can read incoming emails (for example, about scheduling a product demo), classify their intent, and help automate responses or record-keeping. The goal is to make email management smarter and more efficient using local LLM technology.

---

## 📁 Project Structure

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

## Agents

### classifier_agent.py

This agent uses Ollama's llama3.2 model to read incoming messages (emails or JSON) and classify their type or intent. For instance, it can detect whether an email is a request for information, a demo scheduling request, or something else. In one example dataset, an email with subject "Meeting request – product demo" and body "I'd like to schedule a demo of your enterprise solution…" was automatically labeled as a scheduling intent. The classifier lets the system know how to route the message to the right handler next. This is similar to how businesses use text classification to categorize emails by user intent (e.g., inquiries, complaints, requests).

### email_agent.py

Once the ClassifierAgent tags an email (e.g. as a "Demo Request" or "Scheduling" intent), the EmailAgent processes the email content accordingly. For example, it might extract details like names, dates, or specific requests from the subject and body, then either generate a suggested response or log the request in memory. The EmailAgent essentially knows how to interact with email text – summarizing, answering, or updating records – using the llama3.2 model. In simple terms, if an email says "Can I see a demo of your product?", the EmailAgent could recognize that as a demo scheduling request and prepare a response.

### json_agent.py

This agent handles structured JSON inputs that might come from the frontend or an API call. It can read JSON payloads describing tasks or queries and process them in a similar way to email texts. For example, a JSON object like `{"task": "add_event", "details": {"date": "2025-06-05", "title": "Product Demo"}}` could be interpreted by the JSONAgent to update the system's memory or notify the user. This agent ensures that both free-text and structured inputs are integrated into the workflow.

## Shared Memory

### shared_memory.py

This module manages the application's memory, storing context and past interactions. MailMind-AI uses SQLite to persist data, so conversations or task history aren't lost between sessions. SQLite is a lightweight, self-contained SQL database engine that is small and fast, making it ideal for embedding directly in this app without complex setup. In practice, I use shared memory so that different agents can read and write information consistently – for example, remembering that a demo has been scheduled or that an email was previously answered.

## Core Modules

### main.py

This is the application's entry point. When I run the program, main.py initializes the FastAPI server and sets up all the routes and background tasks. It loads configurations (from .env.example as a guide), instantiates agents, and ties together the backend API with the frontend. Essentially, main.py is what starts the MailMind-AI service.

### api.py

This file defines the FastAPI application and its endpoints (for example, routes to submit an email or JSON to process, or to fetch the current memory). FastAPI is a modern, high-performance web framework for building APIs with Python. I chose FastAPI because it automatically generates interactive API docs and handles requests very efficiently, which is great for handling multiple agent calls in parallel. Each API route in api.py calls the appropriate agent and returns JSON responses that the frontend can display.

## Frontend (Templates and Static Assets)

The frontend is built with simple HTML templates and static assets for a user interface:

### Templates

- **base.html** provides the common layout (like navigation bar and linking CSS/JS) for all pages.
- **dashboard.html** is the main interface where the user can view incoming messages, see classifications, and trigger actions.
- **memory.html** shows the contents of the shared memory (e.g. stored past requests or notes) for transparency.

### Static Files

- **css/styles.css** contains the styles, using Tailwind CSS classes. Tailwind is a utility-first CSS framework that lets me quickly style the app by adding classes in the HTML, without writing custom CSS rules. It makes responsive design and theming much faster.
- **js/main.js** holds client-side JavaScript (for example, code to fetch new data from the API or handle user interactions on the dashboard).

Together, these templates and assets create a simple UI so I can see what MailMind-AI is doing (e.g. a "Memory View" page that shows the stored context) and interact with it.

## Example Workflow

To illustrate how MailMind-AI works in practice, consider a demo request scenario:

A user receives an email saying "Hi, I would like to schedule a demo of your product next Tuesday."  
I feed this email into the system. The ClassifierAgent analyzes the text and tags it as a "demo request" or scheduling intent (this is an example of text classification of an email's purpose).  
Recognizing a demo request, the EmailAgent extracts details (like the requested date) and might generate a suggested reply or add an entry to memory saying "Demo requested on [date]".  
If needed, the Shared Memory (SQLite) logs this as a pending task. Later, another agent or me could review the memory page and see "Demo with [customer] scheduled" and confirm it.

This illustrates how the agents work together: ClassifierAgent identifies what the input is about, and EmailAgent or JSONAgent carries out the appropriate action based on that intent. By automating intent detection (e.g. recognizing a request) and response generation, MailMind-AI helps reduce manual sorting and replying.

## Tech Stack & Design Decisions

### FastAPI

I built the backend with FastAPI because it's fast, modern, and easy to work with. FastAPI's type-based syntax makes the code clean, and it provides interactive API docs out of the box, which is helpful during development. Its performance (on par with Node.js/Go) means the agent calls and web requests happen quickly.

### Ollama with llama3.2

For natural language processing, I use Ollama with the llama3.2 model. This provides several advantages:
- Local processing: All inference happens on your machine, no API calls needed
- Privacy: Data never leaves your system
- Cost-effective: No API costs or usage limits
- Customizable: You can fine-tune the model for specific use cases
- Fast: Local inference means lower latency

The llama3.2 model provides excellent performance for:
- Text classification
- Intent detection
- Response generation
- Content analysis

### SQLite

I chose SQLite for persisting memory because it's a lightweight, serverless database engine. As the SQLite documentation states, it's a "small, fast, self-contained, high-reliability, full-featured, SQL database engine." It requires no separate server and stores everything in a single file, which keeps deployment simple. MailMind-AI uses SQLite to store chat history and any structured data so that nothing is lost when the server restarts.

### Tailwind CSS

For the frontend styling, I used Tailwind CSS. Tailwind's utility-first approach (with classes like flex, text-center, etc.) lets me rapidly build clean, responsive layouts by composing simple classes in the HTML. This makes it easy to prototype and tweak the UI without writing a lot of custom CSS.

## Setup Instructions

1. Install Ollama:
   ```bash
   # Follow instructions at https://ollama.ai/download
   ```

2. Pull the llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Ollama server (if not already running):
   ```bash
   ollama serve
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Overall Design

The architecture is deliberately modular: each agent has a single responsibility (classify input, process email text, handle JSON data, etc.). This makes the code easier to maintain and extend. If I want to add a new kind of input (say, a Slack message) or a new intent category, I can add another agent or expand an existing one. The shared memory and FastAPI glue everything together into a cohesive app. By combining these technologies—modern Python frameworks, local LLM processing, and a simple frontend—I aimed to create a human-friendly, efficient email assistant that can adapt to real-world tasks.

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Tailwind CSS](https://tailwindcss.com/)
- Powered by [Ollama](https://ollama.ai/) with llama3.2 model
