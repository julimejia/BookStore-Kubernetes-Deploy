// ====================
// 1. Al cargar la página
// ====================
document.addEventListener("DOMContentLoaded", () => {
  fetchBooks();
});

async function fetchBooks() {
  try {
    const response = await fetch("http://localhost:8000/books/");
    const books = await response.json();

    const container = document.getElementById("libros");
    if (!container) {
      console.error("El contenedor no fue encontrado");
      return;
    }

    container.innerHTML = "";

    if (Array.isArray(books) && books.length > 0) {
      books.forEach(book => {
        const div = document.createElement("div");
        div.classList.add("col-12", "col-md-4", "mb-4");

        div.innerHTML = `
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">${book.title}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${book.author}</h6>
            <p class="card-text">${book.description}</p>
            <p class="card-text"><strong>Precio:</strong> $${book.price.toLocaleString()}</p>
            <p class="card-text"><strong>Stock:</strong> ${book.stock}</p>
            <button class="btn btn-primary mt-2 comprar-btn" data-id="${book.id}" data-price="${book.price}">Comprar</button>
          </div>
        </div>
        `;

        container.appendChild(div);
      });
    } else {
      container.textContent = "No se encontraron libros.";
    }
  } catch (error) {
    console.error("Error al obtener los libros:", error);
  }
}

// ====================
// 2. Modal: Abrir y cargar proveedores
// ====================
document.addEventListener("click", (event) => {
  if (event.target.classList.contains("comprar-btn")) {
    const bookId = event.target.getAttribute("data-id");
    const bookPrice = event.target.getAttribute("data-price");

    const token = localStorage.getItem("token");
    if (!token) {
      alert("Debes iniciar sesión para comprar.");
      return;
    }

    // Redirigir a checkout.html con el ID y precio como parámetros
    window.location.href = `checkout.html?book_id=${bookId}&price=${bookPrice}`;
  }
});