let SERVER = "http://localhost:5000" || "";

/*
 * Query the server for results given a query
 */
async function loadSearchResults () {
    // Prepare JSON payload
    const query = document.getElementById('query').value;
    if (query === '') {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = ''
        console.log('Clearing results')
        return;
    }

    const response = await fetch(SERVER + "/search", {
        method: "POST",
        headers: {
          "content-type": "application/json;charset=UTF-8",
        },
        body: JSON.stringify({ query }),
      });
      const responseJson = await response.json();
    if (responseJson.error !== null) {
        console.log("Fetch error:", responseJson.error);
        return [];
    } else {
        displayResults(responseJson.result);
        return responseJson.result;
    }
}

function displayResults(results) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results

    results.forEach(item => {
        const messageItem = item.message
        const parts = messageItem.split(' "'); // Split by ' "'
        const author = parts[0];
        const message = parts[1].slice(0, -1); // Remove the trailing quote

        // Create a new div for the message and author
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result');

        // Create and append the author element
        const authorDiv = document.createElement('div');
        authorDiv.classList.add('author');
        authorDiv.textContent = author.toLowerCase();
        resultDiv.appendChild(authorDiv);

        // Create and append the message element
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.textContent = message;
        resultDiv.appendChild(messageDiv);

        // Append the result div to the results container
        resultsContainer.appendChild(resultDiv);
    });
}

window.onload = function() {
    let timeout = null;
    let input = document.getElementById('query');
    input.addEventListener('keyup', function (e) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
            loadSearchResults();
            console.log('Searching for:', input.value);
        }, 1000);
    });
}
