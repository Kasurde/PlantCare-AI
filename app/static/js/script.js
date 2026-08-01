// PlantCare AI — small UI niceties for the upload form.
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector('input[type="file"][name="leaf_image"]');
  const zone = document.querySelector(".upload-zone");
  if (!fileInput || !zone) return;

  const primaryText = zone.querySelector(".primary-text");

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      primaryText.textContent = fileInput.files[0].name;
    }
  });

  ["dragenter", "dragover"].forEach((evt) =>
    zone.addEventListener(evt, (e) => {
      e.preventDefault();
      zone.style.borderColor = "#6B9C4B";
    })
  );

  ["dragleave", "drop"].forEach((evt) =>
    zone.addEventListener(evt, (e) => {
      e.preventDefault();
      zone.style.borderColor = "";
    })
  );

  zone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length > 0) {
      fileInput.files = e.dataTransfer.files;
      primaryText.textContent = e.dataTransfer.files[0].name;
    }
  });
});
