function toggleOptionBox() {
    var serviceRadio = document.getElementById("service");
    var optionBox = document.getElementById("option-box");

    if (serviceRadio.checked) optionBox.style.display = "block";
    else optionBox.style.display = "none";
}
