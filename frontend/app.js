// Conecta el formulario de login con el backend Flask (/api/*)
// La página se sirve desde Flask: la dirección es la misma desde la que se abrió
// (localhost en el computador, 10.0.2.2 en el emulador, la IP del computador en el celular).
const SERVER = location.origin;
const form = document.getElementById("auth-form");
const title = document.getElementById("form-title");
const nameInput = document.getElementById("name");
const submitBtn = document.getElementById("submit-btn");
const toggleBtn = document.getElementById("toggle-mode");
const toggleText = document.getElementById("toggle-text");
const msg = document.getElementById("message");
const pwd = document.getElementById("password");
const eye = document.getElementById("toggle-password");
const googleBtn = document.getElementById("google-btn");
const googleFallback = document.getElementById("google-fallback");
const themeBtn = document.getElementById("theme");
let mode = "login";
function showMessage(text, ok) {
    msg.textContent = text;
    msg.className = "text-sm " + (ok ? "text-green-600" : "text-red-600");
}
const SERVER_DOWN =
    "El servidor no está corriendo. Abre una terminal en la carpeta backend y ejecuta: python app.py";
// 1) La página debe abrirse desde el servidor Flask (http://localhost:5000).
// Si se abrió con doble clic (file://) o con Live Server, redirigimos allí.
if (location.protocol === "file:") {
    fetch("http://localhost:5000/api/health", { mode: "no-cors" })
        .then(() => { location.href = "http://localhost:5000/"; })
        .catch(() => showMessage(SERVER_DOWN, false));
} else {
    init();
}
function init() {
    // Si ya hay sesión activa, ir directo al home
    fetch("/api/me").then(r => { if (r.ok) location.href = "/home"; }).catch(() => { });
    setupGoogle();
}
function setMode(newMode) {
    mode = newMode;
    const reg = mode === "register";
    title.textContent = reg ? "Crear cuenta" : "Iniciar sesión";
    submitBtn.textContent = reg ? "Crear cuenta" : "Ingresar";
    nameInput.closest("label").classList.toggle("hidden", !reg);
    pwd.autocomplete = reg ? "new-password" : "current-password";
    toggleText.textContent = reg ? "¿Ya tienes cuenta?" : "¿No tienes cuenta?";
    toggleBtn.textContent = reg ? "Inicia sesión" : "Regístrate";
    msg.textContent = "";
}
toggleBtn.addEventListener("click", () => setMode(mode === "login" ? "register" : "login"));
eye.addEventListener("click", () => { pwd.type = pwd.type === "password" ? "text" : "password"; });
themeBtn.addEventListener("click", () => document.documentElement.classList.toggle("dark"));
async function postJSON(url, body) {
    let res;
    try {
        res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
    } catch {
        throw new Error(SERVER_DOWN);
    }
    let data;
    try { data = await res.json(); } catch {
        throw new Error(`Respuesta inesperada del servidor (${res.status}). Reinicia python app.py`);
    }
    if (!res.ok) throw new Error(data.error || "Error");
    return data;
}
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const data = await postJSON(`/api/${mode}`, {
            email: form.email.value,
            password: form.password.value,
            name: nameInput.value,
        });
        showMessage(`${data.message}. Redirigiendo...`, true);
        location.href = "/home";
    } catch (err) {
        showMessage(err.message, false);
    }
});
// ---------------------------------------------------------------- Google
async function setupGoogle() {
    let clientId = "";
    try {
        clientId = (await (await fetch("/api/config")).json()).google_client_id;
    } catch { }
    if (!clientId) {
        googleFallback.addEventListener("click", () =>
            showMessage("Google no está configurado. Añade GOOGLE_CLIENT_ID en backend/config.py y reinicia el servidor.", false)
        );
        return;
    }
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.onerror = () => showMessage("No se pudo cargar el inicio de sesión de Google.", false);
    script.onload = () => {
        google.accounts.id.initialize({ client_id: clientId, callback: onGoogleCredential });
        google.accounts.id.renderButton(googleBtn, {
            theme: "outline", size: "large", shape: "pill", text: "signin_with", width: googleFallback.offsetWidth || 240,
        });
        googleFallback.classList.add("hidden");
        googleBtn.classList.remove("hidden");
    };
    document.head.appendChild(script);
}

async function onGoogleCredential(response) {
    try {
        const data = await postJSON("/api/google", { credential: response.credential });
        showMessage(`${data.message}. Redirigiendo...`, true);
        location.href = "/home";
    } catch (err) {
        showMessage(err.message, false);
    }
}