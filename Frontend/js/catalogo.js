async function fetchBooks() {
  const res = await fetch('http://localhost:8001/books');  // Solicitar libros sin necesidad de token

  if (res.ok) {
    const books = await res.json();
    const booksList = document.getElementById("books-list");

    books.forEach(book => {
      const listItem = document.createElement("li");
      listItem.className = "list-group-item";
      listItem.innerText = `${book.title} by ${book.author}`;
      booksList.appendChild(listItem);
    });
  } else {
    alert("Could not load the catalog");
  }
}

fetchBooks();
