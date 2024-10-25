async function translateImage() {
    const input = document.getElementById('image-input');
    if (input.files && input.files[0]) {
      const formData = new FormData();
      formData.append('image', input.files[0]);
  
      const response = await fetch('YOUR_BACKEND_URL/translate', {
        method: 'POST',
        body: formData
      });
  
      const data = await response.json();
      if (data.translated_text) {
        document.getElementById('result').innerText = data.translated_text;
      } else {
        document.getElementById('result').innerText = 'Error: ' + data.error;
      }
    } else {
      alert('Please select an image.');
    }
  }
  