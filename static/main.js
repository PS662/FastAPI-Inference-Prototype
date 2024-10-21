async function sendMessage() {
    const responseElement = document.getElementById('response');
    const userInput = document.getElementById('userInput').value;
    responseElement.innerHTML = '<p>Sending...</p>';

    try {
        const response = await fetch('/send_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: userInput,
                model_name: 'vicuna_q2',
                dyn_batch: 1,
                speculative_decoding: false,
            }),
        });

        const data = await response.json();
        const taskId = data.task_id;

        if (taskId) {
            await pollTaskStatus(taskId); // Await the polling result
        } else {
            responseElement.innerHTML = '<p>Error: No task ID returned.</p>';
        }
    } catch (error) {
        responseElement.innerHTML = '<p>Error sending message.</p>';
        console.error('Error:', error);
    }
}

async function pollTaskStatus(taskId, targetStatus = 'finished') {
    const responseElement = document.getElementById('response');

    try {
        const response = await fetch(`/poll_task_status/${taskId}?target_status=${targetStatus}`);
        const result = await response.json();

        if (result.status === 'finished') {
            responseElement.innerHTML = `
                <div class="response-item">
                    <p><strong>Status:</strong> ${result.status}</p>
                    <p><strong>Result:</strong> ${result.result}</p>
                </div>`;
        } else if (result.status === 'failed') {
            responseElement.innerHTML = '<p>Error: Task failed.</p>';
        } else {
            responseElement.innerHTML = '<p>Unexpected status received.</p>';
        }
    } catch (error) {
        responseElement.innerHTML = '<p>Error fetching task status.</p>';
        console.error('Error:', error);
    }
}