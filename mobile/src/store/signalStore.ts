import { create } from 'zustand';
import { fetchApi } from './api';
import type { Signal } from '../types';

interface SignalState {
  signals: Signal[];
  isLoading: boolean;
  error: string | null;
  submitSignal: (text: string, lat: number, lng: number) => Promise<void>;
  fetchSignals: () => Promise<void>;
}

export const useSignalStore = create<SignalState>((set) => ({
  signals: [],
  isLoading: false,
  error: null,

  submitSignal: async (text: string, lat: number, lng: number) => {
    set({ isLoading: true, error: null });
    try {
      await fetchApi('/signals', {
        method: 'POST',
        body: JSON.stringify({ raw_text: text, lat, lng, source_type: 'field' }),
      });
      // Refresh list
      const res = await fetchApi<{ data: Signal[] }>('/signals');
      set({ signals: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  fetchSignals: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: Signal[] }>('/signals');
      set({ signals: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },
}));
