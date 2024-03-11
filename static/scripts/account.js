document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('.navigation a');
    const settingsSections = document.querySelectorAll('.settings-section');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            settingsSections.forEach(section => {
                if (section.id === targetId) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });

            // Remove active class from all links
            links.forEach(link => {
                link.classList.remove('active');
            });

            // Add active class to the clicked link
            this.classList.add('active');
        });
    });
});

const form = document.getElementById('updateForm');
const inputs = form.querySelectorAll('input[type=text]');
const submitButton = document.getElementById('submitButton');

// Disable submit button on page load
submitButton.disabled = true;

inputs.forEach(input => {
    input.addEventListener('input', function () {
        let changed = false;
        inputs.forEach(input => {
            if (input.defaultValue !== input.value) changed = true;
        });

        if (changed) submitButton.disabled = false;
        else submitButton.disabled = true;
    });
});
