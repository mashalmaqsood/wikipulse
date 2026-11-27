import { useEffect, useState } from "react";
import type { StreamPayload } from "../types/wikipulse";

const DEFAULT_API_BASE_URL = "http://127.0.0.1:8001";

export type ConnectionStatus = "connecting" | "open" | "error";

interface WikiPulseStreamState {
  status: ConnectionStatus;
  data: StreamPayload | null;
}

export function useWikiPulseStream(): WikiPulseStreamState {
  const [status, setStatus] = useState<ConnectionStatus>("connecting");
  const [data, setData] = useState<StreamPayload | null>(null);

  useEffect(() => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL;
    const source = new EventSource(`${baseUrl}/stream`);

    source.onopen = () => setStatus("open");

    source.onerror = () => {
      setStatus(source.readyState === EventSource.CLOSED ? "error" : "connecting");
    };

    source.onmessage = (event: MessageEvent<string>) => {
      try {
        const parsed = JSON.parse(event.data) as StreamPayload;
        setData(parsed);
        setStatus("open");
      } catch {
        // Malformed packet (e.g. connection dropped mid-write) -- keep
        // showing the last good data instead of crashing the dashboard.
      }
    };

    return () => {
      source.close();
    };
  }, []);

  return { status, data };
}
