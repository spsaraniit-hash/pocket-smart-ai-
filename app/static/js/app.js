document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("plannerForm");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const status = document.getElementById("status");
    const results = document.getElementById("results");
    const planner = document.getElementById("planner").value;
    const budget = Number(document.getElementById("budget").value);

    let details = {};

    if (planner === "home") {
      details = {
        room_type: document.getElementById("room_type").value,
        style: document.getElementById("style").value,
        important_items: document.getElementById("items").value
      };
    } else if (planner === "party") {
      details = {
        event_type: document.getElementById("event_type").value,
        guests: Number(document.getElementById("guests").value || 0),
        venue: document.getElementById("venue").value
      };
    } else {
      details = {
        occasion: document.getElementById("occasion").value,
        style: document.getElementById("jewelry_style").value
      };

      const file = document.getElementById("outfit").files[0];
      if (file) {
        const formData = new FormData();
        formData.append("file", file);
        try {
          await fetch("/api/jewelry-image", { method: "POST", body: formData });
        } catch (_) {}
      }
    }

    if (!budget || budget <= 0) {
      status.textContent = "Please enter a valid budget.";
      return;
    }

    status.textContent = "Generating your budget plan...";
    results.innerHTML = '<div class="empty-state"><div class="big-icon">⏳</div><h2>Creating recommendations...</h2><p>Please wait.</p></div>';

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ planner, budget, details })
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Request failed");

      renderResults(data);
      status.textContent = data.mode === "gemini"
        ? "Gemini recommendations generated."
        : "Demo/fallback recommendations generated.";
    } catch (error) {
      status.textContent = error.message;
      results.innerHTML = '<div class="empty-state"><div class="big-icon">⚠️</div><h2>Something went wrong</h2><p>Check the terminal for the server error.</p></div>';
    }
  });

  function renderResults(data) {
    const allocation = Object.entries(data.allocation || {})
      .map(([key, value]) => `<div class="summary-box"><span>${escapeHtml(key)}</span><strong>₹${Number(value).toLocaleString("en-IN")}</strong></div>`)
      .join("");

    const recommendations = (data.recommendations || []).map(item => `
      <div class="result-item">
        <div class="meta">${escapeHtml(item.category)} · ${escapeHtml(item.platform)}</div>
        <h3>${escapeHtml(item.suggestion)}</h3>
        <p><strong>${escapeHtml(item.estimated_price)}</strong> — ${escapeHtml(item.reason)}</p>
      </div>
    `).join("");

    const tips = (data.tips || []).map(t => `<li>${escapeHtml(t)}</li>`).join("");

    document.getElementById("results").innerHTML = `
      <h2>Budget plan</h2>
      <p class="meta">Total budget: ₹${Number(data.budget).toLocaleString("en-IN")} · Mode: ${escapeHtml(data.mode)}</p>
      <h3>Suggested allocation</h3>
      <div class="summary">${allocation}</div>
      <h3>Recommendations</h3>
      ${recommendations}
      <div class="tips">
        <strong>Smart tips</strong>
        <ul>${tips}</ul>
      </div>
    `;
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
      "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
    }[char]));
  }
});
