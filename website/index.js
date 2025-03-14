const counter = document.querySelector(".counter-number");
async function updateCounter() {
    
    try {
        let response = await fetch('https://84qhfs9mr3.execute-api.us-east-1.amazonaws.com/prod/visitor', {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
              },
        });
        let data = await response.json();
        counter.innerHTML = `👀 Views: ` + data;
        //document.getElementById("visitors").innerHTML = `👀 Views: ${data.views}`;
        console.log(data);
        return data;
    } catch (err) {
        console.error(err);
    }
}


updateCounter();



/*
const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try{
        let response = await fetch(
            "https://84qhfs9mr3.execute-api.us-east-1.amazonaws.com/prod/visitor", {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
              },
        });
        if (!response.ok) {
             throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let visitors = await response.json();
        counter.innerHTML = `👀 Views: ${visitors.views}`;
        } catch (error) {
        console.error('Error in updateCounter:', error);
      }
}
updateCounter();
*/

/*

const counter = document.querySelector(".counter-number");
async function updateCounter() {
    try{
        let response = await fetch(
            "https://84qhfs9mr3.execute-api.us-east-1.amazonaws.com/prod/visitor", {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
              },
        });
        if (!response.ok) {
             throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let visitors = await response.json();
        counter.innerHTML = `👀 Views: ${visitors.views}`;
        } catch (error) {
        console.error('Error in updateCounter:', error);
      }
}

updateCounter();
*/
