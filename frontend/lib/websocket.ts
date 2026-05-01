const WS_URL =
  process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000/api/v1/observability/ws";

export function createExecutionSocket(executionId: string) {
  return new WebSocket(`${WS_URL}/${executionId}`);
}
