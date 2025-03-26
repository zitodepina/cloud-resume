const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try {
        let response = await fetch('https://q0wpi5nfc3.execute-api.us-east-1.amazonaws.com/prod/visitor', {
            method: 'GET',
        });
        let data = await response.text();
        counter.innerHTML = `👀 Views: ` + data;
        console.log("Data fetched:", data);
        return data;
    } catch (err) {
        console.error("Error fetching data:", err);
    }
}
updateCounter()