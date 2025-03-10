const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try{
        let response = await fetch(
            "https://llljmtwhn5.execute-api.us-east-1.amazonaws.com/prod/visitor", {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
              },
        });
        if (!response.ok) {
             throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        counter.innerHTML = `👀 Views: ${data.views}`;
        } catch (error) {
        console.error('Error in updateCounter:', error);
      }
}

updateCounter();