async function sendMessage() {
    const responseElement = document.getElementById('response');
    responseElement.textContent = 'Sending...';

    try {
        const response = await fetch('/send_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: 'Hello' }),
        });

        const data = await response.json();
        responseElement.textContent = `Response: ${data.task_id}`;
    } catch (error) {
        responseElement.textContent = 'Error sending message.';
        console.error('Error:', error);
    }
}
