// Envia o token CSRF (da <meta name="csrf-token">) no cabeçalho X-CSRFToken
// de toda requisição feita pelo HTMX. O Flask-WTF aceita esse cabeçalho.
document.addEventListener("htmx:configRequest", function (evento) {
  var meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) {
    evento.detail.headers["X-CSRFToken"] = meta.content;
  }
});
