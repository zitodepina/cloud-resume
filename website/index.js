const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try{
        let response = await fetch(
            "https://05p9t7z66j.execute-api.us-east-1.amazonaws.com/prod/visitor", {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
              },
        });
        if (!response.ok) {
             throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const visitors = await response.json();
        counter.innerHTML = `👀 Views: ${visitors.views}`;
        } catch (error) {
        console.error('Error in updateCounter:', error);
      }
}

updateCounter();