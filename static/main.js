async function sendMessage() {
    const responseElement = document.getElementById('response');
    const userInput = document.getElementById('userInput').value;
    const modelName = "vicuna_q2"; // Example model name

    responseElement.innerHTML = '<p>Sending...</p>';

    try {
        const response = await fetch('/send_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: userInput,
                model_name: modelName,
                dyn_batch: 1,
                speculative_decoding: true
            }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            responseElement.innerHTML = `<p>Error: ${errorText}</p>`;
            return;
        }

        const data = await response.json();
        responseElement.innerHTML = `<p>Task ID: ${data.task_id}</p><p>Waiting for response...</p>`;

        // Start polling for task status
        await pollTaskStatus(data.task_id);
    } catch (error) {
        responseElement.innerHTML = '<p>Error sending message.</p>';
        console.error('Error:', error);
    }
}

async function pollTaskStatus(taskId) {
    const responseElement = document.getElementById('response');

    try {
        while (true) {
            const response = await fetch(`/poll_task_status/${taskId}`);
            const result = await response.json();

            if (result.status === 'finished' || result.status === 'failed') {
                responseElement.innerHTML = `
                    <p><strong>Status:</strong> ${result.status}</p>
                    <p><strong>Result:</strong> ${result.result}</p>`;
                break;
            }

            // Wait for 2 seconds before polling again
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    } catch (error) {
        responseElement.innerHTML = '<p>Error fetching task status.</p>';
        console.error('Error:', error);
    }
}