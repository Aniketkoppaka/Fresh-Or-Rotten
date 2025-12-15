document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const uploadBox = document.querySelector('.upload-box');
    const dropZone = document.getElementById('drop-zone');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultCard = document.getElementById('result-card');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    const resultIcon = document.getElementById('result-icon');
    const confidenceBar = document.getElementById('confidence-bar');
    const resetButton = document.getElementById('reset-button');

    // Drag and Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadBox.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadBox.style.borderColor = 'var(--primary-color)';
        uploadBox.style.backgroundColor = 'rgba(102, 187, 106, 0.05)';
    }

    function unhighlight(e) {
        uploadBox.style.borderColor = '#e0e0e0';
        uploadBox.style.backgroundColor = 'white';
    }

    uploadBox.addEventListener('drop', handleDrop, false);
    uploadBox.addEventListener('click', () => fileInput.click()); // Also trigger on box click

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    fileInput.addEventListener('change', function () {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                previewImage(file);
                uploadAndPredict(file);
            } else {
                alert('Please upload an image file.');
            }
        }
    }

    function previewImage(file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            imagePreview.src = reader.result;
            dropZone.style.display = 'none';
            previewContainer.style.display = 'block';
            resultCard.classList.remove('active'); // Reset result
        }
    }

    function uploadAndPredict(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show loading
        loadingOverlay.style.display = 'flex';

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                loadingOverlay.style.display = 'none';
                displayResult(data);
            })
            .catch(error => {
                console.error('Error:', error);
                loadingOverlay.style.display = 'none';
                alert('An error occurred during prediction.');
                resetUpload();
            });
    }

    function displayResult(data) {
        resultCard.classList.add('active');

        // Remove old classes
        resultTitle.classList.remove('is-fresh', 'is-rotten');
        confidenceBar.classList.remove('fresh-bg', 'rotten-bg');

        if (data.result === 'Fresh') {
            resultTitle.textContent = 'It\'s Fresh!';
            resultTitle.classList.add('is-fresh');
            resultMessage.textContent = `Confidence: ${data.confidence}`;
            resultIcon.innerHTML = '<i class="fas fa-check-circle" style="color: var(--primary-color);"></i>';
            confidenceBar.classList.add('fresh-bg');

            // Trigger Confetti
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#66BB6A', '#FF7043', '#FFCBA4']
            });
        } else {
            resultTitle.textContent = 'It\'s Rotten';
            resultTitle.classList.add('is-rotten');
            resultMessage.textContent = `Confidence: ${data.confidence}`;
            resultIcon.innerHTML = '<i class="fas fa-times-circle" style="color: var(--danger-color);"></i>';
            confidenceBar.classList.add('rotten-bg');
        }

        // Animate bar
        setTimeout(() => {
            // confidence is string "99.99%", parse it
            const confVal = parseFloat(data.confidence);
            confidenceBar.style.width = `${confVal}%`;
        }, 100);
    }

    resetButton.addEventListener('click', resetUpload);

    function resetUpload() {
        fileInput.value = '';
        dropZone.style.display = 'flex';
        previewContainer.style.display = 'none';
        imagePreview.src = '';

        // Fully reset result card
        resultCard.classList.remove('active');
        resultTitle.textContent = 'Analyzing...';
        resultTitle.classList.remove('is-fresh', 'is-rotten');
        resultMessage.textContent = 'Upload an image to start';
        resultIcon.innerHTML = '';
        confidenceBar.style.width = '0%';
        confidenceBar.classList.remove('fresh-bg', 'rotten-bg');
    }
});
