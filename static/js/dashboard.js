// /static/js/dashboard.js
async function loadDashboard() {
  try {
    const res = await fetch("/stats");
    const data = await res.json();

    document.getElementById("totalNotes").textContent = data.total_notes;
    document.getElementById("latency").textContent = data.latency_ms;
    document.getElementById("env").textContent = data.environment;
    document.getElementById("errors").textContent = data.error_count;
  } catch (err) {
    console.error("Error fetching dashboard stats:", err);
  }
}

document.addEventListener("DOMContentLoaded", loadDashboard);
