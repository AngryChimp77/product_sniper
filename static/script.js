find ~ -name "server.py"

function analyzeProduct() {

    const link = document.getElementById("productLink").value;

    fetch("/analyze", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            link: link
        })

    })

    .then(response => response.json())

    .then(data => {

        document.getElementById("score").innerText = data.score;

        document.getElementById("verdict").innerText = data.verdict;

        document.getElementById("reason").innerText = data.reason;

    })

    .catch(error => {

        console.error(error);

        alert("Error analyzing product");

    });

}

