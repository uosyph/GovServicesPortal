const form = document.getElementById('updateForm');
const inputs = form.querySelectorAll('input[type=text], textarea');
const submitButton = document.getElementById('submitButton');

// Disable update button on page load
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
