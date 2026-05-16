export type RootStackParamList = {
  MainTabs: undefined;
  IncidentDetail: { incidentId: string };
  AIAnalysis: { incidentId: string };
  Simulation: { incidentId: string };
  ResourceAllocation: { incidentId: string };
  AgentTrace: { incidentId?: string; workflowId?: string };
  SignalIntake: undefined;
  Recovery: { incidentId: string };
  Notifications: { incidentId: string };
};

export type MainTabParamList = {
  Dashboard: undefined;
  Incidents: undefined;
  DemoMode: undefined;
};

// Global augmentation to let useNavigation() know about the types
declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
