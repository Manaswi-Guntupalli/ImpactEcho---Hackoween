/* ImpactEcho Dashboard — fully dynamic from backend */

const user = { username: "Manaswi G" };
const livesPer25 = 25;

/* --- DOM References --- */
const usernameBanner = document.getElementById("username-banner");
const welcomeInline = document.getElementById("welcomeInline");
const usernameInput = document.getElementById("usernameInput");
const causesGrid = document.getElementById("causesGrid");
const totalImpactEl = document.getElementById("totalImpact");
const donationsMadeEl = document.getElementById("donationsMade");
const causesSupportedEl = document.getElementById("causesSupported");
const livesImpactedEl = document.getElementById("livesImpacted");
const impactProgressBar = document.getElementById("impactProgressBar");
const impactPercent = document.getElementById("impactPercent");
const recentList = document.getElementById("recentList");

/* --- State --- */
let causes = [];
let totalImpact = 0;
let donationsMade = 0;
let livesImpacted = 0;
const supportedCauses = new Set();
const recentDonations = [];

/* --- Helper Functions --- */
const formatINR = (num) => "₹" + Number(num).toLocaleString();

/* --- Username Logic --- */
function renderUsername() {
  usernameBanner.textContent = user.username;
  welcomeInline.textContent = user.username;
  usernameInput.value = user.username;
}
usernameInput.addEventListener("input", (e) => {
  user.username = e.target.value || "anonymous";
  renderUsername();
});

/* --- Fetch Causes from Backend --- */
async function fetchCauses() {
  try {
    const res = await fetch("/causes");
    const data = await res.json();
    causes = data;
    renderCauses();
    updateStats();
  } catch (err) {
    console.error("Error fetching causes:", err);
    causesGrid.innerHTML = "<p class='muted'>Unable to load causes at the moment.</p>";
  }
}

/* --- Render Causes --- */
function renderCauses() {
  causesGrid.innerHTML = "";
  causes.forEach((cause) => {
    const percent = Math.min((cause.raised / cause.goal) * 100, 100).toFixed(1);
    const card = document.createElement("div");
    card.className = "cause-card card";
    card.innerHTML = `
      <img src="${cause.image}" alt="${cause.title}" class="cause-img">
      <h3>${cause.title}</h3>
      <p>${cause.description}</p>
      <div class="progress-wrap-small">
        <div class="progress-small-fill" style="width:${percent}%;"></div>
      </div>
      <p class="muted small">${formatINR(cause.raised)} raised of ${formatINR(cause.goal)}</p>
      <button class="fund-btn" data-id="${cause.id}">Fund Cause</button>
    `;
    causesGrid.appendChild(card);
  });

  document.querySelectorAll(".fund-btn").forEach((btn) => {
    btn.addEventListener("click", handleFundClick);
  });

  causesSupportedEl.textContent = supportedCauses.size;
}

/* --- Handle Funding --- */
function handleFundClick(e) {
  const id = Number(e.target.getAttribute("data-id"));
  const cause = causes.find((c) => c.id === id);
  const amount = Number(prompt(`Enter amount to fund "${cause.title}" (in ₹):`));

  if (!amount || isNaN(amount) || amount <= 0) return;

  // Update locally
  cause.raised += amount;
  totalImpact += amount;
  donationsMade++;
  livesImpacted += Math.floor(amount / livesPer25);
  supportedCauses.add(cause.title);

  // Update UI immediately
  renderCauses();
  updateStats();
  addRecentDonation(cause.title, amount);

  // Optional: send update to backend (if you implement it)
  // fetch(`/fund/${id}`, { method: 'POST', body: JSON.stringify({ amount }), headers: { 'Content-Type': 'application/json' } });
}

/* --- Stats Update --- */
function updateStats() {
  totalImpactEl.textContent = formatINR(totalImpact);
  donationsMadeEl.textContent = donationsMade;
  livesImpactedEl.textContent = livesImpacted;
  causesSupportedEl.textContent = supportedCauses.size;

  const avgProgress =
    causes.reduce((sum, c) => sum + (c.raised / c.goal) * 100, 0) / causes.length || 0;
  const percent = Math.min(avgProgress, 100).toFixed(1);
  impactProgressBar.style.width = `${percent}%`;
  impactPercent.textContent = `${percent}%`;
}

/* --- Recent Donations --- */
function addRecentDonation(title, amount) {
  const li = document.createElement("li");
  li.textContent = `Funded ${formatINR(amount)} to "${title}"`;
  recentList.prepend(li);

  if (recentList.children.length > 6) {
    recentList.removeChild(recentList.lastChild);
  }
}

/* --- Initialize --- */
function init() {
  renderUsername();
  fetchCauses();
}

document.addEventListener("DOMContentLoaded", init);

