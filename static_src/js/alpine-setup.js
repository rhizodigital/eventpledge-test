import Alpine from "alpinejs";

window.Alpine = Alpine;

// 🔁 Re-initialise Alpine after any htmx content swap
document.addEventListener("htmx:afterSwap", (event) => {
  // Re-scan the swapped-in content for Alpine components
  Alpine.flushAndStopDeferringMutations();
  Alpine.initTree(event.target);
});

Alpine.start();
