import React, { useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, RefreshControl, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { useIncidentStore } from '../store/incidentStore';
import { useResourceStore } from '../store/resourceStore';
import { useSignalStore } from '../store/signalStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'MainTabs'>;

export default function HomeDashboardScreen() {
  const navigation = useNavigation<NavigationProp>();
  
  const { incidents, fetchIncidents, isLoading: loadingIncidents } = useIncidentStore();
  const { resources, fetchResources, isLoading: loadingResources } = useResourceStore();
  const { signals, fetchSignals, isLoading: loadingSignals } = useSignalStore();

  useEffect(() => {
    fetchIncidents();
    fetchResources();
    fetchSignals();
  }, []);

  const onRefresh = React.useCallback(() => {
    fetchIncidents();
    fetchResources();
    fetchSignals();
  }, []);

  const activeIncidents = incidents.filter(i => i.status !== 'resolved');
  const criticalCount = activeIncidents.filter(i => i.severity === 'CRITICAL').length;
  const deployedResources = resources.filter(r => r.status === 'assigned').length;
  const availableResources = resources.filter(r => r.status === 'available').length;
  
  const isRefreshing = loadingIncidents || loadingResources || loadingSignals;

  return (
    <SafeAreaView className="flex-1 bg-slate-950">
      {/* Header */}
      <View className="px-6 py-4 flex-row justify-between items-center border-b border-slate-800">
        <View>
          <Text className="text-sky-400 font-bold text-xl uppercase tracking-widest">CityCommand</Text>
          <Text className="text-slate-400 text-xs">AI Orchestrator • Online</Text>
        </View>
        <TouchableOpacity onPress={() => navigation.navigate('SignalIntake')}>
          <View className="bg-sky-500/20 p-3 rounded-full">
            <Feather name="plus" size={20} color="#38BDF8" />
          </View>
        </TouchableOpacity>
      </View>

      <ScrollView 
        className="flex-1 px-4"
        refreshControl={<RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} tintColor="#38BDF8" />}
      >
        {/* Metric Cards */}
        <View className="flex-row mt-6 mb-8 justify-between">
          <View className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex-1 mr-2">
            <Feather name="alert-triangle" size={24} color={criticalCount > 0 ? "#EF4444" : "#F59E0B"} />
            <Text className="text-white text-3xl font-bold mt-2">{activeIncidents.length}</Text>
            <Text className="text-slate-400 text-xs mt-1 uppercase">Active Incidents</Text>
          </View>
          
          <View className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex-1 ml-2">
            <Feather name="truck" size={24} color="#38BDF8" />
            <Text className="text-white text-3xl font-bold mt-2">{deployedResources}</Text>
            <Text className="text-slate-400 text-xs mt-1 uppercase">Units Deployed</Text>
          </View>
        </View>

        {/* Priority Incidents List */}
        <View className="mb-8">
          <View className="flex-row justify-between items-end mb-4">
            <Text className="text-white text-lg font-bold">Priority Incidents</Text>
            <TouchableOpacity onPress={() => navigation.navigate('MainTabs' as any)}>
              <Text className="text-sky-400 text-sm">View All</Text>
            </TouchableOpacity>
          </View>
          
          {activeIncidents.length === 0 ? (
            <View className="bg-slate-900/50 p-6 rounded-xl border border-slate-800/50 items-center">
              <Feather name="check-circle" size={32} color="#10B981" />
              <Text className="text-slate-300 mt-3 font-medium">City sector clear</Text>
              <Text className="text-slate-500 text-sm mt-1 text-center">No active emergencies detected in the grid.</Text>
            </View>
          ) : (
            activeIncidents.slice(0, 3).map((incident) => (
              <TouchableOpacity 
                key={incident.id} 
                onPress={() => navigation.navigate('IncidentDetail', { incidentId: incident.id })}
                className="bg-slate-900 p-4 rounded-xl mb-3 border border-slate-800 flex-row items-center"
              >
                <View className={`w-3 h-full rounded-full mr-4 ${incident.severity === 'CRITICAL' ? 'bg-red-500' : incident.severity === 'HIGH' ? 'bg-orange-500' : 'bg-yellow-500'}`} />
                <View className="flex-1">
                  <Text className="text-white font-bold text-base">{incident.title}</Text>
                  <Text className="text-slate-400 text-sm mt-1">
                    <Feather name="map-pin" size={12} /> {incident.location?.area || 'Unknown location'}
                  </Text>
                </View>
                <Feather name="chevron-right" size={20} color="#64748B" />
              </TouchableOpacity>
            ))
          )}
        </View>

        {/* Live Signal Feed */}
        <View className="mb-8">
          <Text className="text-white text-lg font-bold mb-4">Live Signal Feed</Text>
          {signals.slice(0, 5).map((signal) => (
            <View key={signal.id} className="flex-row mb-4 bg-slate-900/30 p-3 rounded-lg border border-slate-800/30">
              <View className="bg-slate-800 p-2 rounded-full h-10 w-10 items-center justify-center mr-3">
                <Feather 
                  name={signal.source_type === 'social' ? 'twitter' : signal.source_type === 'sensor' ? 'cpu' : 'phone-call'} 
                  size={16} 
                  color="#94A3B8" 
                />
              </View>
              <View className="flex-1">
                <Text className="text-slate-200 text-sm">{signal.raw_text}</Text>
                <Text className="text-slate-500 text-xs mt-1 uppercase tracking-wider">{signal.source_type} • {signal.metadata?.urgency || 'Normal'}</Text>
              </View>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
