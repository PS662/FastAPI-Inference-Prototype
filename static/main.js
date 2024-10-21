async function sendMessage() {
    const responseElement = document.getElementById('response');
    const spinner = document.getElementById('spinner');
    const userInput = document.getElementById('userInput').value;

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
            spinner.classList.remove('hidden');  // Show spinner
            await pollTaskStatus(taskId);
        } else {
            responseElement.innerHTML = '<p>Error: No task ID returned.</p>';
        }
    } catch (error) {
        responseElement.innerHTML = '<p>Error sending message.</p>';
        console.error('Error:', error);
    }
}

async function pollTaskStatus(taskId, targetStatus = 'SUCCESS') {
    const responseElement = document.getElementById('response');
    const spinner = document.getElementById('spinner');

    try {
        const response = await fetch(`/poll_task_status/${taskId}?target_status="SUCCESS"`);
        const result = await response.json();

        if (result.status === 'SUCCESS') {
            responseElement.innerHTML = `
                <div class="response-item">
                    <p><strong>Result:</strong> ${result.result}</p>
                </div>`;
        } else if (result.status === 'failed') {
            responseElement.innerHTML = '<p>Error: Task failed.</p>';
        } else {
            responseElement.innerHTML = '<p>Status is still pending...</p>';
            setTimeout(() => pollTaskStatus(taskId, targetStatus), 1000); // Retry polling
            return;  // Exit to avoid hiding spinner prematurely
        }
    } catch (error) {
        responseElement.innerHTML = '<p>Error fetching task status.</p>';
        console.error('Error:', error);
    } finally {
        spinner.classList.add('hidden');  // Hide spinner
    }
}