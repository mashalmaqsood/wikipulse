import type { VandalismVerdict } from "../types/wikipulse";

const LABELS: Record<VandalismVerdict["verdict"], string> = {
  vandalism: "Likely vandalism",
  uncertain: "Needs review",
  clean: "Checked, clean",
};

export function VandalismBadge({ vandalism }: { vandalism: VandalismVerdict | null }) {
  if (vandalism === null) {
    return null;
  }

  return (
    <div className={`flag-box flag-box--${vandalism.verdict}`}>
      <span className="flag-box__label">
        <span className="flag-box__dot" aria-hidden="true" />
        {LABELS[vandalism.verdict]}
      </span>
      <span className="flag-box__reason">{vandalism.reason}</span>
    </div>
  );
}
