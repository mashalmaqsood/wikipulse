export interface TopPage {
  title: string;
  count: number;
}

export interface WikiStats {
  edits_per_minute: number;
  top_pages: TopPage[];
}

export interface Stats {
  global: WikiStats;
  by_wiki: Record<string, WikiStats>;
}

export interface VandalismVerdict {
  verdict: "vandalism" | "clean" | "uncertain";
  reason: string;
}

export interface FeedItem {
  type: string;
  title: string;
  wiki: string;
  user: string;
  bot: boolean;
  comment: string;
  length_delta: number | null;
  vandalism: VandalismVerdict | null;
}

export interface StreamPayload {
  stats: Stats;
  feed: FeedItem[];
  summary: string | null;
}
