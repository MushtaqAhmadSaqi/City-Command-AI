import { create } from 'zustand';
import { fetchApi } from './api';
import type { Resource, ResourceAssignment } from '../types';

interface ResourceState {
  resources: Resource[];
  assignments: ResourceAssignment[];
  isLoading: boolean;
  error: string | null;

  fetchResources: () => Promise<void>;
  fetchAssignments: (incidentId: string) => Promise<void>;
  allocateResources: (incidentIds: string[]) => Promise<void>;
  releaseResource: (resourceId: string) => Promise<void>;
}

export const useResourceStore = create<ResourceState>((set) => ({
  resources: [],
  assignments: [],
  isLoading: false,
  error: null,

  fetchResources: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: Resource[] }>('/resources');
      set({ resources: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  fetchAssignments: async (incidentId: string) => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: ResourceAssignment[] }>(`/resources/assignments/${incidentId}`);
      set({ assignments: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  allocateResources: async (incidentIds: string[]) => {
    set({ isLoading: true, error: null });
    try {
      await fetchApi('/resources/allocate', {
        method: 'POST',
        body: JSON.stringify({ incident_ids: incidentIds }),
      });
      // Refresh resources
      const res = await fetchApi<{ data: Resource[] }>('/resources');
      set({ resources: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  releaseResource: async (resourceId: string) => {
    set({ isLoading: true, error: null });
    try {
      await fetchApi(`/resources/${resourceId}/release`, { method: 'POST' });
      // Refresh resources
      const res = await fetchApi<{ data: Resource[] }>('/resources');
      set({ resources: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },
}));
