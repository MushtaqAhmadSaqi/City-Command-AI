import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, RefreshControl, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useRoute } from '@react-navigation/native';

import { useResourceStore } from '../store/resourceStore';
import { useIncidentStore } from '../store/incidentStore';

export default function ResourceAllocationScreen() {
  const route = useRoute<any>();
  const incidentId = route.params?.incidentId;

  const { 
    resources, 
    assignments, 
    fetchResources, 
    fetchAssignments, 
    allocateResources, 
    releaseResource,
    isLoading: resLoading
  } = useResourceStore();

  const { currentIncident, fetchIncidentDetail } = useIncidentStore();

  const [isAllocating, setIsAllocating] = useState(false);

  useEffect(() => {
    if (incidentId) {
      fetchIncidentDetail(incidentId);
      fetchAssignments(incidentId);
      fetchResources(); // Get full fleet status
    }
  }, [incidentId]);

  const onRefresh = React.useCallback(() => {
    if (incidentId) {
      fetchIncidentDetail(incidentId);
      fetchAssignments(incidentId);
      fetchResources();
    }
  }, [incidentId]);

  const handleTriggerDispatch = async () => {
    setIsAllocating(true);
    try {
      await allocateResources([incidentId]);
      await fetchAssignments(incidentId);
      await fetchResources();
      Alert.alert("Dispatch Complete", "AI has allocated optimal resources.");
    } catch (err: any) {
      Alert.alert("Dispatch Failed", err.message);
    } finally {
      setIsAllocating(false);
    }
  };

  const handleRelease = (resourceId: string) => {
    Alert.alert(
      "Release Unit",
      "Return this unit to available status?",
      [
        { text: "Cancel", style: "cancel" },
        { 
          text: "Release", 
          style: "destructive",
          onPress: async () => {
            await releaseResource(resourceId);
            fetchAssignments(incidentId);
            fetchResources();
          }
        }
      ]
    );
  };

  const getIcon = (type: string) => {
    if (type.includes('ambulance')) return 'activity';
    if (type.includes('police')) return 'shield';
    if (type.includes('pump')) return 'droplet';
    if (type.includes('crane')) return 'tool';
    return 'truck';
  };

  const availableUnits = resources.filter(r => r.status === 'available');
  const cityReserve = availableUnits.filter(r => r.city_reserve);
  const generalAvailable = availableUnits.filter(r => !r.city_reserve);

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <ScrollView 
        className="flex-1 px-4"
        refreshControl={<RefreshControl refreshing={resLoading} onRefresh={onRefresh} tintColor="#38BDF8" />}
      >
        <View className="py-4">
          <Text className="text-white font-bold text-xl mb-1">Resource Dispatch</Text>
          <Text className="text-slate-400 text-sm">{currentIncident?.title}</Text>
        </View>

        {/* Action Trigger */}
        <TouchableOpacity 
          className={`flex-row justify-center items-center p-4 rounded-xl mb-6 ${isAllocating ? 'bg-sky-900/50' : 'bg-sky-600'}`}
          onPress={handleTriggerDispatch}
          disabled={isAllocating || currentIncident?.status === 'resolved'}
        >
          {isAllocating ? (
            <ActivityIndicator color="#fff" className="mr-2" />
          ) : (
            <Feather name="cpu" size={20} color="#fff" className="mr-2" />
          )}
          <Text className="text-white font-bold text-lg">
            {isAllocating ? 'Calculating Routes...' : 'Trigger AI Dispatch'}
          </Text>
        </TouchableOpacity>

        {/* Assigned Units */}
        <Text className="text-slate-400 font-bold text-xs tracking-widest uppercase mb-3">Units On Scene / En Route</Text>
        {assignments.length === 0 ? (
          <View className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl items-center mb-6">
            <Feather name="truck" size={32} color="#334155" />
            <Text className="text-slate-400 mt-2">No units currently assigned.</Text>
          </View>
        ) : (
          <View className="mb-6">
            {assignments.map(assignment => {
              const res = resources.find(r => r.id === assignment.resource_id);
              return (
                <View key={assignment.id} className="bg-slate-900 border border-slate-800 p-4 rounded-xl mb-3">
                  <View className="flex-row justify-between items-center mb-2">
                    <View className="flex-row items-center">
                      <View className="bg-sky-500/20 p-2 rounded-lg mr-3">
                        <Feather name={getIcon(assignment.resource_type)} size={18} color="#38BDF8" />
                      </View>
                      <View>
                        <Text className="text-white font-bold">{assignment.resource_type.replace('_', ' ').toUpperCase()}</Text>
                        <Text className="text-slate-400 text-xs">ETA: {assignment.estimated_arrival_mins} mins</Text>
                      </View>
                    </View>
                    <TouchableOpacity 
                      className="bg-red-500/20 px-3 py-1.5 rounded-lg border border-red-500/30"
                      onPress={() => handleRelease(assignment.resource_id)}
                    >
                      <Text className="text-red-400 text-xs font-bold">Release</Text>
                    </TouchableOpacity>
                  </View>
                  {assignment.trade_off_notes && (
                    <View className="bg-slate-950 p-3 rounded-lg border border-slate-800/50 mt-2">
                      <View className="flex-row items-center mb-1">
                        <Feather name="info" size={12} color="#94A3B8" className="mr-1" />
                        <Text className="text-slate-400 text-xs font-bold uppercase tracking-widest">AI Trade-off Note</Text>
                      </View>
                      <Text className="text-slate-300 text-sm leading-5">{assignment.trade_off_notes}</Text>
                    </View>
                  )}
                </View>
              );
            })}
          </View>
        )}

        {/* Global Fleet Status */}
        <Text className="text-slate-400 font-bold text-xs tracking-widest uppercase mb-3">Global Fleet Status</Text>
        <View className="bg-slate-900 border border-slate-800 p-5 rounded-xl mb-8">
          <View className="flex-row justify-between items-center mb-4 border-b border-slate-800 pb-4">
            <Text className="text-slate-300">Available General Units</Text>
            <Text className="text-white font-bold text-lg">{generalAvailable.length}</Text>
          </View>
          <View className="flex-row justify-between items-center mb-1">
            <Text className="text-slate-300">City Reserve (Emergency Only)</Text>
            <Text className="text-sky-400 font-bold text-lg">{cityReserve.length}</Text>
          </View>
          <Text className="text-slate-500 text-xs mt-2">
            The AI prioritizes general units and only unlocks City Reserve for CRITICAL multi-node emergencies.
          </Text>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}
