document.getElementById('transfer-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const shareLink = document.getElementById('share_link').value;
    const token = document.getElementById('token').value;
    const output = document.getElementById('output');
    output.value = '';

    const eventSource = new EventSource('/transfer?' + new URLSearchParams({ share_link: shareLink, token: token }));
    eventSource.onmessage = function (event) {
        output.value += event.data + '\n';
        output.scrollTop = output.scrollHeight;
    };
    eventSource.onerror = function () {
        eventSource.close();
    };
});