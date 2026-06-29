const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");

function fillInput(text) {
  input.value = text;
  input.focus();
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function formatMarkdown(text) {
  let html = text
    .replace(/^### (.*$)/gim, "<h3>$1</h3>")
    .replace(/^## (.*$)/gim,  "<h2>$1</h2>")
    .replace(/^# (.*$)/gim,   "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
    .replace(/^[\*\-] (.*$)/gim, "<li>$1</li>");

  // wrap consecutive <li> into a single <ul>
  html = html.replace(/(<li>.*<\/li>\n?)+/gim, (match) => `<ul>${match}</ul>`);

  // remaining newlines → <br> but not inside tags
  html = html.replace(/\n/g, "<br>");

  // clean up <br> right after block elements
  html = html.replace(/(<\/h[123]>|<\/ul>|<\/li>)<br>/g, "$1");

  return html;
}

function removeWelcome() {
  const w = document.querySelector(".welcome");
  if (w) w.remove();
}

function addMessage(text, type) {
  removeWelcome();

  const row = document.createElement("div");
  row.className = `msg-row ${type}`;

  const label = document.createElement("div");
  label.className = "msg-label";
  label.textContent = type === "user" ? "You" : "FitForge";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = type === "bot" ? formatMarkdown(text) : escapeHtml(text);

  row.appendChild(label);
  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
  removeWelcome();
  const row = document.createElement("div");
  row.className = "msg-row bot";
  row.id = "typing-row";

  const label = document.createElement("div");
  label.className = "msg-label";
  label.textContent = "FitForge";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = '<div class="typing-bubble"><span></span><span></span><span></span></div>';

  row.appendChild(label);
  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById("typing-row");
  if (t) t.remove();
}

async function send() {
  const q = input.value.trim();
  if (!q) return;

  addMessage(q, "user");
  input.value = "";
  sendBtn.disabled = true;
  showTyping();

  try {
    const res = await fetch("/api/v1/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });

    const data = await res.json();
    removeTyping();

    if (!data || !data.answer) throw new Error("Empty response");
    addMessage(data.answer, "bot");

  } catch (err) {
    removeTyping();
    addMessage("⚠️ Something went wrong. Please try again.", "bot");
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") send();
});