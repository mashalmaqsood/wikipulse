import type { ReactNode } from "react";

interface StatTileProps {
  label: string;
  value: string;
  sublabel?: string;
  trailing?: ReactNode;
  wide?: boolean;
  stale?: boolean;
}

export function StatTile({ label, value, sublabel, trailing, wide, stale }: StatTileProps) {
  return (
    <div className={`stat-tile${wide ? " stat-tile--wide" : ""}`}>
      <div className="stat-tile__main">
        <span className="stat-tile__label">{label}</span>
        <span className={`stat-tile__value${stale ? " stat-tile__value--stale" : ""}`}>{value}</span>
        {sublabel && <span className="stat-tile__sublabel">{sublabel}</span>}
      </div>
      {trailing && <div className="stat-tile__trailing">{trailing}</div>}
    </div>
  );
}
