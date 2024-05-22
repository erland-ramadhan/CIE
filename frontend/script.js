document.getElementById('runEncrypt').addEventListener('click', function() {
    const formData = new FormData();
    const imageFile = document.getElementById('imageUpload').files[0];
    formData.append('image', imageFile); // Append the file correctly
    formData.append('func', document.getElementById('dropdown').value);
    formData.append('x0', document.getElementById('x0').value);
    formData.append('alpha', document.getElementById('alpha').value);
    formData.append('beta', document.getElementById('beta').value);
    formData.append('Omega', document.getElementById('Omega').value);
    formData.append('K', document.getElementById('K').value);

    fetch('/encrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const processedImage = document.getElementById('processedImage');
        processedImage.src = `data:image/jpeg;base64,${data.encrypted_image}`;
        const execTimeElement = document.getElementById('executionTime');
        execTimeElement.textContent = `${data.execution_time.toFixed(2)} seconds`;
        const rmseElement = document.getElementById('rmse');
        rmseElement.textContent = `${data.calculated_rmse.toFixed(2)} seconds`;
        const psnrElement = document.getElementById('psnr');
        psnrElement.textContent = `${data.calculated_psnr} seconds`
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('runDecrypt').addEventListener('click', function() {
    const formData = new FormData();
    const imageFile = document.getElementById('imageUpload').files[0];
    formData.append('image', imageFile); // Append the file correctly
    formData.append('func', document.getElementById('dropdown').value);
    formData.append('x0', document.getElementById('x0').value);
    formData.append('alpha', document.getElementById('alpha').value);
    formData.append('beta', document.getElementById('beta').value);
    formData.append('Omega', document.getElementById('Omega').value);
    formData.append('K', document.getElementById('K').value);

    fetch('/decrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const processedImage = document.getElementById('processedImage');
        processedImage.src = `data:image/jpeg;base64,${data.decrypted_image}`;
        const execTimeElement = document.getElementById('executionTime');
        execTimeElement.textContent = `${data.execution_time.toFixed(2)} seconds`;
        const rmseElement = document.getElementById('rmse');
        rmseElement.textContent = `${data.calculated_rmse.toFixed(2)} seconds`;
        const psnrElement = document.getElementById('psnr');
        psnrElement.textContent = `${data.calculated_psnr} seconds`
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('imageUpload').addEventListener('change', function(event) {
    const originalImage = document.getElementById('originalImage');
    // const processedImage = document.getElementById('processedImage');
    originalImage.src = URL.createObjectURL(event.target.files[0]);
    originalImage.onload = function() {
        URL.revokeObjectURL(originalImage.src); // Free memory
    }
    // processedImage.src = URL.createObjectURL(event.target.files[0]);
    processedImage.onload = function() {
        URL.revokeObjectURL(processedImage.src); // Free memory
    }
});