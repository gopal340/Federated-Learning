import type { ChatResponse, ModelInfo, JevArtifactDetails } from './types';

const API_BASE = 'http://localhost:8000';
const WS_BASE = 'ws://localhost:8000';

export async function checkBackendHealth(): Promise<{ status: string; models_loaded: boolean; device: string }> {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch {
    return { status: 'offline', models_loaded: false, device: 'unknown' };
  }
}

export async function getModelInfo(): Promise<ModelInfo | null> {
  try {
    const res = await fetch(`${API_BASE}/api/model-info`);
    if (!res.ok) throw new Error('Failed to fetch model info');
    return await res.json();
  } catch (err) {
    console.error('Error fetching model info:', err);
    return null;
  }
}

export async function getJevArtifacts(): Promise<JevArtifactDetails | null> {
  try {
    const res = await fetch(`${API_BASE}/api/jev/artifacts`);
    if (!res.ok) throw new Error('Failed to fetch JEV artifacts');
    return await res.json();
  } catch (err) {
    console.error('Error fetching JEV artifacts:', err);
    return null;
  }
}

export async function sendChatDecision(question: string, context?: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, context }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Inference request failed (${res.status}): ${errorText}`);
  }

  return await res.json();
}

export function createInferenceWebSocket(
  onMessage: (msg: any) => void,
  onError?: (err: any) => void
): WebSocket | null {
  try {
    const ws = new WebSocket(`${WS_BASE}/ws/inference`);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.error('Failed to parse WS message:', e);
      }
    };
    ws.onerror = (err) => {
      console.warn('WebSocket error:', err);
      if (onError) onError(err);
    };
    return ws;
  } catch (e) {
    console.warn('WebSocket connection error:', e);
    return null;
  }
}
