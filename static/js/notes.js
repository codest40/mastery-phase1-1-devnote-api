// /static/js/notes.js

// ====================
// LOAD ALL NOTES
// ====================
export async function loadNotes() {
  try {
    const res = await fetch("/notes/");
    if (!res.ok) throw new Error("Failed to load notes");

    const notes = await res.json();
    const container = document.getElementById("notesContainer");
    container.innerHTML = "";

    if (!notes.length) {
      container.innerHTML = "<p>No notes found.</p>";
      return;
    }

    notes.forEach(note => {
      const div = document.createElement("div");
      div.classList.add("note");
      div.innerHTML = `
        <div class='note-actions'>
          <button onclick="deleteNote(${note.id})">Delete</button>
          <button onclick="updateNote(${note.id}, '${note.title}', '${note.content || ""}')">Update</button>
        </div>
        <h3>${note.title}</h3>
        <p>${note.content || ""}</p>
      `;
      container.appendChild(div);
    });
  } catch (err) {
    console.error("❌ Failed to load notes:", err);
  }
}

// ====================
// CREATE A NEW NOTE
// ====================
export async function createNote(title, content) {
  try {
    const res = await fetch("/notes/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, content }),
    });
    if (!res.ok) throw new Error("Failed to create note");
    await loadNotes();
  } catch (err) {
    console.error("❌ Failed to create note:", err);
  }
}

// ====================
// UPDATE AN EXISTING NOTE
// ====================
export async function updateNote(id, oldTitle = "", oldContent = "") {
  try {
    // Prompt user for updated data
    const newTitle = prompt("Edit title:", oldTitle);
    if (newTitle === null) return; // Cancelled

    const newContent = prompt("Edit content:", oldContent);
    if (newContent === null) return; // Cancelled

    // Prepare only changed fields
    const updatedData = {};
    if (newTitle.trim() && newTitle.trim() !== oldTitle.trim()) {
      updatedData.title = newTitle.trim();
    }
    if (newContent.trim() && newContent.trim() !== oldContent.trim()) {
      updatedData.content = newContent.trim();
    }

    // If nothing changed, skip request
    if (Object.keys(updatedData).length === 0) {
      alert("No changes made.");
      return;
    }

    // Send PATCH insteadv (not PUT) — better for partial updates
    const res = await fetch(`/notes/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedData),
    });

    if (!res.ok) throw new Error("Failed to update note");

    await loadNotes();
  } catch (err) {
    console.error("❌ Failed to update note:", err);
  }
}


// ====================
// DELETE A NOTE
// ====================
export async function deleteNote(id) {
  try {
    const confirmDelete = confirm("Delete this note?");
    if (!confirmDelete) return;

    const res = await fetch(`/notes/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete note");
    await loadNotes();
  } catch (err) {
    console.error("❌ Failed to delete note:", err);
  }
}
