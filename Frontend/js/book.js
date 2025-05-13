document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("crearLibroForm");
  
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
  
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Debes iniciar sesión para crear un libro.");
        return;
      }
  
      const newBook = {
        title: document.getElementById("title").value.trim(),
        author: document.getElementById("author").value.trim(),
        description: document.getElementById("description").value.trim(),
        price: parseFloat(document.getElementById("price").value),
        stock: parseInt(document.getElementById("stock").value)
      };
  
      try {
        const response = await fetch("http://localhost:8000/books", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(newBook)
        });
  
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error al crear el libro: ${errorText}`);
        }
  
        alert("✅ Libro creado con éxito");
        form.reset();
      } catch (error) {
        console.error(error);
        alert("❌ " + error.message);
      }
    });
  });
  