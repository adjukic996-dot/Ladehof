/* ============================================================================
   Ladehof — Bewegung
   Faehrt, was CSS nicht kann. Alle Dauern und Kurven stehen im Stylesheet,
   damit es genau eine Quelle fuer die Werte gibt. Siehe DESIGN.md 4.
   ========================================================================== */
(() => {
  "use strict";
  const sparsam = matchMedia("(prefers-reduced-motion: reduce)");

  /* -- 1. Einblenden ------------------------------------------------------
     Gemessen an der Vorlage: eine reine Opazitaetsblende ueber 400 ms.
     Kein Versatz, kein Kippen. Die Varianten "hoch" und "schwung" nehmen
     zusaetzlich einen transform mit — ebenfalls gemessen. */
  const einblenden = () => {
    const stuecke = document.querySelectorAll("[data-ein], [data-balken]");
    if (!stuecke.length) return;
    if (sparsam.matches) { stuecke.forEach(e => e.classList.add("da")); return; }

    const beobachter = new IntersectionObserver((eintraege) => {
      for (const e of eintraege) {
        if (!e.isIntersecting) continue;
        e.target.classList.add("da");
        beobachter.unobserve(e.target);
      }
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });

    stuecke.forEach(e => beobachter.observe(e));

    /* Zwei Netze darunter. Die ganze Seitenschrift startet auf Opazitaet 0 —
       loest der Beobachter nicht aus, bleibt die Seite leer. Das darf nicht
       an einem einzigen Ausloeser haengen.

       Netz 1: Was beim Laden ohnehin im Bild steht, wird sofort gezeigt.
       Netz 2: Hat nach 2,5 s gar nichts ausgeloest, war der Beobachter
       wirkungslos — dann faellt alles sichtbar. Lieber ohne Bewegung lesbar
       als mit Bewegung unsichtbar. */
    const zeigeSichtbare = () => {
      for (const el of stuecke) {
        if (el.classList.contains("da")) continue;
        const r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0) {
          el.classList.add("da");
          beobachter.unobserve(el);
        }
      }
    };
    requestAnimationFrame(zeigeSichtbare);

    setTimeout(() => {
      if ([...stuecke].some(el => el.classList.contains("da"))) return;
      stuecke.forEach(el => { el.classList.add("da"); beobachter.unobserve(el); });
    }, 2500);
  };

  /* -- 2. Handymenue ----------------------------------------------------- */
  const menue = () => {
    const brenner = document.querySelector(".brenner");
    const blende  = document.querySelector(".blende");
    if (!brenner || !blende) return;

    const setze = (auf) => {
      blende.dataset.auf = auf ? "ja" : "nein";
      brenner.setAttribute("aria-expanded", String(auf));
      document.documentElement.style.overflow = auf ? "hidden" : "";
    };

    setze(false);
    brenner.addEventListener("click", () => setze(blende.dataset.auf !== "ja"));
    blende.querySelectorAll("a").forEach(a => a.addEventListener("click", () => setze(false)));
    addEventListener("keydown", (ev) => { if (ev.key === "Escape") setze(false); });
    matchMedia("(min-width:1000px)").addEventListener("change", (m) => {
      if (m.matches) setze(false);
    });
  };

  /* -- 3. Reiterleiste ----------------------------------------------------
     Reiterwechsel ist ein Zustandswechsel: gemessene 300 ms, kein erneutes
     Einblenden des Feldes. */
  const reiter = () => {
    for (const leiste of document.querySelectorAll('[role="tablist"]')) {
      const knoepfe = [...leiste.querySelectorAll('[role="tab"]')];
      if (!knoepfe.length) continue;

      const zeige = (ziel) => {
        for (const k of knoepfe) {
          const an = k === ziel;
          k.setAttribute("aria-selected", String(an));
          k.tabIndex = an ? 0 : -1;
          const feld = document.getElementById(k.getAttribute("aria-controls"));
          if (feld) { feld.hidden = !an; if (an) feld.classList.add("da"); }
        }
      };
      zeige(knoepfe.find(k => k.getAttribute("aria-selected") === "true") || knoepfe[0]);

      knoepfe.forEach((k, i) => {
        k.addEventListener("click", () => zeige(k));
        k.addEventListener("keydown", (ev) => {
          const schritt = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
          if (!schritt) return;
          ev.preventDefault();
          const n = knoepfe[(i + schritt + knoepfe.length) % knoepfe.length];
          zeige(n); n.focus();
        });
      });
    }
  };

  /* -- 4. Klapplisten -----------------------------------------------------
     Die Hoehe muss in Pixeln laufen, `auto` laesst sich nicht uebergehen. */
  const klappen = () => {
    const dauer = 300;
    document.querySelectorAll(".klappe").forEach((kl) => {
      const kopf = kl.querySelector(".klappe__kopf");
      const koerper = kl.querySelector(".klappe__koerper");
      if (!kopf || !koerper) return;

      const id = koerper.id || "k" + Math.random().toString(36).slice(2, 8);
      koerper.id = id;
      kopf.setAttribute("aria-controls", id);

      const setze = (auf) => {
        kl.dataset.auf = auf ? "ja" : "nein";
        kopf.setAttribute("aria-expanded", String(auf));
        if (sparsam.matches) { koerper.style.height = auf ? "auto" : "0px"; return; }
        if (auf) {
          koerper.style.height = koerper.scrollHeight + "px";
          setTimeout(() => { if (kl.dataset.auf === "ja") koerper.style.height = "auto"; }, dauer);
        } else {
          koerper.style.height = koerper.scrollHeight + "px";
          requestAnimationFrame(() => { koerper.style.height = "0px"; });
        }
      };
      setze(false);
      kopf.addEventListener("click", () => setze(kl.dataset.auf !== "ja"));
    });
  };

  /* -- 5. Karussell -------------------------------------------------------
     Gemessen: transform und opacity ueber 1000 ms, ease. */
  const karussell = () => {
    document.querySelectorAll("[data-karussell]").forEach((kar) => {
      const spur = kar.querySelector(".karussell__spur");
      const folien = [...kar.querySelectorAll(".karussell__folie")];
      const punkte = [...kar.querySelectorAll(".karussell__punkt")];
      if (folien.length < 2) return;

      const zeige = (n) => {
        spur.style.transform = `translateX(-${n * 100}%)`;
        folien.forEach((f, i) => f.setAttribute("aria-hidden", String(i !== n)));
        punkte.forEach((p, i) => p.setAttribute("aria-current", String(i === n)));
      };
      zeige(0);
      punkte.forEach((p, i) => p.addEventListener("click", () => zeige(i)));
    });
  };

  const los = () => { einblenden(); menue(); reiter(); klappen(); karussell(); };
  if (document.readyState === "loading") addEventListener("DOMContentLoaded", los);
  else los();
})();
