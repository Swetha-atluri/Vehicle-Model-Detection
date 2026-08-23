document.addEventListener('DOMContentLoaded', () => {
    // State
    let selectedFile = null;

    // DOM Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const dropZoneContent = document.querySelector('.drop-zone-content');
    
    const btnDetect = document.getElementById('btn-detect');
    const btnClear = document.getElementById('btn-clear');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');

    const resultsEmpty = document.getElementById('results-empty');
    const resultsActive = document.getElementById('results-active');
    const annotatedImage = document.getElementById('annotated-image');
    const detectionsTbody = document.getElementById('detections-tbody');
    
    // Stats & Analytics Elements
    const countCar = document.getElementById('count-car');
    const countTruck = document.getElementById('count-truck');
    const countBus = document.getElementById('count-bus');
    const countMotorcycle = document.getElementById('count-motorcycle');
    
    const analyticsTotalCount = document.getElementById('analytics-total-count');
    const analyticsResolution = document.getElementById('analytics-resolution');

    // --- Drag and Drop Handlers ---
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    dropZone.addEventListener('click', (e) => {
        // Prevent trigger loop when clicking browse label
        if (e.target.tagName !== 'LABEL' && e.target.tagName !== 'INPUT') {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // File Preview Logic
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file.');
            return;
        }
        selectedFile = file;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            dropZoneContent.style.opacity = '0';
            
            // Enable detect button
            btnDetect.disabled = false;
            btnClear.style.display = 'inline-flex';
        };
        reader.readAsDataURL(file);
    }

    // --- Detect Request ---
    btnDetect.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI Loading State
        btnDetect.disabled = true;
        btnSpinner.style.display = 'inline-block';
        btnText.innerHTML = 'Analyzing...';
        
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to analyze image');
            }

            const result = await response.json();
            
            if (result.success) {
                renderResults(result);
            }
        } catch (error) {
            console.error('Detection error:', error);
            alert(`Analysis failed: ${error.message}`);
        } finally {
            // Restore Button State
            btnDetect.disabled = false;
            btnSpinner.style.display = 'none';
            btnText.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Run Detection';
        }
    });

    // --- Render Detection Results ---
    function renderResults(data) {
        // Update Stats Values
        countCar.textContent = data.counts.car || 0;
        countTruck.textContent = data.counts.truck || 0;
        countBus.textContent = data.counts.bus || 0;
        countMotorcycle.textContent = data.counts.motorcycle || 0;

        // Render Annotated Image
        annotatedImage.src = data.annotated_image;

        // Render Table Log Rows
        detectionsTbody.innerHTML = '';
        if (data.detections.length === 0) {
            detectionsTbody.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align: center; color: var(--text-muted); padding: 30px 0;">No vehicles detected</td>
                </tr>
            `;
        } else {
            data.detections.forEach(det => {
                const confPercent = Math.round(det.confidence * 100);
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>
                        <span class="tag-class" data-class="${det.class}">${det.class}</span>
                    </td>
                    <td>
                        <div class="confidence-wrapper" data-class="${det.class}">
                            <strong style="width: 38px;">${confPercent}%</strong>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: ${confPercent}%;"></div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <span class="bbox-code">[${det.box.join(', ')}]</span>
                    </td>
                `;
                detectionsTbody.appendChild(tr);
            });
        }

        // Update Analytics Metrics
        analyticsTotalCount.textContent = data.summary.total_detected;
        analyticsResolution.textContent = `${data.summary.image_width} × ${data.summary.image_height}`;

        // View Transition
        resultsEmpty.style.display = 'none';
        resultsActive.style.display = 'flex';
    }

    // --- Clear Handler ---
    btnClear.addEventListener('click', () => {
        // Reset states
        selectedFile = null;
        fileInput.value = '';
        imagePreview.src = '';
        imagePreview.style.display = 'none';
        dropZoneContent.style.opacity = '1';
        
        btnDetect.disabled = true;
        btnClear.style.display = 'none';
        
        resultsActive.style.display = 'none';
        resultsEmpty.style.display = 'flex';
    });

    // --- Tabs Handling ---
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`tab-${targetTab}`).classList.add('active');
        });
    });
});
