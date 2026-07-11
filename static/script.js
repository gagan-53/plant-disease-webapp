const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const previewImg = document.getElementById('previewImg');
const resultArea = document.getElementById('resultArea');
const loader = document.getElementById('loader');
const errorBox = document.getElementById('errorBox');
const resetBtn = document.getElementById('resetBtn');

const topPlant = document.getElementById('topPlant');
const topCondition = document.getElementById('topCondition');
const topConfidence = document.getElementById('topConfidence');
const topConfidenceBar = document.getElementById('topConfidenceBar');
const topDescription = document.getElementById('topDescription');
const topTreatment = document.getElementById('topTreatment');
const treatmentBlock = document.getElementById('treatmentBlock');
const topkList = document.getElementById('topkList');
const latency = document.getElementById('latency');
const classesGrid = document.getElementById('classesGrid');

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove('hidden');
}
function hideError() {
  errorBox.classList.add('hidden');
  errorBox.textContent = '';
}

browseBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  fileInput.click();
});
dropzone.addEventListener('click', () => fileInput.click());

['dragenter', 'dragover'].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  }),
);
['dragleave', 'drop'].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
  }),
);

dropzone.addEventListener('drop', (e) => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) handleFile(file);
});

resetBtn.addEventListener('click', () => {
  resultArea.classList.add('hidden');
  fileInput.value = '';
  hideError();
});

async function handleFile(file) {
  hideError();
  if (!file.type.startsWith('image/')) {
    showError('Please upload an image file (JPG, PNG, or WebP).');
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showError('Image is larger than 10 MB. Please upload a smaller file.');
    return;
  }

  const reader = new FileReader();
  reader.onload = (ev) => {
    previewImg.src = ev.target.result;
  };
  reader.readAsDataURL(file);

  resultArea.classList.add('hidden');
  loader.classList.remove('hidden');

  const fd = new FormData();
  fd.append('image', file);

  try {
    const res = await fetch('/api/predict', { method: 'POST', body: fd });
    const data = await res.json();
    if (!res.ok) {
      showError(data.error || `Request failed (${res.status}).`);
      return;
    }
    renderResult(data);
  } catch (err) {
    showError(`Network error: ${err.message}`);
  } finally {
    loader.classList.add('hidden');
  }
}

function renderResult(data) {
  const top = data.top;
  topPlant.textContent = top.plant;
  topCondition.textContent = top.condition;
  topCondition.className = `condition ${top.status}`;
  const pct = Math.round(top.confidence * 1000) / 10;
  topConfidence.textContent = `${pct}%`;
  topConfidenceBar.style.width = `${pct}%`;
  topDescription.textContent = top.description || '';
  if (top.treatment) {
    topTreatment.textContent = top.treatment;
    treatmentBlock.classList.remove('hidden');
  } else {
    treatmentBlock.classList.add('hidden');
  }
  latency.textContent = `Inference: ${data.elapsed_ms} ms`;

  topkList.innerHTML = '';
  data.predictions.forEach((p) => {
    const li = document.createElement('li');
    li.className = 'topk-row';
    const pctP = Math.round(p.confidence * 1000) / 10;
    li.innerHTML = `
      <div class="topk-name">
        <div><strong>${escapeHtml(p.plant)}</strong> · ${escapeHtml(p.condition)}</div>
        <div class="raw">${escapeHtml(p.class)}</div>
      </div>
      <div class="topk-bar">
        <div class="topk-bar-track"><div class="topk-bar-fill" style="width:${pctP}%"></div></div>
        <span class="topk-pct">${pctP.toFixed(1)}%</span>
      </div>
    `;
    topkList.appendChild(li);
  });

  resultArea.classList.remove('hidden');
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

async function loadClasses() {
  try {
    const res = await fetch('/api/info');
    const data = await res.json();
    if (!data.classes || !data.classes.length) {
      classesGrid.innerHTML = '<p class="muted">No classes loaded. Train the model first.</p>';
      return;
    }
    classesGrid.innerHTML = '';
    data.classes.forEach((c) => {
      const div = document.createElement('div');
      div.className = `class-chip ${c.status}`;
      div.innerHTML = `<div class="plant">${escapeHtml(c.plant)}</div><div class="cond">${escapeHtml(c.condition)}</div>`;
      classesGrid.appendChild(div);
    });
  } catch (e) {
    classesGrid.innerHTML = '<p class="muted">Could not load classes.</p>';
  }
}

loadClasses();
