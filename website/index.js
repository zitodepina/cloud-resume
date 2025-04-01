const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try {
        let response = await fetch('https://upqg49f2a4.execute-api.us-east-1.amazonaws.com/prod/visitor', {
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