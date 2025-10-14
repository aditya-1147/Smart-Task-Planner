import axios from 'axios';

const API_BASE = "http://localhost:8000";

export async function generatePlan(goal) {
  const response = await axios.post(`${API_BASE}/plan`, { goal });
  return response.data;
}

export async function getPlans() {
  const response = await axios.get(`${API_BASE}/plans`);
  return response.data;
}
