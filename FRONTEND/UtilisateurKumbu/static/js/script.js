/* =====================================================
   KUMBU — script du template statique
   Thème clair/sombre, menu mobile, onglets, assistant IA
   ===================================================== */

document.addEventListener("DOMContentLoaded", function () {

  /* ---------- Menu mobile (hamburger) ---------- */
  var mainNav = document.getElementById("mainNav");
  var hamburger = document.getElementById("navToggle");

  if (hamburger && mainNav) {
    function closeMenu() {
      mainNav.classList.remove("open");
      hamburger.classList.remove("open");
      hamburger.setAttribute("aria-expanded", "false");
    }

    hamburger.addEventListener("click", function () {
      var isOpen = mainNav.classList.toggle("open");
      hamburger.classList.toggle("open", isOpen);
      hamburger.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    // Fermer proprement le menu après avoir choisi une page.
    mainNav.querySelectorAll(".nav-link, .nav-utils a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });

    // Fermer avec Échap.
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
  }

  /* ---------- Thème clair / sombre ---------- */
  var root = document.documentElement;
  var themeToggle = document.getElementById("themeToggle");
  var savedTheme = null;
  try { savedTheme = localStorage.getItem("kumbu-theme"); } catch (err) {}

  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.setAttribute("data-theme", savedTheme || (prefersDark ? "dark" : "light"));

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("kumbu-theme", next); } catch (err) {}
    });
  }

  /* ---------- Onglets connexion / inscription ---------- */
  var authTabs = document.querySelectorAll(".auth-tab");
  var authForms = document.querySelectorAll(".auth-form");

  authTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var target = tab.dataset.form;
      authTabs.forEach(function (t) { t.classList.toggle("active", t === tab); });
      authForms.forEach(function (form) {
        form.classList.toggle("active", form.id === "form-" + target);
      });
    });
  });

  /* ---------- Onglets secondaires (page profil) ---------- */
  var profileTabs = document.querySelectorAll(".tabs-secondary span");
  profileTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      profileTabs.forEach(function (t) { t.classList.remove("active"); });
      tab.classList.add("active");
      /* Le contenu réel de chaque onglet sera branché côté Django (vues/contexte) */
    });
  });

  /* ---------- Exemple d'envoi de message pour l'assistant IA ---------- */
  var chatForm = document.getElementById("chatForm");
  var chatWindow = document.getElementById("chatWindow");
  if (chatForm && chatWindow) {
    chatForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = chatForm.querySelector("input");
      var text = input.value.trim();
      if (!text) return;

      var userMsg = document.createElement("div");
      userMsg.className = "msg msg-user";
      userMsg.textContent = text;
      chatWindow.appendChild(userMsg);

      input.value = "";
      chatWindow.scrollTop = chatWindow.scrollHeight;

      /* Ceci est un espace réservé — brancher ici l'appel réel à l'IA côté Django */
      var botMsg = document.createElement("div");
      botMsg.className = "msg msg-bot";
      botMsg.textContent = "Réponse de l'assistant Kumbu à connecter côté serveur.";
      setTimeout(function () {
        chatWindow.appendChild(botMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }, 300);
    });
  }
  /* ---------- Connexion avec Google ---------- */
  var googleLogin = document.getElementById("google-login");
  var googleError = document.getElementById("google-error");

  if (googleLogin) {
    googleLogin.addEventListener("click", async function () {

      googleLogin.disabled = true;
      googleLogin.style.opacity = "0.7";

      if (googleError) {
        googleError.style.display = "none";
        googleError.textContent = "";
      }

      try {
        const { auth, provider, signInWithPopup } = window.kumbuFirebase;

        const result = await signInWithPopup(auth, provider);

        const idToken = await result.user.getIdToken();

        const response = await fetch("/connexion/google/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: JSON.stringify({
            id_token: idToken
          })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(data.error || "La connexion a échoué.");
        }

        window.location.href = data.redirect_url;

      } catch (error) {

        console.error("Connexion Google :", error);

        if (googleError) {
          googleError.textContent =
            error.message || "Impossible de se connecter avec Google.";
          googleError.style.display = "block";
        }

      } finally {
        googleLogin.disabled = false;
        googleLogin.style.opacity = "1";
      }
    });
  }

  /* ---------- Récupération du cookie CSRF Django ---------- */
  function getCookie(name) {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === name + "=") {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }

    return null;
  }
});
