/* ========================================
   AR Model Uploader - JavaScript
   ======================================== */

let selectedFile = null;
let currentFileId = null;

// ========== Initialize ==========
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDrop();
    loadModels();
});

// ========== Drag and Drop Setup ==========
function setupDragAndDrop() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    // Drag over
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('dragover');
    });

    // Drag leave
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');
    });

    // Drop
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

// ========== File Selection ==========
function handleFileSelect(file) {
    // Check file type
    const allowedExtensions = ['glb', 'usdz', 'gltf', 'obj'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        showError(`❌ ファイル形式が対応していません。対応形式: ${allowedExtensions.join(', ')}`);
        return;
    }

    // Check file size (100MB)
    const maxSize = 100 * 1024 * 1024;
    if (file.size > maxSize) {
        showError(`❌ ファイルサイズが大きすぎます。最大: 100MB (現在: ${(file.size / (1024 * 1024)).toFixed(2)}MB)`);
        return;
    }

    selectedFile = file;
    showFileInfo();
    clearError();
}

// ========== Show File Info ==========
function showFileInfo() {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');

    fileName.textContent = `📄 ファイル名: ${selectedFile.name}`;
    fileSize.textContent = `📊 サイズ: ${(selectedFile.size / (1024 * 1024)).toFixed(2)}MB`;
    fileInfo.style.display = 'block';
}

// ========== Clear File ==========
function clearFile() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    clearError();
}

// ========== Upload File ==========
function uploadFile() {
    // Validation
    if (!selectedFile) {
        showError('❌ ファイルを選択してください');
        return;
    }

    const title = document.getElementById('titleInput').value.trim();
    if (!title) {
        showError('❌ モデルタイトルを入力してください');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('title', title);
    formData.append('description', document.getElementById('descriptionInput').value);

    // Disable button
    document.getElementById('uploadBtn').disabled = true;

    // Show progress
    showProgress();

    // Upload
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentFileId = data.file_id;
            showSuccess(data);
            loadModels();
        } else {
            showError(`❌ エラー: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        showError(`❌ アップロードに失敗しました: ${error.message}`);
    })
    .finally(() => {
        document.getElementById('uploadBtn').disabled = false;
        hideProgress();
    });
}

// ========== Show Progress ==========
function showProgress() {
    document.getElementById('progressContainer').style.display = 'block';
    document.getElementById('progressFill').style.width = '0%';
    
    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 90) progress = 90;
        
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('progressText').textContent = `アップロード中: ${Math.floor(progress)}%`;
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 200);

    // Complete progress after upload
    setTimeout(() => {
        clearInterval(interval);
    }, 5000);
}

// ========== Hide Progress ==========
function hideProgress() {
    const progressContainer = document.getElementById('progressContainer');
    setTimeout(() => {
        progressContainer.style.display = 'none';
        document.getElementById('progressFill').style.width = '0%';
    }, 500);
}

// ========== Show Success ==========
function showSuccess(data) {
    const successContainer = document.getElementById('successContainer');
    const successMessage = document.getElementById('successMessage');
    const embedCode = document.getElementById('embedCode');
    const viewerLink = document.getElementById('viewerLink');

    // Update content
    successMessage.innerHTML = `
        ✅ ファイル <strong>${data.file_name}</strong> がアップロードされました！<br>
        <small>Google Driveリンク: <a href="${data.public_url}" target="_blank">ここをクリック</a></small>
    `;

    embedCode.textContent = data.embed_code;

    viewerLink.innerHTML = `
        <a href="${data.viewer_url}" target="_blank">${data.viewer_url}</a>
    `;

    successContainer.style.display = 'block';
    document.getElementById('uploadContainer').style.display = 'none';
}

// ========== Open Viewer ==========
function openViewer() {
    if (currentFileId) {
        const viewerUrl = `/api/viewer/${currentFileId}`;
        window.open(viewerUrl, '_blank');
    }
}

// ========== Copy to Clipboard ==========
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;

    navigator.clipboard.writeText(text).then(() => {
        alert('✅ コピーしました！');
    }).catch(err => {
        console.error('コピーに失敗しました:', err);
    });
}

// ========== Reset Form ==========
function resetForm() {
    // Clear inputs
    document.getElementById('titleInput').value = '';
    document.getElementById('descriptionInput').value = '';
    clearFile();

    // Hide success container
    document.getElementById('successContainer').style.display = 'none';
    document.getElementById('uploadContainer').style.display = 'block';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========== Show Error ==========
function showError(message) {
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
}

// ========== Clear Error ==========
function clearError() {
    document.getElementById('errorContainer').style.display = 'none';
}

// ========== Load Models ==========
function loadModels() {
    fetch('/api/models')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayModels(data.models);
            }
        })
        .catch(error => console.error('Error loading models:', error));
}

// ========== Display Models ==========
function displayModels(models) {
    const modelsList = document.getElementById('modelsList');

    if (models.length === 0) {
        modelsList.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #718096;">まだモデルがアップロードされていません</p>';
        return;
    }

    modelsList.innerHTML = models.map(model => `
        <div class="model-card">
            <h3>🎨 ${model.title}</h3>
            <div class="model-info">
                <strong>ファイル:</strong> ${model.file_name}
            </div>
            <div class="model-info">
                <strong>サイズ:</strong> ${model.file_size_mb}MB
            </div>
            <div class="model-info">
                <strong>アップロード:</strong> ${new Date(model.uploaded_at).toLocaleDateString('ja-JP')}
            </div>
            <div class="model-buttons">
                <button class="btn btn-primary" onclick="window.open('${model.viewer_url}', '_blank')">
                    🎮 見る
                </button>
                <button class="btn btn-secondary" onclick="deleteModel('${model.file_id}')">
                    🗑️ 削除
                </button>
            </div>
        </div>
    `).join('');
}

// ========== Delete Model ==========
function deleteModel(fileId) {
    if (confirm('このモデルを削除してもよろしいですか？')) {
        fetch(`/api/delete/${fileId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ モデルが削除されました');
                loadModels();
            } else {
                alert(`❌ エラー: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Delete error:', error);
            alert('❌ 削除に失敗しました');
        });
    }
}

// ========== Auto-reload Models ==========
setInterval(loadModels, 10000); // Reload every 10 seconds
