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

// function to create a "node" in this graph (contains both actual nodes (actor) and edges(movies))
function createGraphNode(text, nodeType, id) {

  // make a new node, make the link it points to open in a new window
  const node = document.createElement('a');
  node.className = `node ${nodeType}`;
  node.target = '_blank';

  // both the text content and the link are based on the nodeType (actor-node or movie-node)
  if (nodeType === 'actor-node'){
    node.href = `https://www.themoviedb.org/person/${id}`;
    node.textContent = `Node (Actor): ${text}`;
  } else {
    node.href = `https://www.themoviedb.org/movie/${id}`;
    node.textContent = `Edge (Movie): ${text}`;
  }

  return node;
}

// create the bottom triangle section of the arrow between nodes
function createArrow() {
  const arrow = document.createElement('div');
  arrow.className = 'arrow';
  return arrow;
}

// create the top line section of the arrow between nodes
function createLine() {
  const line = document.createElement('div');
  line.className = 'line';
  return line;
}

function buildGraph(path) {

  // fetch the graph and clear the previously queried graph
  const graphContainer = document.querySelector('.graph');
  graphContainer.innerHTML = '';
  
  // get the id and name of the source node (actor), and add it to the graph
  const sourceId = document.getElementById("first_id").value;
  const firstActorName = actorIdToName[String(sourceId)];
  graphContainer.appendChild(createGraphNode(firstActorName, 'actor-node', sourceId));
  
  // loop through the quickest path detected from source to end
  for (let i = 0; i < path.length; i++) {
    actorId = path[i][0];
    movieId = path[i][1];
    
    // create the arrow between nodes
    graphContainer.appendChild(createLine());
    graphContainer.appendChild(createArrow());
    
    // add the movie node to the graph
    movieTitle = movieIdToName[String(movieId)];
    graphContainer.appendChild(createGraphNode(movieTitle, 'movie-node', movieId));
    
    // create another arrow
    graphContainer.appendChild(createLine());
    graphContainer.appendChild(createArrow());
    
    // add the next actor node to the graph
    actorName = actorIdToName[String(actorId)];
    graphContainer.appendChild(createGraphNode(actorName, 'actor-node', actorId));
  }
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
  
    // 1) Decide which endpoint to hit based on selection
  const algo = document.getElementById("algorithm").value;
  const apiUrl = new URL(`http://127.0.0.1:8080/${algo}`);
    apiUrl.searchParams.append('source', sourceId);
    apiUrl.searchParams.append('target', targetId);

    // Start timer
    const startTime = performance.now();

    const res = await fetch(apiUrl);
    const { path } = await res.json();               // e.g. [[A1, M1], [A2, M2], ...]

    // End timer
    const endTime = performance.now();
    const durationMs = endTime - startTime;

    // 2) Format into human-readable HTML
    const out = document.getElementById("output");
    out.innerHTML = "";  // clear previous

    const timeDisplay = document.createElement("p");
    timeDisplay.textContent = `Search completed in ${durationMs.toFixed(2)} ms.`;
    out.appendChild(timeDisplay);

    if (!path || path.length === 0) {
      out.textContent = `No connection found between ${actorIdToName[String(sourceId)]} and ${actorIdToName[String(targetId)]}.`;
      out.appendChild(timeDisplay);
      return;
    }

    // Build a <ul> with one <li> per "hop"
    const ul = document.createElement('ul');
    let previousActorId = sourceId;
    for (let i = 0; i < path.length; i++) {
      const [actorId, movieId] = path[i];
    //   const nextActorId     = path[i+1][0];
  
      const actorName  = actorIdToName[String(previousActorId)]  || `(actor #${previousActorId})`;
      let movieTitle = movieIdToName[String(movieId)]  || `(movie #${movieId})`;

      const nextActor  = actorIdToName[String(actorId)] || `(actor #${actorId})`;
      previousActorId = actorId;
      const li = document.createElement('li');
      li.textContent = `${actorName} appeared in "${movieTitle}" with ${nextActor}.`;
      ul.appendChild(li);
    }
  
    out.appendChild(ul);
    
    buildGraph(path);
  };
  

document.getElementById("form").addEventListener("submit", submit);

// run on page load
init().catch(err => console.error(err));