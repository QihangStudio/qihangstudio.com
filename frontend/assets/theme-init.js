    (() => {
      const STORAGE_KEY = "qihangstudio-theme";
      let preference = "system";
      try {
        preference = localStorage.getItem(STORAGE_KEY) || "system";
      } catch (_) {}
      const systemDark =
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
      const resolved =
        preference === "system"
          ? (systemDark ? "dark" : "light")
          : preference;
      document.documentElement.dataset.theme = resolved;
      document.documentElement.dataset.themePreference = preference;
    })();
