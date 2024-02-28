document.addEventListener('DOMContentLoaded', function() {
    const encodeForm = document.getElementById('encodeForm');
    const decodeForm = document.getElementById('decodeForm');
    const backToFormButton = document.getElementById('backToFormButton');
    const transferButton = document.getElementById('transferButton');

    if (encodeForm) {
        encodeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            encodeImage();
        });
    }

    if (decodeForm) {
        decodeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            decodeImage();
        });
    }

    if (backToFormButton) {
        backToFormButton.addEventListener('click', function() {
            document.getElementById('encodedImageDiv').style.display = 'none';
    
            document.getElementById('encodeForm').style.display = 'block';
            
            document.getElementById('backToFormButton').style.display = 'none';

            document.getElementById('title').textContent = "Encode Message";
        });
    }

    if (transferButton) {
        transferButton.addEventListener('click', function() {
            var encodedImageSrc = document.getElementById('encodedImage').src;
            var defaultFilename = encodedImageSrc.substring(encodedImageSrc.lastIndexOf('/') + 1);
            var customFilename = "encoded_image.png";
            var link = document.createElement('a');

            link.href = encodedImageSrc;
            
            link.download = customFilename || defaultFilename;
            
            link.click();
        });
    }
});


function encodeImage() {
    const formData = new FormData(document.getElementById('encodeForm'));
    const csrfToken = formData.get('csrfmiddlewaretoken');
    
    // Remove the CSRF token from the form data
    formData.delete('csrfmiddlewaretoken');

    fetch('/encode', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('encodeForm').style.display = 'none';
        
        document.getElementById('encodedImage').src = 'data:image/png;base64,' + data.encoded_image;
        document.getElementById('encodedImageDiv').style.display = 'block';
        
        document.getElementById('backToFormButton').style.display = 'block';

        document.getElementById('title').textContent = "Encoded Image";
    })
    .catch(error => {
        console.error('Error:', error);
        const encodeErrorMessage = document.getElementById('encodeErrorMessage');
        encodeErrorMessage.style.display = 'block';
    });
}

function decodeImage() {
    const formData = new FormData(document.getElementById('decodeForm'));
    const csrfToken = formData.get('csrfmiddlewaretoken');
    
    // Remove the CSRF token from the form data
    formData.delete('csrfmiddlewaretoken');

    fetch('/decode', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        const decodedMessageContainer = document.getElementById('decodedMessageContainer');
        const decodedMessageContent = document.getElementById('decodedMessageContent');
        const decodeErrorMessage = document.getElementById('decodeErrorMessage');

        if (data.error) {
            decodeErrorMessage.textContent = data.error;
            decodeErrorMessage.style.display = 'block';
            decodedMessageContainer.style.display = 'none';
        } else {
            decodedMessageContent.textContent = '"' + data.message + '"';
            decodedMessageContainer.style.display = 'block';
            decodeErrorMessage.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const decodeErrorMessage = document.getElementById('decodeErrorMessage');
        decodeErrorMessage.textContent = "An error occurred. Please try again.";
        decodeErrorMessage.style.display = 'block';

        const decodedMessageContainer = document.getElementById('decodedMessageContainer');
        decodedMessageContainer.style.display = 'none';
    });
}

