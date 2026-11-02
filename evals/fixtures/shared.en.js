// Shared component intentionally used in two contexts.
const sharedLabel = "Illustration";
function badge() {
  const span = document.createElement("span");
  span.className = "muted";
  span.textContent = sharedLabel;
  return span;
}
document.querySelector("#shared-preview").append(badge());
document.querySelector("#shared-example").append(badge());
