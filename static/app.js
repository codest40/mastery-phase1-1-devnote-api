let offset = 0;
const limit = 5;

async function fetchStatus() {
  const start = performance.now();
  const res = await fetch(`/status?offset=${offset}&limit=${limit}`);
  const data = await res.json();
  document.getElementById("env").textContent = data.env;
  document.getElementById("count").textContent = data.total_notes;
  document.getElementById("time").textContent = Math.round(performance.now() - start);
  return data.notes;
}

async function loadNotes(reset = true) {
  document.getElementById("loading").style.display = "block";
  const notes = await fetchStatus();
  const container = document.getElementById("notesContainer");
  if (reset) container.innerHTML = "";
  notes.forEach(note => {
    container.innerHTML += `
      <div class='note'>
        <div>
          <h3>${note.title}</h3>
          <p>${note.content || ''}</p>
        </div>
        <div>
          <button onclick="deleteNote(${note.id})">Delete</button>
          <button onclick="editNote(${note.id}, '${note.title}', '${note.content || ''}')">Edit</button>
        </div>
      </div>`;
  });
  document.getElementById("loading").style.display = "none";
}

async function deleteNote(id) {
  await fetch(`/notes/${id}`, { method: 'DELETE' });
  loadNotes();
}

function editNote(id, oldTitle, oldContent) {
  const title = prompt("Edit title:", oldTitle);
  const content = prompt("Edit content:", oldContent);
  if (title !== null) {
    fetch(`/notes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    }).then(loadNotes);
  }
}

document.getElementById("noteForm").addEventListener("submit", async e => {
  e.preventDefault();
  const title = document.getElementById("title").value.trim();
  const content = document.getElementById("content").value.trim();
  if (!title) return alert("Title required!");
  await fetch("/notes/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content })
  });
  document.getElementById("noteForm").reset();
  loadNotes();
});

document.getElementById("loadMore").addEventListener("click", () => {
  offset += limit;
  loadNotes(false);
});

// Initial load
loadNotes();
