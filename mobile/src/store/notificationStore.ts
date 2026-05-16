import { create } from 'zustand';
import { fetchApi } from './api';

export interface Notification {
  id: string;
  incident_id: string;
  audience: string;
  channel: string;
  message: string;
  status: 'draft' | 'approved' | 'sent' | 'retracted';
  requires_approval: boolean;
  sent_at: string | null;
  created_by_agent: string;
  created_at: string;
}

interface NotificationState {
  notifications: Notification[];
  isLoading: boolean;
  error: string | null;

  fetchNotifications: (incidentId: string) => Promise<void>;
  draftNotifications: (incidentId: string) => Promise<void>;
  updateStatus: (notificationId: string, status: string, incidentId: string) => Promise<void>;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  isLoading: false,
  error: null,

  fetchNotifications: async (incidentId: string) => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetchApi<{ data: Notification[] }>(`/notifications?incident_id=${incidentId}`);
      set({ notifications: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  draftNotifications: async (incidentId: string) => {
    set({ isLoading: true, error: null });
    try {
      await fetchApi('/notifications/draft', {
        method: 'POST',
        body: JSON.stringify({ incident_id: incidentId })
      });
      // Refresh list
      const res = await fetchApi<{ data: Notification[] }>(`/notifications?incident_id=${incidentId}`);
      set({ notifications: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  updateStatus: async (notificationId: string, status: string, incidentId: string) => {
    set({ isLoading: true, error: null });
    try {
      await fetchApi(`/notifications/${notificationId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status })
      });
      // Refresh list
      const res = await fetchApi<{ data: Notification[] }>(`/notifications?incident_id=${incidentId}`);
      set({ notifications: res.data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  }
}));
