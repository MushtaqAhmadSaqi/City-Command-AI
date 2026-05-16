import { create } from 'zustand';
import { fetchApi } from './api';
import type { Incident } from '../types';

interface IncidentState {
  incidents: Incident[];
  currentIncident: Incident | null;
  aiAnalysis: any | null; // Detailed AI analysis data
  isLoading: boolean;
  error: string | null;

  fetchIncidents: () => Promise<void>;
  fetchIncidentDetail: (id: string) => Promise<void>;
  fetchAiAnalysis: (id: string) => Promise<void>;
  updateStatus: (id: string, status: string) => Promise<void>;
}

export const useIncidentStore = create<IncidentState>((set) => ({
  incidents: [],
  currentIncident: null,
  aiAnalysis: null,
  isLoading: false,
  error: null,

  fetchIncidents: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: Incident[] }>('/incidents');
      set({ incidents: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  fetchIncidentDetail: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: Incident }>(`/incidents/${id}`);
      set({ currentIncident: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  fetchAiAnalysis: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: any }>(`/incidents/${id}/ai-analysis`);
      set({ aiAnalysis: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  updateStatus: async (id: string, status: string) => {
    set({ isLoading: true, error: null });
    try {
      await fetchApi(`/incidents/${id}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      });
      // Refresh current incident after update
      const res = await fetchApi<{ data: Incident }>(`/incidents/${id}`);
      set({ currentIncident: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },
}));
