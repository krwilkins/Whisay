// Event listener for image input changes
document.getElementById('image-input').addEventListener('change', function() {
  handleFileChange(this);
});

/**
 * Handles file input change events.
 * 
 * @param {HTMLInputElement} input - The input element that triggered the change event.
 */
function handleFileChange(input) {
  if (input.files && input.files[0]) {
    // Enable the translate button and update the result message
    document.getElementById('translate-button').disabled = false;
    document.getElementById('result').innerText = 'Image uploaded successfully. Ready to translate.';
  } else {
    // Disable the translate button and prompt user to select an image
    document.getElementById('translate-button').disabled = true;
    document.getElementById('result').innerText = 'Please select an image.';
  }
}

/**
 * Handles the translation process when the translate button is clicked.
 */
async function translateImage() {
  const input = document.getElementById('image-input');
  const progressBar = document.getElementById('progress-bar');

  if (input.files && input.files[0]) {
    // Reset and show the progress bar
    progressBar.style.width = '0%';
    progressBar.style.visibility = 'visible';

    const formData = new FormData();
    formData.append('image', input.files[0]);

    try {
      // Simulate progress bar update
      let progress = 0;
      const interval = setInterval(() => {
        if (progress < 90) {
          progress += 10;
          progressBar.style.width = progress + '%';
        }
      }, 500);

      // Send the image to the server for translation
      const response = await fetch('/translate', {
        method: 'POST',
        body: formData,
      });

      // Clear the interval and complete the progress bar
      clearInterval(interval);
      progressBar.style.width = '100%';

      // Play the received audio response
      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audio.play();
      } else {
        const error = await response.json();
        throw new Error('Translation error: ' + error.error);
      }
    } catch (error) {
      console.error('Error:', error);
      document.getElementById('result').innerText = 'Error occurred during the translation: ' + error.message;
    } finally {
      // Hide the progress bar after a brief delay
      setTimeout(() => {
        progressBar.style.width = '0%';
        progressBar.style.visibility = 'hidden';
      }, 1000);
    }
  } else {
    alert('Please select an image.');
  }
}
