const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', function () {
    fileList.innerHTML = '';

    for (let i = 0; i < fileInput.files.length; i++) {
        const file = fileInput.files[i];
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        fileItem.textContent = `${file.name} (${formatBytes(file.size)})`;

        // Generate thumbnail
        const thumbnail = document.createElement('img');
        thumbnail.classList.add('thumbnail');
        thumbnail.file = file;
        thumbnail.style.width = '50px';
        thumbnail.style.height = '50px';
        fileItem.appendChild(thumbnail);

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
});

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
