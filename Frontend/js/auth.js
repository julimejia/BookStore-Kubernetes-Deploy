function renderNavbar() {
  const nav = document.getElementById("nav-links");
  nav.innerHTML = "";

  const token = localStorage.getItem("token");

  if (token) {
    nav.innerHTML += `
      <li class="nav-item">
        <a class="nav-link" href="#" id="mis-libros-btn">Mis Libros</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#" onclick="logout()">Cerrar Sesión</a>
      </li>
    `;
  } else {
    nav.innerHTML += `
      <li class="nav-item">
        <a class="nav-link" href="login.html">Login</a>
      </li>
    `;
  }
}

function logout() {
  localStorage.removeItem("token"); // Elimina el token
  renderNavbar(); // Actualiza el navbar
  window.location.href = "index.html"; // Redirige al usuario (opcional)
}
