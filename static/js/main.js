// /static/js/main.js

import { loadNotes, createNote, deleteNote, updateNote } from "./notes.js";

// Expose deleteNote globally so inline button onclick can use it
window.deleteNote = deleteNote;
window.updateNote = updateNote;

document.addEventListener("DOMContentLoaded", () => {
  loadNotes();

  const form = document.getElementById("noteForm");
  form.addEventListener("submit", async e => {
    e.preventDefault();

    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!title) {
      alert("Title required!");
      return;
    }

    await createNote(title, content);
    form.reset();
  });
});
