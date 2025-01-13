const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try{
        let response = await fetch(
            "https://cv5w5jmhloyiqm7euhsl5724l40ghbbc.lambda-url.us-east-1.on.aws/"
        );
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let data = await response.json();
        counter.innerHTML = `👀 Views: ${data}`;
        } catch (error) {
        console.error('Error in updateCounter:', error);
      }
}
updateCounter();