import { create } from 'zustand';
import { fetchApi } from './api';
import type { AgentTrace } from '../types';

interface TraceState {
  traces: AgentTrace[];
  isLoading: boolean;
  error: string | null;

  fetchTraces: (incidentId?: string) => Promise<void>;
}

export const useTraceStore = create<TraceState>((set) => ({
  traces: [],
  isLoading: false,
  error: null,

  fetchTraces: async (incidentId?: string) => {
    set({ isLoading: true, error: null });
    try {
      const endpoint = incidentId ? `/traces?incident_id=${incidentId}` : '/traces';
      const res = await fetchApi<{ data: AgentTrace[] }>(endpoint);
      set({ traces: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  }
}));
