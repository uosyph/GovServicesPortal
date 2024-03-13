function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    const files = ev.dataTransfer.files;
    handleFiles(files);
}

function handleFiles(files) {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = '';

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');

        // Generate thumbnail
        const thumbnail = document.createElement('img');
        thumbnail.classList.add('thumbnail');
        thumbnail.file = file;
        thumbnail.style.width = '50px';
        thumbnail.style.height = '50px';
        fileItem.appendChild(thumbnail);

        // File name and size
        const fileInfo = document.createElement('div');
        fileInfo.classList.add('file-info');

        const fileNameSpan = document.createElement('span');
        fileNameSpan.classList.add('file-name');
        fileNameSpan.textContent = `${file.name}`;

        const fileSizeSpan = document.createElement('span');
        fileSizeSpan.classList.add('file-size');
        fileSizeSpan.textContent = `(${formatBytes(file.size)})`;

        fileItem.title = `${file.name} (${formatBytes(file.size)})`

        fileInfo.appendChild(fileNameSpan);
        fileInfo.appendChild(fileSizeSpan);
        fileItem.appendChild(fileInfo);
        fileList.appendChild(fileItem);

        // Display thumbnail
        const reader = new FileReader();
        reader.onload = (function (aImg) {
            return function (e) {
                aImg.src = e.target.result;
            };
        })(thumbnail);

        reader.readAsDataURL(file);
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
