// /static/js/dashboard.js

async function loadDashboard() {
  try {
    const res = await fetch("/stats");
    const data = await res.json();
//    console.log(data);
    document.getElementById("totalNotes").textContent = data.total_notes;
    document.getElementById("latency").textContent = data.latency_ms;
    document.getElementById("env").textContent = data.environment;
//    document.getElementById("version").textContent = data.python_version;
    document.getElementById("errors").textContent = data.error_count;
    document.getElementById("errorType").textContent = data.last_error_type;
    document.getElementById("errorTime").textContent = data.last_error_time;
  } catch (err) {
    console.error("Error fetching dashboard stats:", err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Initial dashboard load
  loadDashboard();

  // Auto-refresh dashboard every 5 seconds
  setInterval(loadDashboard, 5000);
});
