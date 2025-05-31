from fastapi import FastAPI, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from main import process_input
from memory.shared_memory import SharedMemory

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory storage for demo purposes
# In a real app, use a proper database
memory_entries = []

class MemoryEntry(BaseModel):
    key: str
    value: Any
    source: Optional[str] = "system"
    type: Optional[str] = "info"
    timestamp: datetime = datetime.now()

# Add some sample data for demo
if not memory_entries:
    memory_entries.append(MemoryEntry(
        key="system.startup",
        value="System initialized",
        source="system",
        type="info"
    ))

# Root route - redirect to dashboard
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/dashboard")

# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Memory logs route
@app.get("/memory", response_class=HTMLResponse)
async def memory_page(request: Request):
    return templates.TemplateResponse("memory.html", {"request": request})

# API endpoints
@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process the file
    result = process_input(file_path)
    
    # Log to memory
    memory_entry = MemoryEntry(
        key=f"process.file.{file.filename}",
        value={
            "filename": file.filename,
            "content_type": file.content_type,
            "result": result
        },
        source="file_upload",
        type="process"
    )
    memory_entries.append(memory_entry)
    
    return JSONResponse(content=result)

@app.post("/process-json/")
async def process_json_input(json_data: dict):
    import json
    temp_path = os.path.join(UPLOAD_DIR, "temp.json")
    with open(temp_path, "w") as f:
        json.dump(json_data, f)
    
    # Process the JSON
    result = process_input(temp_path)
    
    # Log to memory
    memory_entry = MemoryEntry(
        key=f"process.json.{datetime.now().timestamp()}",
        value={
            "input": json_data,
            "result": result
        },
        source="json_input",
        type="process"
    )
    memory_entries.append(memory_entry)
    
    return JSONResponse(content=result)

class EmailInput(BaseModel):
    subject: str = ""
    body: str

@app.post("/process-email/")
async def process_email_input(email_data: EmailInput):
    try:
        # Process the email
        email_agent = EmailAgent()
        result = email_agent.process_email(email_data.body)
        
        # Extract metadata and content safely
        metadata = result.get('metadata', {})
        content = result.get('content', {})
        
        # Add to recent activities with enhanced metadata
        activity = {
            "type": "email",
            "title": f"Email: {metadata.get('subject', 'No Subject')}",
            "content": content.get('body', email_data.body[:200] + ("..." if len(email_data.body) > 200 else "")),
            "timestamp": metadata.get('received_at', datetime.now().isoformat()),
            "metadata": {
                "sender": metadata.get('sender_name') or metadata.get('sender_email', 'Unknown'),
                "intent": metadata.get('intent', 'Unknown'),
                "urgency": metadata.get('urgency', 'Normal'),
                "suggested_actions": content.get('suggested_actions', [])
            },
            "response_preview": content.get('response', '')[:150] + ('...' if len(content.get('response', '')) > 150 else '')
        }
        
        # Log to memory
        memory_entry = MemoryEntry(
            key=f"process.email.{datetime.now().timestamp()}",
            value=activity,
            source="email_input",
            type="process"
        )
        memory_entries.append(memory_entry)
        
        return {
            "status": "success", 
            "result": result,
            "activity": activity  # Include the activity data in the response
        }
        
    except Exception as e:
        # Log to memory
        memory_entry = MemoryEntry(
            key=f"process.email.{datetime.now().timestamp()}",
            value={
                "error": f"Error processing email: {str(e)}",
                "metadata": {
                    "sender_email": "",
                    "sender_name": "",
                    "subject": "Error Processing Email",
                    "intent": "Error",
                    "urgency": "High",
                    "received_at": datetime.now().isoformat()
                },
                "content": {
                    "body": email_data.body[:500] + ("..." if len(email_data.body) > 500 else ""),
                    "response": "We encountered an error processing your email. Our team has been notified.",
                    "suggested_actions": ["Review manually"]
                }
            },
            source="email_input",
            type="error"
        )
        memory_entries.append(memory_entry)
        
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error": str(e), "result": memory_entry.value}
        )

# Memory API endpoints
@app.get("/api/memory/entries", response_model=List[Dict[str, Any]])
async def get_memory_entries(limit: int = 50):
    """Get recent memory entries"""
    # Return most recent entries first
    entries = sorted(memory_entries, key=lambda x: x.timestamp, reverse=True)[:limit]
    return [entry.dict() for entry in entries]

@app.get("/api/memory/search")
async def search_memory(q: str, limit: int = 10):
    """Search memory entries by key or value"""
    if not q:
        return []
    
    q = q.lower()
    results = []
    
    for entry in reversed(memory_entries):  # Search from newest to oldest
        entry_dict = entry.dict()
        
        # Check if query matches key or value
        if (isinstance(entry_dict['key'], str) and q in entry_dict['key'].lower()) or \
           (isinstance(entry_dict['value'], str) and q in str(entry_dict['value']).lower()) or \
           (isinstance(entry_dict['source'], str) and q in entry_dict['source'].lower()) or \
           (isinstance(entry_dict['type'], str) and q in entry_dict['type'].lower()):
            results.append(entry_dict)
            
            if len(results) >= limit:
                break
    
    return results 