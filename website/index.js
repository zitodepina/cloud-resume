const counter = document.querySelector(".counter-number");

const url_id = window.location.href;
console.log(url_id);

VISITORS_ENDPOINT = "https://upqg49f2a4.execute-api.us-east-1.amazonaws.com/prod/visitor" + '?' + 'id='+url_id;

async function updateCounter() {
    try {
        let response = await fetch(VISITORS_ENDPOINT, {
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