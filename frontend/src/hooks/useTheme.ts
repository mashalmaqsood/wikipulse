import { useEffect, useState } from "react";

type ThemeOverride = "light" | "dark" | null;

const STORAGE_KEY = "wikipulse-theme";
const MEDIA_QUERY = "(prefers-color-scheme: dark)";

function readStoredOverride(): ThemeOverride {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored === "light" || stored === "dark" ? stored : null;
  } catch {
    return null;
  }
}

export function useTheme() {
  const [override, setOverride] = useState<ThemeOverride>(() => readStoredOverride());
  const [systemPrefersDark, setSystemPrefersDark] = useState(
    () => window.matchMedia(MEDIA_QUERY).matches,
  );

  useEffect(() => {
    const media = window.matchMedia(MEDIA_QUERY);
    const listener = (event: MediaQueryListEvent) => setSystemPrefersDark(event.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    if (override) {
      root.setAttribute("data-theme", override);
    } else {
      root.removeAttribute("data-theme");
    }
    try {
      if (override) {
        localStorage.setItem(STORAGE_KEY, override);
      } else {
        localStorage.removeItem(STORAGE_KEY);
      }
    } catch {
      // Private browsing / blocked storage -- theme still applies for this session.
    }
  }, [override]);

  const effective: "light" | "dark" = override ?? (systemPrefersDark ? "dark" : "light");
  const toggle = () => setOverride(effective === "dark" ? "light" : "dark");

  return { effective, toggle };
}
