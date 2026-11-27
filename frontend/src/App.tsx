import { useEffect, useMemo, useState } from "react";
import "./App.css";
import { Header } from "./components/Header";
import { LiveFeed } from "./components/LiveFeed";
import { PulseSummaryCard } from "./components/PulseSummaryCard";
import { Sparkline } from "./components/Sparkline";
import { StatTile } from "./components/StatTile";
import { TopPagesList } from "./components/TopPagesList";
import { ALL_WIKIS } from "./components/WikiFilter";
import { useTheme } from "./hooks/useTheme";
import { useWikiPulseStream } from "./hooks/useWikiPulseStream";
import { isFlagged } from "./lib/vandalism";
import type { StreamPayload, WikiStats } from "./types/wikipulse";

const EMPTY_WIKI_STATS: WikiStats = { edits_per_minute: 0, top_pages: [] };
const SPARKLINE_LENGTH = 40;

function App() {
  const { status, data } = useWikiPulseStream();
  const { effective: theme, toggle: toggleTheme } = useTheme();
  const [selectedWiki, setSelectedWiki] = useState<string>(ALL_WIKIS);
  const [history, setHistory] = useState<number[]>([]);
  const [prevWiki, setPrevWiki] = useState(selectedWiki);
  const [prevData, setPrevData] = useState<StreamPayload | null>(null);
  const [summaryUpdatedAt, setSummaryUpdatedAt] = useState<number | null>(null);
  const [prevSummary, setPrevSummary] = useState<string | null>(null);
  const [now, setNow] = useState(() => Date.now());

  const availableWikis = useMemo(
    () => (data ? Object.keys(data.stats.by_wiki).sort() : []),
    [data],
  );

  const activeStats: WikiStats =
    selectedWiki === ALL_WIKIS
      ? (data?.stats.global ?? EMPTY_WIKI_STATS)
      : (data?.stats.by_wiki[selectedWiki] ?? EMPTY_WIKI_STATS);

  // Adjusting state in response to a prop/state change, computed during
  // render against last render's snapshot -- React's recommended
  // alternative to an effect here, since it avoids an extra render pass.
  if (selectedWiki !== prevWiki) {
    setPrevWiki(selectedWiki);
    setHistory([]);
  } else if (data && data !== prevData) {
    setPrevData(data);
    setHistory((h) => [...h, activeStats.edits_per_minute].slice(-SPARKLINE_LENGTH));
  }

  if (data?.summary && data.summary !== prevSummary) {
    setPrevSummary(data.summary);
    setSummaryUpdatedAt(now);
  }

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const scopedFeed = useMemo(() => {
    if (!data) return [];
    return selectedWiki === ALL_WIKIS
      ? data.feed
      : data.feed.filter((item) => item.wiki === selectedWiki);
  }, [data, selectedWiki]);

  const flaggedCount = scopedFeed.filter(isFlagged).length;
  const botCount = scopedFeed.filter((item) => item.bot).length;
  const botShare = scopedFeed.length ? Math.round((botCount / scopedFeed.length) * 100) : 0;
  const distinctWikis = new Set(scopedFeed.map((item) => item.wiki)).size;

  const secondsSinceUpdate = summaryUpdatedAt ? Math.round((now - summaryUpdatedAt) / 1000) : null;
  const isStale = status === "error" || data === null;

  return (
    <div className="dashboard">
      <Header
        wikis={availableWikis}
        selectedWiki={selectedWiki}
        onWikiChange={setSelectedWiki}
        status={status}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <div className={isStale ? "dashboard__live-region dashboard__live-region--stale" : "dashboard__live-region"}>
        <section aria-label="Key figures" className="stats-row">
          <StatTile
            wide
            stale={isStale}
            label="Edits per minute"
            value={activeStats.edits_per_minute.toFixed(1)}
            sublabel={selectedWiki === ALL_WIKIS ? "Across all wikis" : `On ${selectedWiki}`}
            trailing={<Sparkline values={history} />}
          />
          <StatTile label="Flagged in feed" value={String(flaggedCount)} sublabel={`of ${scopedFeed.length} recent edits`} />
          <StatTile label="Bot edits" value={`${botShare}%`} sublabel="share of recent edits" />
          <StatTile label="Wikis in feed" value={String(distinctWikis)} sublabel="distinct editions" />
        </section>

        <div className="dashboard__body">
          <div className="dashboard__main">
            <PulseSummaryCard summary={data?.summary ?? null} secondsSinceUpdate={secondsSinceUpdate} />

            <section className="panel" aria-labelledby="top-h">
              <div className="panel__head">
                <h2 id="top-h">Most-edited pages</h2>
                <span className="panel__hint">Last 5 minutes · edits per page</span>
              </div>
              <TopPagesList pages={activeStats.top_pages} />
            </section>
          </div>

          <LiveFeed items={scopedFeed} />
        </div>
      </div>
    </div>
  );
}

export default App;
