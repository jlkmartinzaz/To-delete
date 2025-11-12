const API_BASE = "/";

async function login() {
  const email = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(API_BASE + "auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (res.ok) {
    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    document.getElementById("login-section").classList.add("hidden");
    document.getElementById("main-section").classList.remove("hidden");
    loadCats();
  } else {
    document.getElementById("login-error").textContent = "Usuario o contraseña incorrectos";
  }
}
