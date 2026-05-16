import { create } from 'zustand';
import { fetchApi } from './api';
import { useIncidentStore } from './incidentStore';

interface DemoState {
  isGenerating: boolean;
  error: string | null;
  triggerDemoScenario: () => Promise<void>;
}

export const useDemoStore = create<DemoState>((set) => ({
  isGenerating: false,
  error: null,

  triggerDemoScenario: async () => {
    set({ isGenerating: true, error: null });
    try {
      await fetchApi('/demo/run-scenario', { method: 'POST' });
      // Refresh incidents after demo run
      await useIncidentStore.getState().fetchIncidents();
      set({ isGenerating: false });
    } catch (err: any) {
      set({ error: err.message, isGenerating: false });
    }
  }
}));
