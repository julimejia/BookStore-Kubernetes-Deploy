function renderNavbar() {
  const nav = document.getElementById("nav-links");
  nav.innerHTML = "";

  const token = localStorage.getItem("token");

  if (token) {
    nav.innerHTML += `
      <li class="nav-item">
        <a class="nav-link" href="#">Mis Libros</a>
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
  localStorage.removeItem("token");
  window.location.href = "login.html";
}
