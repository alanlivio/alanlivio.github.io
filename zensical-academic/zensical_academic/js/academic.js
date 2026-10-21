(() => {
  const CACHE_PREFIX = "academic_gh_repo_";
  const CACHE_TTL_MS = 3600 * 1000;

  function updateCard(card, data) {
    if (!data) return;
    if (typeof data.stars === "number") {
      const starSpan = card.querySelector(".repo-stat-stars-val");
      if (starSpan) {
        starSpan.textContent = data.stars;
      }
    }
    if (typeof data.forks === "number") {
      const forkSpan = card.querySelector(".repo-stat-forks-val");
      if (forkSpan) {
        forkSpan.textContent = data.forks;
      }
    }
    if (data.description) {
      const descEl = card.querySelector(".repo-card-new-desc");
      if (descEl && !descEl.textContent.trim()) {
        descEl.textContent = data.description;
      }
    }
  }

  function updateSummaryCounters(cards) {
    let stars = 0;
    let forks = 0;
    cards.forEach((card) => {
      const starSpan = card.querySelector(".repo-stat-stars-val");
      const forkSpan = card.querySelector(".repo-stat-forks-val");
      if (starSpan) {
        stars += parseInt(starSpan.textContent, 10) || 0;
      }
      if (forkSpan) {
        forks += parseInt(forkSpan.textContent, 10) || 0;
      }
    });

    const starsCountEl = document.getElementById("github-stars-count");
    if (starsCountEl) {
      starsCountEl.textContent = stars;
    }
    const forksCountEl = document.getElementById("github-forks-count");
    if (forksCountEl) {
      forksCountEl.textContent = forks;
    }
    const reposCountEl = document.getElementById("github-repos-count");
    if (reposCountEl && (reposCountEl.textContent === "0" || !reposCountEl.textContent)) {
      reposCountEl.textContent = cards.length;
    }
  }

  function initRepoStats() {
    const cards = Array.from(document.querySelectorAll(".repo-card-new[data-repo]"));
    if (cards.length === 0) return;

    updateSummaryCounters(cards);

    const pending = [];

    cards.forEach((card) => {
      const repoName = card.getAttribute("data-repo");
      if (!repoName) return;

      const cacheKey = CACHE_PREFIX + repoName;
      let cached = null;
      try {
        const raw = localStorage.getItem(cacheKey);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Date.now() - parsed.timestamp < CACHE_TTL_MS) {
            cached = parsed.data;
          }
        }
      } catch (err) {
        cached = null;
      }

      if (cached) {
        updateCard(card, cached);
      } else {
        pending.push({ card, repoName, cacheKey });
      }
    });

    if (pending.length === 0) {
      updateSummaryCounters(cards);
      return;
    }

    Promise.all(
      pending.map(async ({ card, repoName, cacheKey }) => {
        try {
          const res = await fetch(`https://api.github.com/repos/${repoName}`, {
            headers: { Accept: "application/vnd.github+json" },
          });
          if (res.ok) {
            const json = await res.json();
            const data = {
              stars: json.stargazers_count ?? 0,
              forks: json.forks_count ?? 0,
              description: json.description || "",
            };
            try {
              localStorage.setItem(
                cacheKey,
                JSON.stringify({ timestamp: Date.now(), data })
              );
            } catch (err) {}
            updateCard(card, data);
          }
        } catch (err) {}
      })
    ).finally(() => {
      updateSummaryCounters(cards);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRepoStats);
  } else {
    initRepoStats();
  }
})();
