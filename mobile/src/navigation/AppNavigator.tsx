import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Feather } from '@expo/vector-icons';

// Import Types
import { RootStackParamList, MainTabParamList } from './types';

// Import Screens (Stubs exist in src/screens)
import HomeDashboardScreen from '../screens/HomeDashboardScreen';
import IncidentsScreen from '../screens/IncidentsScreen';
import DemoModeScreen from '../screens/DemoModeScreen';

import IncidentDetailScreen from '../screens/IncidentDetailScreen';
import AIAnalysisScreen from '../screens/AIAnalysisScreen';
import SimulationScreen from '../screens/SimulationScreen';
import ResourceAllocationScreen from '../screens/ResourceAllocationScreen';
import AgentTraceScreen from '../screens/AgentTraceScreen';
import SignalIntakeScreen from '../screens/SignalIntakeScreen';
import RecoveryScreen from '../screens/RecoveryScreen';
import NotificationScreen from '../screens/NotificationScreen';
import SplashScreen from '../screens/SplashScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

/**
 * Bottom Tabs Navigator
 * Holds the root-level navigation items
 */
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#0F172A', // Slate 900
          borderTopColor: '#1E293B',  // Slate 800
          borderTopWidth: 1,
        },
        tabBarActiveTintColor: '#38BDF8', // Sky 400
        tabBarInactiveTintColor: '#64748B', // Slate 500
        tabBarIcon: ({ color, size }) => {
          let iconName: keyof typeof Feather.glyphMap;

          if (route.name === 'Dashboard') {
            iconName = 'activity';
          } else if (route.name === 'Incidents') {
            iconName = 'alert-triangle';
          } else if (route.name === 'DemoMode') {
            iconName = 'play-circle';
          } else {
            iconName = 'circle';
          }

          return <Feather name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Dashboard" component={HomeDashboardScreen} />
      <Tab.Screen name="Incidents" component={IncidentsScreen} />
      <Tab.Screen name="DemoMode" component={DemoModeScreen} options={{ title: 'Demo' }} />
    </Tab.Navigator>
  );
}

/**
 * Root Stack Navigator
 * Wraps the Bottom Tabs and adds modal/drill-down screens on top
 */
export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: '#0F172A' },
          headerTintColor: '#F8FAFC',
          headerTitleStyle: { fontWeight: 'bold' },
          contentStyle: { backgroundColor: '#020617' }, // Slate 950 base background
        }}
      >
        <Stack.Screen 
          name="Splash" 
          component={SplashScreen} 
          options={{ headerShown: false }} 
        />
        <Stack.Screen 
          name="MainTabs" 
          component={MainTabs} 
          options={{ headerShown: false, gestureEnabled: false }} 
        />
        
        {/* Drill-down screens */}
        <Stack.Screen 
          name="IncidentDetail" 
          component={IncidentDetailScreen} 
          options={{ title: 'Incident Detail' }} 
        />
        <Stack.Screen 
          name="AIAnalysis" 
          component={AIAnalysisScreen} 
          options={{ title: 'AI Analysis' }} 
        />
        <Stack.Screen 
          name="Simulation" 
          component={SimulationScreen} 
          options={{ title: 'Simulation' }} 
        />
        <Stack.Screen 
          name="ResourceAllocation" 
          component={ResourceAllocationScreen} 
          options={{ title: 'Resource Allocation' }} 
        />
        <Stack.Screen 
          name="AgentTrace" 
          component={AgentTraceScreen} 
          options={{ title: 'Agent Trace' }} 
        />
        <Stack.Screen 
          name="SignalIntake" 
          component={SignalIntakeScreen} 
          options={{ title: 'Signal Intake', presentation: 'modal' }} 
        />
        <Stack.Screen 
          name="Recovery" 
          component={RecoveryScreen} 
          options={{ title: 'False Alarm Recovery', presentation: 'modal' }} 
        />
        <Stack.Screen 
          name="Notifications" 
          component={NotificationScreen} 
          options={{ title: 'Notifications' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
