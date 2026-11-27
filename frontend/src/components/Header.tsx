import { ALL_WIKIS, WikiFilter } from "./WikiFilter";
import { ConnectionBadge } from "./ConnectionBadge";
import { ThemeToggle } from "./ThemeToggle";
import type { ConnectionStatus } from "../hooks/useWikiPulseStream";

interface HeaderProps {
  wikis: string[];
  selectedWiki: string;
  onWikiChange: (wiki: string) => void;
  status: ConnectionStatus;
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

export function Header({ wikis, selectedWiki, onWikiChange, status, theme, onToggleTheme }: HeaderProps) {
  return (
    <header className="header">
      <div className="header__brand">
        <div className="header__logo">
          <svg width="32" height="32" viewBox="0 0 32 32" aria-hidden="true">
            <rect x="0" y="0" width="32" height="32" rx="9" fill="var(--accent-soft)" />
            <polyline
              points="6,17 11,17 13.5,10 17.5,23 20.5,14 26,14"
              fill="none"
              stroke="var(--accent)"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="header__name">WikiPulse</span>
        </div>
        <span className="header__divider" aria-hidden="true" />
        <span className="header__tagline">Real-time edits across all Wikipedia language editions</span>
      </div>
      <div className="header__controls">
        <WikiFilter wikis={wikis.filter((w) => w !== ALL_WIKIS)} selected={selectedWiki} onChange={onWikiChange} />
        <span className="header__divider" aria-hidden="true" />
        <ConnectionBadge status={status} />
        <ThemeToggle effective={theme} onToggle={onToggleTheme} />
      </div>
    </header>
  );
}
