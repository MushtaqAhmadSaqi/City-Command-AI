import React, { useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, RefreshControl, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { useIncidentStore } from '../store/incidentStore';
import { useResourceStore } from '../store/resourceStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'IncidentDetail'>;

export default function IncidentDetailScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<any>();
  const incidentId = route.params?.incidentId;

  const { currentIncident, fetchIncidentDetail, isLoading: loadingInc } = useIncidentStore();
  const { assignments, fetchAssignments, isLoading: loadingRes } = useResourceStore();

  useEffect(() => {
    if (incidentId) {
      fetchIncidentDetail(incidentId);
      fetchAssignments(incidentId);
    }
  }, [incidentId]);

  const onRefresh = React.useCallback(() => {
    if (incidentId) {
      fetchIncidentDetail(incidentId);
      fetchAssignments(incidentId);
    }
  }, [incidentId]);

  if (!currentIncident) {
    return (
      <SafeAreaView className="flex-1 bg-slate-950 justify-center items-center">
        <ActivityIndicator size="large" color="#38BDF8" />
      </SafeAreaView>
    );
  }

  const isRefreshing = loadingInc || loadingRes;
  const isCritical = currentIncident.severity === 'CRITICAL';
  const isResolved = currentIncident.status === 'resolved';

  const QuickActionButton = ({ icon, label, onPress, color = '#38BDF8', bg = 'bg-slate-900' }: any) => (
    <TouchableOpacity 
      onPress={onPress}
      className={`${bg} p-4 rounded-xl border border-slate-800 flex-1 mx-1 items-center justify-center min-h-[100px] mb-2`}
    >
      <Feather name={icon} size={24} color={color} className="mb-2" />
      <Text className="text-slate-300 text-xs font-bold text-center mt-2">{label}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <ScrollView 
        className="flex-1 px-4"
        refreshControl={<RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} tintColor="#38BDF8" />}
      >
        {/* Header Block */}
        <View className={`p-5 rounded-2xl border mb-6 mt-4 ${isCritical ? 'bg-red-950/40 border-red-900/50' : 'bg-slate-900 border-slate-800'}`}>
          <View className="flex-row justify-between items-start mb-4">
            <View className={`px-2 py-1 rounded ${isResolved ? 'bg-slate-800' : isCritical ? 'bg-red-500' : 'bg-orange-500'}`}>
              <Text className="text-white text-xs font-bold uppercase">{isResolved ? 'RESOLVED' : currentIncident.severity}</Text>
            </View>
            <Text className="text-slate-400 text-xs">{new Date(currentIncident.created_at).toLocaleTimeString()}</Text>
          </View>
          
          <Text className="text-white font-bold text-2xl mb-2">{currentIncident.title}</Text>
          
          <View className="flex-row items-center mb-4">
            <Feather name="map-pin" size={14} color="#94A3B8" />
            <Text className="text-slate-400 ml-2">{currentIncident.location?.area || 'Unknown Area'}</Text>
          </View>

          <View className="flex-row border-t border-slate-800/50 pt-4">
            <View className="flex-1">
              <Text className="text-slate-500 text-xs uppercase mb-1">Confidence</Text>
              <Text className="text-white font-bold text-lg">{(currentIncident.confidence * 100).toFixed(0)}%</Text>
            </View>
            <View className="flex-1 border-l border-slate-800/50 pl-4">
              <Text className="text-slate-500 text-xs uppercase mb-1">Priority Score</Text>
              <Text className="text-white font-bold text-lg">{currentIncident.priority_score?.toFixed(1) || 'N/A'}</Text>
            </View>
            <View className="flex-1 border-l border-slate-800/50 pl-4">
              <Text className="text-slate-500 text-xs uppercase mb-1">Signals</Text>
              <Text className="text-white font-bold text-lg">{currentIncident.signal_ids?.length || 0}</Text>
            </View>
          </View>
        </View>

        {/* Resources Summary */}
        <View className="mb-6 bg-slate-900 p-4 rounded-xl border border-slate-800 flex-row justify-between items-center">
          <View>
            <Text className="text-white font-bold text-base">Assigned Units</Text>
            <Text className="text-slate-400 text-sm">{assignments.length} resources en route</Text>
          </View>
          <TouchableOpacity 
            className="bg-sky-500/20 px-4 py-2 rounded-lg"
            onPress={() => navigation.navigate('ResourceAllocation', { incidentId })}
          >
            <Text className="text-sky-400 font-bold text-sm">Manage</Text>
          </TouchableOpacity>
        </View>

        {/* Action Grid */}
        <Text className="text-white font-bold text-lg mb-3">AI Intelligence</Text>
        <View className="flex-row mb-2">
          <QuickActionButton 
            icon="cpu" 
            label="AI Analysis" 
            onPress={() => navigation.navigate('AIAnalysis', { incidentId })} 
          />
          <QuickActionButton 
            icon="activity" 
            label="Simulation" 
            color="#A855F7" // Purple
            onPress={() => navigation.navigate('Simulation', { incidentId })} 
          />
        </View>

        <Text className="text-white font-bold text-lg mb-3 mt-4">Operations</Text>
        <View className="flex-row mb-2">
          <QuickActionButton 
            icon="radio" 
            label="Notifications" 
            color="#10B981" // Emerald
            onPress={() => navigation.navigate('Notifications', { incidentId })} 
          />
          <QuickActionButton 
            icon="file-text" 
            label="Agent Traces" 
            color="#F59E0B" // Amber
            onPress={() => navigation.navigate('AgentTrace', { incidentId })} 
          />
        </View>

        {/* Danger Zone */}
        {!isResolved && (
          <View className="mt-8 mb-8">
            <TouchableOpacity 
              className="bg-slate-900 border border-red-900/50 p-4 rounded-xl flex-row justify-center items-center"
              onPress={() => navigation.navigate('Recovery', { incidentId })}
            >
              <Feather name="x-circle" size={18} color="#EF4444" className="mr-2" />
              <Text className="text-red-400 font-bold ml-2">Mark as False Alarm</Text>
            </TouchableOpacity>
          </View>
        )}
        
      </ScrollView>
    </SafeAreaView>
  );
}
