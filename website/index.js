const counter = document.querySelector(".counter-number");
async function updateCounter() {
    let response = await fetch(
        "https://cv5w5jmhloyiqm7euhsl5724l40ghbbc.lambda-url.us-east-1.on.aws/"
    );
    let data = await response.json();
    counter.innerHTML = `👀 Views: ${data}`;
}
updateCounter();