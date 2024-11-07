document.getElementById('transfer-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const shareLink = document.getElementById('share_link').value;
    const token = document.getElementById('token').value;
    const output = document.getElementById('output');
    const errorMessage = document.getElementById('error-message');
    output.value = '';
    errorMessage.style.display = 'none';

    const sseUrl = '/transfer?' + new URLSearchParams({ share_link: shareLink, token: token });

    fetch(sseUrl)
        .then(response => {
            if (response.ok) {
                const eventSource = new EventSource(sseUrl);

                eventSource.onmessage = function (event) {
                    output.value += event.data + '\r';
                    output.scrollTop = output.scrollHeight;
                };

                eventSource.onerror = function (error) {
                    console.error('Error:', error);
                    eventSource.close();
                };

                eventSource.onopen = function () {
                    console.log('Connection opened');
                };
            } else if (response.status === 401) {
                errorMessage.textContent = 'Invalid token';
                errorMessage.style.display = 'block';
            } else {
                console.error('Failed to connect, status:', response.status);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
});