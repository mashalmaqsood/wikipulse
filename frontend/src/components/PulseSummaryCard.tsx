interface PulseSummaryCardProps {
  summary: string | null;
  secondsSinceUpdate: number | null;
}

export function PulseSummaryCard({ summary, secondsSinceUpdate }: PulseSummaryCardProps) {
  return (
    <section className="panel pulse-summary" aria-labelledby="pulse-h">
      <div className="pulse-summary__head">
        <div className="pulse-summary__title">
          <h2 id="pulse-h">Pulse summary</h2>
          <span className="ai-badge">AI-generated</span>
        </div>
        {secondsSinceUpdate !== null && (
          <span className="pulse-summary__meta">Written {secondsSinceUpdate}s ago</span>
        )}
      </div>
      {summary === null ? (
        <div className="skeleton-lines" aria-label="Generating summary">
          <span className="skeleton-line" style={{ width: "92%" }} />
          <span className="skeleton-line" style={{ width: "84%" }} />
          <span className="skeleton-line" style={{ width: "58%" }} />
        </div>
      ) : (
        <p>{summary}</p>
      )}
    </section>
  );
}
