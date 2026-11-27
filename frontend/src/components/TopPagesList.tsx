import type { TopPage } from "../types/wikipulse";

export function TopPagesList({ pages }: { pages: TopPage[] }) {
  if (pages.length === 0) {
    return <p className="empty-state">No edits recorded in this window yet.</p>;
  }

  const max = pages[0].count || 1;

  return (
    <ol className="top-pages">
      {pages.map((page, index) => (
        <li key={page.title} className="top-pages__row" title={page.title}>
          <span className="top-pages__rank">{index + 1}</span>
          <span className="top-pages__title">{page.title}</span>
          <span className="top-pages__track">
            <span
              className={`top-pages__fill${index === 0 ? " top-pages__fill--lead" : ""}`}
              style={{ width: `${Math.round((page.count / max) * 100)}%` }}
            />
          </span>
          <span className="top-pages__count">{page.count}</span>
        </li>
      ))}
    </ol>
  );
}
