import type { ConnectionStatus } from "../hooks/useWikiPulseStream";

const LABELS: Record<ConnectionStatus, string> = {
  connecting: "Connecting…",
  open: "Live",
  error: "Disconnected",
};

export function ConnectionBadge({ status }: { status: ConnectionStatus }) {
  return (
    <span className={`connection-badge connection-badge--${status}`} role="status">
      <span className="connection-badge__dot" aria-hidden="true" />
      <span className="connection-badge__label">{LABELS[status]}</span>
    </span>
  );
}
