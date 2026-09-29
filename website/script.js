async function analyzeNews() {

    const url = document.getElementById("url").value;
    const topic = document.getElementById("topic").value;
    const result = document.getElementById("result");

    if (!url) {
        result.innerHTML = "Please enter a news article URL.";
        return;
    }

    result.innerHTML = "Analyzing article...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    url: url,
                    topic: topic
                })
            }
        );

        const data = await response.json();

        if (data.status === "Relevant") {

            result.innerHTML = `
                <h3>Result</h3>
                <p><b>Title:</b> ${data.title}</p>
                <p><b>Language:</b> ${data.language}</p>
                <p><b>Topic:</b> ${data.topic}</p>
                <p><b>Status:</b> ✅ ${data.status}</p>
                <p><b>Summary:</b></p>
                <p>${data.summary}</p>
            `;

        } else {

            result.innerHTML = `
                <h3>Result</h3>
                <p><b>Title:</b> ${data.title}</p>
                <p><b>Language:</b> ${data.language}</p>
                <p><b>Topic:</b> ${data.topic}</p>
                <p><b>Status:</b> ❌ ${data.status}</p>
            `;
        }

    } catch (error) {

        result.innerHTML =
            "Something went wrong. Please check the article URL and server.";
    }
}