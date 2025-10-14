# 🧠 Smart Task Planner

An **AI-powered planner** that breaks down user goals into actionable tasks, with dependencies and estimated timelines.  
Powered by **FastAPI** and **OpenRouter**, it can be paired with an optional frontend (e.g., React + Vite) for goal submission and task visualization.

---

## 🚀 Features

- 🧠 **AI Task Breakdown** – Converts high-level goals into structured JSON tasks using OpenRouter models.  
- 🗂 **Database Storage** – Saves goals and tasks into a local SQLite database.  
- 🌐 **CORS Enabled** – Works seamlessly with any frontend.  
- ⚡ **FastAPI Backend** – Lightweight, high-performance Python server.  
- 📅 **Dependency Mapping** – Each task can include dependency IDs and estimated durations.  
- 🔄 **Retrieve Past Plans** – List all previously generated plans from the database.  
- 🎨 **Optional Frontend** – React + Vite frontend for submitting goals and viewing tasks.  

---

## 🧰 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic  
- **AI API**: [OpenRouter](https://openrouter.ai)  
- **Frontend** (Optional): React + Vite  
- **Database**: SQLite  
- **Language**: Python 3.10+  

---

## 📝 Prerequisites

Before running the project, make sure you have:

- 🐍 Python 3.10 or higher  
- [Git](https://git-scm.com/downloads)  
- An [OpenRouter API Key](https://openrouter.ai/keys)  

---

## ⚡ Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Add your API key
uvicorn app:app --reload

---

## 📁 Repository Structure

smart-task-planner/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/              
│   ├── index.html
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── api.js
│   ├── package.json
│   └── README.md
│
├── demo/
│   └── demo_video.mp4    
│
            

