/* =====================================================
   KUMBU — script du template statique
   Navigation entre pages, thème clair/sombre, menu mobile
   ===================================================== */

document.addEventListener("DOMContentLoaded", function () {

  /* ---------- Navigation entre pages ---------- */
  var pages = document.querySelectorAll(".page");
  var navLinks = document.querySelectorAll("[data-page]");
  var mainNav = document.getElementById("mainNav");
  var hamburger = document.getElementById("navToggle");

  function showPage(name) {
    pages.forEach(function (page) {
      page.classList.toggle("active", page.id === "page-" + name);
    });
    navLinks.forEach(function (link) {
      link.classList.toggle("active", link.dataset.page === name);
    });
    window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
  }

  navLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      showPage(link.dataset.page);
      if (mainNav && mainNav.classList.contains("open")) {
        closeMobileNav();
      }
    });
  });

  /* Page de départ : on respecte un éventuel #ancre dans l'URL */
  var initial = window.location.hash ? window.location.hash.replace("#", "") : "accueil";
  if (!document.getElementById("page-" + initial)) initial = "accueil";
  showPage(initial);

  /* ---------- Menu mobile (hamburger) ---------- */
  function closeMobileNav() {
    mainNav.classList.remove("open");
    hamburger.classList.remove("open");
    hamburger.setAttribute("aria-expanded", "false");
  }

  if (hamburger && mainNav) {
    hamburger.addEventListener("click", function () {
      var isOpen = mainNav.classList.toggle("open");
      hamburger.classList.toggle("open", isOpen);
      hamburger.setAttribute("aria-expanded", isOpen ? "true" : "false");
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

});
