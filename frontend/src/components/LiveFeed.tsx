import { Bot, Pause, Play, User } from "lucide-react";
import { useState } from "react";
import type { FeedItem } from "../types/wikipulse";
import { isFlagged } from "../lib/vandalism";
import { VandalismBadge } from "./VandalismBadge";

function formatDelta(delta: number | null): string {
  if (delta === null) return "";
  return delta > 0 ? `+${delta.toLocaleString()}` : delta.toLocaleString();
}

export function LiveFeed({ items }: { items: FeedItem[] }) {
  const [paused, setPaused] = useState(false);
  const [prevPaused, setPrevPaused] = useState(paused);
  const [filter, setFilter] = useState<"all" | "flagged">("all");
  const [frozen, setFrozen] = useState<FeedItem[] | null>(null);

  // Capture the feed the instant "paused" flips on, during render against
  // last render's snapshot, rather than in an effect -- avoids an extra
  // render pass for what is otherwise just reacting to a prop/state change.
  if (paused !== prevPaused) {
    setPrevPaused(paused);
    setFrozen(paused ? items : null);
  }

  const displayed = paused && frozen !== null ? frozen : items;
  const waitingCount = paused && frozen !== null ? Math.max(0, items.length - frozen.length) : 0;
  const visible = filter === "all" ? displayed : displayed.filter(isFlagged);
  const flaggedCount = displayed.filter(isFlagged).length;

  return (
    <section className="panel panel--feed" aria-labelledby="feed-h">
      <div className="feed__head">
        <div className="feed__heading">
          <h2 id="feed-h">Live feed</h2>
          <span className="feed__hint">Newest first</span>
        </div>
        <button
          type="button"
          className="feed__pause-btn"
          onClick={() => setPaused((p) => !p)}
          aria-pressed={paused}
        >
          {paused ? <Play size={12} /> : <Pause size={12} />}
          {paused ? "Resume" : "Pause"}
        </button>
      </div>

      <div className="feed__tabs" role="group" aria-label="Feed filter">
        <button
          type="button"
          className={`feed__tab${filter === "all" ? " feed__tab--active" : ""}`}
          aria-pressed={filter === "all"}
          onClick={() => setFilter("all")}
        >
          All edits
        </button>
        <button
          type="button"
          className={`feed__tab${filter === "flagged" ? " feed__tab--active" : ""}`}
          aria-pressed={filter === "flagged"}
          onClick={() => setFilter("flagged")}
        >
          Flagged · {flaggedCount}
        </button>
      </div>

      {paused && (
        <div className="feed__paused-banner">
          <span>Feed paused{waitingCount > 0 ? ` · ${waitingCount} new edits waiting` : ""}</span>
          <button type="button" onClick={() => setPaused(false)}>
            Show them
          </button>
        </div>
      )}

      <ol className="live-feed">
        {visible.length === 0 && (
          <li className="empty-state empty-state--feed">
            No edits match this filter yet. New edits will appear here as they arrive.
          </li>
        )}
        {visible.map((item, index) => (
          <li key={index} className="live-feed__item">
            <div className="live-feed__row">
              <span className="live-feed__title">{item.title}</span>
              <span className={`live-feed__delta ${item.length_delta !== null && item.length_delta < 0 ? "delta--negative" : "delta--positive"}`}>
                {formatDelta(item.length_delta)}
              </span>
            </div>
            <div className="live-feed__row live-feed__row--meta">
              <span className="live-feed__wiki-tag">{item.wiki}</span>
              <span className="live-feed__user">
                <User size={12} />
                {item.user}
              </span>
              {item.bot && (
                <span className="live-feed__bot-tag">
                  <Bot size={12} />
                  Bot
                </span>
              )}
            </div>
            {item.comment && <p className="live-feed__comment">{item.comment}</p>}
            <VandalismBadge vandalism={item.vandalism} />
          </li>
        ))}
      </ol>

      <div className="feed__footer">
        <span>Keeping the latest {items.length > 0 ? items.length : 50} edits</span>
        <span>AI checks run on suspicious edits only</span>
      </div>
    </section>
  );
}
