// ─── Modal helpers ─────────────────────────────────────────────────────────
function openModal() {
  document.getElementById("modal-overlay").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden");
  document.getElementById("modal-body").innerHTML = "";
}

// Close on overlay click
document.getElementById("modal-overlay").addEventListener("click", function(e) {
  if (e.target === this) closeModal();
});

// Close on Escape
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") closeModal();
});
