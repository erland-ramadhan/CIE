function appendFormData() {
    const formData = new FormData();
    const imageFile = document.getElementById('imageUpload').files[0];
    formData.append('image', imageFile);
    formData.append('func', document.getElementById('dropdown').value);
    formData.append('x0', document.getElementById('x0').value);
    formData.append('alpha', document.getElementById('alpha').value);
    formData.append('beta', document.getElementById('beta').value);
    formData.append('Omega', document.getElementById('Omega').value);
    formData.append('K', document.getElementById('K').value);
    return formData;
};

function updateResults(data, key) {
    const processedImage = document.getElementById('processedImage');
    processedImage.src = `data:image/jpeg;base64,${data[key]}`;
    document.getElementById('executionTime').textContent = `${data.execution_time.toFixed(2)} seconds`;
};

document.getElementById('runEncrypt').addEventListener('click', function() {
    fetch('/encrypt', {
        method: 'POST',
        body: appendFormData()
    })
    .then(response => response.json())
    .then(data => updateResults(data, 'encrypted_image'))
    .catch(error => console.error('Error:', error));
});

document.getElementById('runDecrypt').addEventListener('click', function() {
    fetch('/decrypt', {
        method: 'POST',
        body: appendFormData()
    })
    .then(response => response.json())
    .then(data => updateResults(data, 'decrypted_image'))
    .catch(error => console.error('Error:', error));
});

document.getElementById('runCompare').addEventListener('click', function() {
    const imgData = new FormData();
    const orgImg = document.getElementById('origUpload').files[0];
    const deImg = document.getElementById('decryptUpload').files[0];
    imgData.append('org', orgImg); // Append the file correctly
    imgData.append('de', deImg); // Append the file correctly
    
    fetch('/compare', {
        method: 'POST',
        body: imgData
    })
    .then(response => response.json())
    .then(data => {
        const rmseElement = document.getElementById('rmse');
        rmseElement.textContent = `${data.calculated_rmse.toFixed(2)}`;
        const psnrElement = document.getElementById('psnr');
        if (data.calculated_psnr === "Infinity") {
            psnrElement.textContent = "Infinity";
        } else {
            psnrElement.textContent = `${data.calculated_psnr.toFixed(2)}`;
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('downloadImage').addEventListener('click', function() {
    const processedImage = document.getElementById('processedImage').src;

    const link = document.createElement('a');
    link.href = processedImage;
    link.download = 'processed_image.png'; // Set the download file name
    link.click(); // Trigger the download
});

document.getElementById('imageUpload').addEventListener('change', function(event) {
    const originalImage = document.getElementById('originalImage');

    originalImage.src = URL.createObjectURL(event.target.files[0]);
    originalImage.onload = () => URL.revokeObjectURL(originalImage.src);
    processedImage.onload = () => URL.revokeObjectURL(processedImage.src);
});

document.getElementById('origUpload').addEventListener('change', function(event) {
    const origImg = document.getElementById('origImg');

    origImg.src = URL.createObjectURL(event.target.files[0]);
    origImg.onload = () => URL.revokeObjectURL(origImg.src);
});

document.getElementById('decryptUpload').addEventListener('change', function(event) {
    const decryptImg = document.getElementById('decryptImg');
    
    decryptImg.src = URL.createObjectURL(event.target.files[0]);
    decryptImg.onload = () => URL.revokeObjectURL(decryptImg.src);
});
