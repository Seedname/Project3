
const submit = async (event) => {
    event.preventDefault();

    const apiUrl = new URL("http://127.0.0.1:8080/bfs");
    const actor1 = document.getElementById("first");
    const actor2 = document.getElementById("second");

    apiUrl.searchParams.append('source', actor1.value);
    apiUrl.searchParams.append('target', actor2.value);

    const response = await fetch(apiUrl, {
        method: "GET"
    });

    const result = await response.json();
    document.getElementById("output").innerText = JSON.stringify(result);
}

document.getElementById("form").addEventListener("submit", submit);