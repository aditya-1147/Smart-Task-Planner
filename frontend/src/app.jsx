import React, { useState } from "react";
import { generatePlan } from "./api";

export default function App() {
  const [goal, setGoal] = useState("");
  const [tasks, setTasks] = useState([]);

  async function handleSubmit(e) {
    e.preventDefault();
    const data = await generatePlan(goal);
    setTasks(data.tasks);
  }

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Smart Task Planner</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Enter your goal..."
          className="w-full p-2 border rounded"
        ></textarea>
        <button className="bg-blue-600 text-white px-4 py-2 mt-2 rounded">Generate Plan</button>
      </form>

      {tasks.length > 0 && (
        <div>
          <h2 className="font-semibold mb-2">Generated Tasks:</h2>
          <ul>
            {tasks.map((t) => (
              <li key={t.task_id} className="mb-2 border p-2 rounded">
                <strong>{t.name}</strong> – {t.estimated_days} days
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
