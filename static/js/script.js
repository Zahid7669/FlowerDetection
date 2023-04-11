const form = document.querySelector('form');
const fileInput = document.querySelector('input[type="file"]');
const predictionElem = document.querySelector('.prediction');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Disable the form elements while the prediction is being made
    fileInput.disabled = true;
    form.querySelector('button').disabled = true;

    // Send a FormData object containing the uploaded image to the server
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(prediction => {
        // Update the UI with the prediction result
        predictionElem.textContent = `${prediction}`;

        // Re-enable the form elements
        fileInput.disabled = false;
        form.querySelector('button').disabled = false;
    })
    .catch(error => console.error(error));
});
