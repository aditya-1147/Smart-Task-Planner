from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from models import Plan, Task
import os, json, re, requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Task Planner")

# Allow frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Config ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "alibaba/tongyi-deepresearch-30b-a3b:free")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Pydantic Model ---
class GoalInput(BaseModel):
    goal: str


# --- Helper: Extract JSON safely from model response ---
def safe_json_extract(text: str):
    """
    Extracts the first valid JSON object or array from the model output using regex.
    This handles cases where the model adds extra text or markdown formatting.
    """
    # Remove markdown code fences if present
    text = re.sub(r"```(json)?", "", text)
    text = text.replace("```", "").strip()

    # Find the first JSON object or array in the text
    match = re.search(r"(\[.*\]|\{.*\})", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object or array found in model output.")

    json_str = match.group(1)
    return json.loads(json_str)


# --- Helper to call OpenRouter ---
def call_openrouter(goal: str):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OpenRouter API Key")

    prompt = f"""
    Break down the following goal into a JSON array of tasks.
    Each task must have:
    - task_id (int)
    - name (string)
    - description (string)
    - dependency_ids (list of ints)
    - estimated_days (int)

    Respond with ONLY valid JSON. No explanations, no markdown.

    Goal: "{goal}"
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",  # required by OpenRouter ToS
        "X-Title": "Smart Task Planner",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful project planning assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"OpenRouter Error: {response.text}")

    data = response.json()

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail=f"Unexpected OpenRouter response format: {data}")

    try:
        tasks = safe_json_extract(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON Parse Error: {str(e)}\n\nRaw response:\n{content}")

    return tasks


# --- API Endpoint: Generate a plan ---
@app.post("/plan")
async def generate_plan(goal_input: GoalInput):
    try:
        tasks_json = call_openrouter(goal_input.goal)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db = SessionLocal()
    try:
        # Save Plan
        plan = Plan(goal_text=goal_input.goal)
        db.add(plan)
        db.commit()
        db.refresh(plan)
        plan_id = plan.id  # ✅ Extract ID before session closes

        # Save Tasks
        for t in tasks_json:
            task = Task(
                plan_id=plan_id,
                name=t["name"],
                description=t.get("description", ""),
                dependency_ids=json.dumps(t.get("dependency_ids", [])),
                estimated_days=t.get("estimated_days", 1)
            )
            db.add(task)
        db.commit()

        total_days = sum(t["estimated_days"] for t in tasks_json)
        return {"plan_id": plan_id, "tasks": tasks_json, "total_days": total_days}

    finally:
        db.close()


# --- API Endpoint: List all plans ---
@app.get("/plans")
async def get_all_plans():
    db = SessionLocal()
    plans = db.query(Plan).all()
    output = [{"id": p.id, "goal": p.goal_text} for p in plans]
    db.close()
    return output
