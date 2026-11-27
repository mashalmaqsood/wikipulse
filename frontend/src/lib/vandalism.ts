import type { FeedItem } from "../types/wikipulse";

export function isFlagged(item: FeedItem): boolean {
  return item.vandalism !== null && item.vandalism.verdict !== "clean";
}
