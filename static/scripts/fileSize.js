function getFileSize(fileUrl, tooltipElement) {
    fetch(fileUrl)
        .then(response => {
            const size = response.headers.get('content-length');
            const fileSize = formatFileSize(size);
            tooltipElement.textContent = fileSize;
        })
        .catch(error => { });
}

function formatFileSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes == 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}

// Get all elements with the common class 'download-btn'
const buttons = document.querySelectorAll('.download-btn');

// Loop through each button and get file size for each button individually
buttons.forEach(button => {
    const tooltip = button.querySelector('.tooltip');
    const fileUrl = tooltip.getAttribute('data-file');
    getFileSize(fileUrl, tooltip);
});
