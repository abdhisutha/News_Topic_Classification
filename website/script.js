
async function analyzeNews() {
    const url = document.getElementById("url").value.trim();
    const topic = document.getElementById("topic").value;
    const result = document.getElementById("result");

    if (!url) {
        result.textContent = "Please enter a news article URL.";
        return;
    }

    result.textContent = "Analyzing article...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url, topic })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Server error: " + response.status
            );
        }

        result.replaceChildren();

        const heading = document.createElement("h3");
        heading.textContent = "Result";
        result.appendChild(heading);

        const fields = [
            ["Title", data.title],
            ["Language", data.language],
            ["Predicted category", data.predicted_topic],
            ["Selected category", data.topic],
            ["Status", data.status]
        ];

        fields.forEach(([label, value]) => {
            const p = document.createElement("p");
            const b = document.createElement("b");

            b.textContent = label + ": ";
            p.appendChild(b);
            p.appendChild(document.createTextNode(value || ""));
            result.appendChild(p);
        });

        const summary = data.summary;

        if (summary && typeof summary === "object") {
            const summaryHeading = document.createElement("h3");
            summaryHeading.textContent = "Summary";
            result.appendChild(summaryHeading);

            const summaryFields = [
                ["English Summary", summary.english]
            ];

            if (data.language === "te") {
                summaryFields.push(
                    ["Telugu Summary", summary.telugu]
                );
            }

            summaryFields.forEach(([label, value]) => {
                if (!value || value === "Currently unavailable.") {
                    return;
                }

                const p = document.createElement("p");
                const b = document.createElement("b");

                b.textContent = label + ": ";
                p.appendChild(b);
                p.appendChild(document.createTextNode(value));

                result.appendChild(p);
            });

        } else {
            const p = document.createElement("p");
            const b = document.createElement("b");

            b.textContent = "Summary: ";
            p.appendChild(b);
            p.appendChild(document.createTextNode(
                summary || "No summary available."
            ));

            result.appendChild(p);
        }

    } catch (error) {
        result.textContent = "Error: " + error.message;
    }
}
