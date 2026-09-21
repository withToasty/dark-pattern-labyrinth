(() => {
  "use strict";

  const ACCEPTED_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
  const ACCEPTED_EXTENSIONS = /\.(jpe?g|png|webp)$/i;

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const previewArea = document.getElementById("preview-area");
  const previewImage = document.getElementById("preview-image");
  const previewFilename = document.getElementById("preview-filename");
  const changeFileButton = document.getElementById("change-file-button");
  const analyzeButton = document.getElementById("analyze-button");
  const statusMessage = document.getElementById("status-message");
  const errorMessage = document.getElementById("error-message");

  const resultSection = document.getElementById("result-section");
  const warningsBox = document.getElementById("warnings-box");
  const originalImage = document.getElementById("original-image");
  const annotatedImage = document.getElementById("annotated-image");
  const detectionsBody = document.getElementById("detections-body");
  const noDetectionsMessage = document.getElementById("no-detections-message");
  const horizonSection = document.getElementById("horizon-section");
  const horizonSummary = document.getElementById("horizon-summary");
  const fenceMaskSection = document.getElementById("fence-mask-section");
  const fenceMaskImage = document.getElementById("fence-mask-image");
  const toggleFenceMaskButton = document.getElementById("toggle-fence-mask");
  const jsonOutput = document.getElementById("json-output");
  const yamlOutput = document.getElementById("yaml-output");
  const jsonCode = document.getElementById("json-code");
  const yamlCode = document.getElementById("yaml-code");
  const tabButtons = Array.from(document.querySelectorAll(".tab-button"));
  const copyButton = document.getElementById("copy-button");
  const downloadLink = document.getElementById("download-link");

  let selectedFile = null;
  let analyzing = false;
  let lastResponse = null;
  let activeTab = "json";

  function isAcceptedFile(file) {
    if (!file) return false;
    if (ACCEPTED_TYPES.has(file.type)) return true;
    return ACCEPTED_EXTENSIONS.test(file.name || "");
  }

  function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = !message;
  }

  function setSelectedFile(file) {
    if (!file) return;
    if (!isAcceptedFile(file)) {
      showError("Unsupported file type. Please choose a JPG, PNG, or WEBP image.");
      return;
    }
    showError("");
    selectedFile = file;
    previewImage.src = URL.createObjectURL(file);
    previewFilename.textContent = file.name;
    previewArea.hidden = false;
    analyzeButton.disabled = analyzing;
  }

  dropzone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropzone.classList.remove("dragover");
    const file = event.dataTransfer.files && event.dataTransfer.files[0];
    setSelectedFile(file);
  });

  fileInput.addEventListener("change", () => {
    setSelectedFile(fileInput.files && fileInput.files[0]);
  });

  changeFileButton.addEventListener("click", () => {
    fileInput.value = "";
    fileInput.click();
  });

  function formatNumber(value, digits) {
    if (value === null || value === undefined) return "—";
    return Number(value).toFixed(digits);
  }

  function renderDetections(detections) {
    detectionsBody.innerHTML = "";
    if (!detections || detections.length === 0) {
      noDetectionsMessage.hidden = false;
      return;
    }
    noDetectionsMessage.hidden = true;
    for (const det of detections) {
      const row = document.createElement("tr");
      const group = det.group === undefined || det.group === null || det.group === "" ? "—" : det.group;
      const cells = [det.id, det.label, group, formatNumber(det.confidence, 4), det.minx, det.miny, det.maxx, det.maxy];
      for (const value of cells) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
      }
      detectionsBody.appendChild(row);
    }
  }

  function addSummaryEntry(term, value) {
    const wrapper = document.createElement("div");
    const dt = document.createElement("dt");
    dt.textContent = term;
    const dd = document.createElement("dd");
    dd.textContent = value;
    wrapper.appendChild(dt);
    wrapper.appendChild(dd);
    horizonSummary.appendChild(wrapper);
  }

  function renderHorizon(horizon) {
    horizonSummary.innerHTML = "";
    if (!horizon) {
      horizonSection.hidden = true;
      return;
    }
    horizonSection.hidden = false;

    addSummaryEntry("Detected", horizon.detected ? "yes" : "no");
    addSummaryEntry("Confidence", formatNumber(horizon.confidence, 3));
    addSummaryEntry("Reference score", formatNumber(horizon.reference_score, 3));
    if (horizon.rejection_reason) {
      addSummaryEntry("Rejection reason", horizon.rejection_reason);
    }
    const rectified = horizon.rectified;
    if (rectified) {
      addSummaryEntry("Center Y (normalized)", formatNumber(rectified.center_y_normalized, 4));
      addSummaryEntry("Angle (deg)", formatNumber(rectified.angle_deg, 2));
    }
  }

  function updateOutputTab() {
    const isJson = activeTab === "json";
    jsonOutput.hidden = !isJson;
    yamlOutput.hidden = isJson;
    for (const button of tabButtons) {
      const active = button.dataset.tab === activeTab;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
    }
    if (lastResponse) {
      const asset = isJson ? lastResponse.assets.json : lastResponse.assets.yaml;
      downloadLink.href = asset;
      downloadLink.setAttribute("download", isJson ? "detections.json" : "detections.yaml");
    }
  }

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeTab = button.dataset.tab;
      updateOutputTab();
    });
  });

  copyButton.addEventListener("click", async () => {
    if (!lastResponse) return;
    const text = activeTab === "json" ? lastResponse.json_text : lastResponse.yaml_text;
    try {
      await navigator.clipboard.writeText(text);
      const original = copyButton.textContent;
      copyButton.textContent = "Copied";
      setTimeout(() => {
        copyButton.textContent = original;
      }, 1200);
    } catch (err) {
      showError("Could not copy to clipboard.");
    }
  });

  toggleFenceMaskButton.addEventListener("click", () => {
    const expanded = toggleFenceMaskButton.getAttribute("aria-expanded") === "true";
    const next = !expanded;
    toggleFenceMaskButton.setAttribute("aria-expanded", String(next));
    toggleFenceMaskButton.textContent = next ? "Hide fence mask" : "Show fence mask";
    fenceMaskImage.hidden = !next;
    if (next && !fenceMaskImage.src && lastResponse && lastResponse.assets.fence_mask) {
      fenceMaskImage.src = lastResponse.assets.fence_mask;
    }
  });

  function renderResult(data) {
    lastResponse = data;

    if (data.warnings && data.warnings.length > 0) {
      warningsBox.innerHTML = "";
      const title = document.createElement("strong");
      title.textContent = "Warnings";
      const list = document.createElement("ul");
      for (const warning of data.warnings) {
        const item = document.createElement("li");
        item.textContent = warning;
        list.appendChild(item);
      }
      warningsBox.appendChild(title);
      warningsBox.appendChild(list);
      warningsBox.hidden = false;
    } else {
      warningsBox.hidden = true;
    }

    originalImage.src = data.assets.original;
    annotatedImage.src = data.assets.annotated;

    renderDetections(data.result.detections);

    const horizon = data.result.scene_geometry && data.result.scene_geometry.horizon;
    renderHorizon(horizon || null);

    if (data.assets.fence_mask) {
      fenceMaskSection.hidden = false;
      fenceMaskImage.hidden = true;
      fenceMaskImage.removeAttribute("src");
      toggleFenceMaskButton.setAttribute("aria-expanded", "false");
      toggleFenceMaskButton.textContent = "Show fence mask";
    } else {
      fenceMaskSection.hidden = true;
    }

    jsonCode.textContent = data.json_text;
    yamlCode.textContent = data.yaml_text;
    activeTab = "json";
    updateOutputTab();

    resultSection.hidden = false;
  }

  async function analyze() {
    if (!selectedFile || analyzing) return;
    analyzing = true;
    analyzeButton.disabled = true;
    statusMessage.textContent = "Analyzing…";
    showError("");

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("/api/analyze", { method: "POST", body: formData });
      let data;
      try {
        data = await response.json();
      } catch (parseError) {
        data = null;
      }
      if (!response.ok) {
        const detail = (data && data.detail) || "Analysis failed. Please try again.";
        showError(detail);
        return;
      }
      renderResult(data);
    } catch (err) {
      showError("Could not reach the server. Please try again.");
    } finally {
      analyzing = false;
      analyzeButton.disabled = !selectedFile;
      statusMessage.textContent = "";
    }
  }

  analyzeButton.addEventListener("click", analyze);
})();
