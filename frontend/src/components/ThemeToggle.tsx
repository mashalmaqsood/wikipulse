import { Moon, Sun } from "lucide-react";

interface ThemeToggleProps {
  effective: "light" | "dark";
  onToggle: () => void;
}

export function ThemeToggle({ effective, onToggle }: ThemeToggleProps) {
  const next = effective === "dark" ? "light" : "dark";

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={onToggle}
      aria-label={`Switch to ${next} mode`}
      title={`Switch to ${next} mode`}
    >
      {effective === "dark" ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  );
}
