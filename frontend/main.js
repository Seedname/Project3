let actors = [];     // array of actor names (strings), sorted
let actorMap = {};   // name -> id
let actorIdToName = {};
let movieIdToName = {};


// binary search with a prefix
function lowerBoundPrefix(arr, prefix) {
  let lo = 0, hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid].localeCompare(prefix) < 0) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return lo;
}

// source: https://stackoverflow.com/questions/32589197/how-can-i-capitalize-the-first-letter-of-each-word-in-a-string-using-javascript
function titleCase(str) {
    var splitStr = str.toLowerCase().split(' ');
    for (var i = 0; i < splitStr.length; i++) {
        splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
    }
    return splitStr.join(' '); 
 }


// given an input element and its suggestion list ul, update suggestions
function attachAutocomplete(inputEl, suggestionsEl, idHiddenEl) {
  inputEl.addEventListener('input', () => {
    const q = inputEl.value.trim().toLowerCase();
    suggestionsEl.innerHTML = '';
    idHiddenEl.value = ''; // clear selected id

    if (q.length === 0) return;

    let idx = lowerBoundPrefix(actors, q);
    let count = 0;
    // grab up to 8 matches
    while (idx < actors.length && count < 8) {
      const name = actors[idx];
      if (!name.startsWith(q)) break;
      const li = document.createElement('li');
      li.textContent = titleCase(name);
      li.addEventListener('click', () => {
        inputEl.value = name;
        idHiddenEl.value = actorMap[name];
        suggestionsEl.innerHTML = '';
      });
      suggestionsEl.appendChild(li);
      idx++;
      count++;
    }
  });

  // hide suggestions on blur (delay to allow click)
  inputEl.addEventListener('blur', () => {
    setTimeout(() => suggestionsEl.innerHTML = '', 200);
  });
}

async function init() {
    //
    // 1) Load the actor-name → ID map (for autocomplete)
    //
    const resp = await fetch('./actor_names_sorted.json');
    const data = await resp.json();
    actors = Object.keys(data);
    actorMap = data; // name → id
  
    //
    // 2) Load the ID → actor-name map
    //
    {
      const r = await fetch('./id_actors_names.json');
      actorIdToName = await r.json();
    }
  
    //
    // 3) Load the ID → movie-title map
    //
    {
      const r = await fetch('./id_movies_names.json');
      movieIdToName = await r.json();
    }
  
    //
    // 4) Wire up autocompletes
    //
    attachAutocomplete(
      document.getElementById('first'),
      document.getElementById('first_suggestions'),
      document.getElementById('first_id')
    );
    attachAutocomplete(
      document.getElementById('second'),
      document.getElementById('second_suggestions'),
      document.getElementById('second_id')
    );
  }
  
  const submit = async event => {
    event.preventDefault();
  
    const sourceId = document.getElementById("first_id").value;
    const targetId = document.getElementById("second_id").value;
    if (!sourceId || !targetId) {
      return alert("Please select both actors from the suggestions.");
    }
  
    // 1) Query the BFS endpoint
    const apiUrl = new URL("http://127.0.0.1:8080/bfs");
    apiUrl.searchParams.append('source', sourceId);
    apiUrl.searchParams.append('target', targetId);
    const res = await fetch(apiUrl);
    const { path } = await res.json();               // e.g. [[A1, M1], [A2, M2], ...]

    // 2) Format into human-readable HTML
    const out = document.getElementById("output");
    out.innerHTML = "";  // clear previous
  
    if (!path || path.length === 0) {
      out.textContent = "No connection found.";
      return;
    }

    // Build a <ul> with one <li> per “hop”
    const ul = document.createElement('ul');
    let previousActorId = sourceId;
    for (let i = 0; i < path.length; i++) {
      const [actorId, movieId] = path[i];
    //   const nextActorId     = path[i+1][0];
  
      const actorName  = actorIdToName[String(previousActorId)]  || `(actor #${previousActorId})`;
      const movieTitle = movieIdToName[String(movieId)]  || `(movie #${movieId})`;
      const nextActor  = actorIdToName[String(actorId)] || `(actor #${actorId})`;
    previousActorId = actorId;
      const li = document.createElement('li');
      li.textContent = `${actorName} appeared in “${movieTitle}” with ${nextActor}.`;
      ul.appendChild(li);
    }
  
  
    out.appendChild(ul);
  };
  

document.getElementById("form").addEventListener("submit", submit);

// run on page load
init().catch(err => console.error(err));
