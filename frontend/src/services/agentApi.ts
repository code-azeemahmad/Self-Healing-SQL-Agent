import type { AgentEvent } from "../types/agent";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

interface StreamCallbacks {
  onEvent: (event: AgentEvent) => void;
  onError: (error: Error) => void;
}

export async function streamAgentQuery(
  query: string,
  callbacks: StreamCallbacks,
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/agent/query/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      `Agent request failed with status ${response.status}.`,
    );
  }

  if (!response.body) {
    throw new Error(
      "The server returned an empty streaming response.",
    );
  }

  const reader = response.body
    .pipeThrough(new TextDecoderStream())
    .getReader();

  let buffer = "";

  try {
    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        break;
      }

      buffer += value;

      const events = buffer.split("\n\n");

      buffer = events.pop() ?? "";

      for (const rawEvent of events) {
        const parsed = parseSSEEvent(rawEvent);

        if (parsed) {
          callbacks.onEvent(parsed);
        }
      }
    }

    if (buffer.trim()) {
      const parsed = parseSSEEvent(buffer);

      if (parsed) {
        callbacks.onEvent(parsed);
      }
    }
  } catch (error) {
    const normalizedError =
      error instanceof Error
        ? error
        : new Error("Unknown SSE streaming error.");

    callbacks.onError(normalizedError);

    throw normalizedError;
  } finally {
    reader.releaseLock();
  }
}

function parseSSEEvent(rawEvent: string): AgentEvent | null {
  const lines = rawEvent.split("\n");

  let eventName = "";
  let data = "";

  for (const line of lines) {
    if (line.startsWith("event:")) {
      eventName = line.slice(6).trim();
    }

    if (line.startsWith("data:")) {
      data += line.slice(5).trim();
    }
  }

  if (!data) {
    return null;
  }

  const parsed = JSON.parse(data) as AgentEvent;

  return {
    ...parsed,
    event: parsed.event || eventName,
  };
}
