import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useRoute } from '@react-navigation/native';

import { fetchApi } from '../store/api';
import type { SimulationResult } from '../types';

export default function SimulationScreen() {
  const route = useRoute<any>();
  const incidentId = route.params?.incidentId;

  const [availableActions, setAvailableActions] = useState<string[]>([]);
  const [selectedActions, setSelectedActions] = useState<string[]>([]);
  const [simulation, setSimulation] = useState<SimulationResult | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [isLoadingActions, setIsLoadingActions] = useState(true);

  useEffect(() => {
    const loadActions = async () => {
      try {
        const res = await fetchApi<{ success: boolean; data: string[] }>('/simulations/actions');
        setAvailableActions(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoadingActions(false);
      }
    };
    loadActions();
  }, []);

  const toggleAction = (action: string) => {
    setSelectedActions(prev => 
      prev.includes(action) ? prev.filter(a => a !== action) : [...prev, action]
    );
  };

  const runSimulation = async () => {
    if (selectedActions.length === 0) {
      Alert.alert("No Actions Selected", "Please select at least one action to simulate.");
      return;
    }

    setIsSimulating(true);
    setSimulation(null);
    try {
      const res = await fetchApi<{ success: boolean; data: SimulationResult }>('/simulations/run', {
        method: 'POST',
        body: JSON.stringify({
          incident_id: incidentId,
          proposed_actions: selectedActions
        })
      });
      setSimulation(res.data);
    } catch (err: any) {
      Alert.alert("Simulation Failed", err.message);
    } finally {
      setIsSimulating(false);
    }
  };

  const formatActionName = (action: string) => {
    return action.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  };

  const renderDelta = (metric: string, data: any) => {
    const isImproved = data.improved;
    return (
      <View key={metric} className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex-row justify-between items-center mb-2">
        <View>
          <Text className="text-slate-300 font-bold uppercase tracking-wider text-xs mb-1">
            {metric.replace(/_/g, ' ')}
          </Text>
          <View className="flex-row items-center">
            <Text className="text-slate-500 line-through mr-2">{data.before}</Text>
            <Feather name="arrow-right" size={14} color="#64748B" className="mr-2" />
            <Text className="text-white font-bold">{data.after}</Text>
          </View>
        </View>
        <View className={`px-2 py-1 rounded flex-row items-center ${isImproved ? 'bg-emerald-500/20' : 'bg-red-500/20'}`}>
          <Feather name={isImproved ? "trending-down" : "trending-up"} size={14} color={isImproved ? "#10B981" : "#EF4444"} />
          <Text className={`ml-1 text-xs font-bold ${isImproved ? 'text-emerald-400' : 'text-red-400'}`}>
            {Math.abs(data.delta_pct)}%
          </Text>
        </View>
      </View>
    );
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <ScrollView className="flex-1 px-4">
        
        <Text className="text-white font-bold text-xl mb-2 mt-4">Action Sandbox</Text>
        <Text className="text-slate-400 text-sm mb-6">
          Select interventions to model their predicted impact on the crisis before authorizing dispatch.
        </Text>

        {/* Action Selection */}
        <Text className="text-slate-500 text-xs font-bold uppercase tracking-widest mb-3">Available Actions</Text>
        
        {isLoadingActions ? (
          <ActivityIndicator color="#A855F7" />
        ) : (
          <View className="flex-row flex-wrap mb-6">
            {availableActions.map(action => {
              const isSelected = selectedActions.includes(action);
              return (
                <TouchableOpacity
                  key={action}
                  onPress={() => toggleAction(action)}
                  className={`px-3 py-2 rounded-lg border mr-2 mb-2 ${
                    isSelected 
                      ? 'bg-purple-900/60 border-purple-500/50' 
                      : 'bg-slate-900 border-slate-800'
                  }`}
                >
                  <Text className={isSelected ? 'text-purple-300 font-bold' : 'text-slate-400'}>
                    {formatActionName(action)}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </View>
        )}

        <TouchableOpacity 
          className={`flex-row justify-center items-center p-4 rounded-xl mb-8 ${isSimulating ? 'bg-purple-900/50' : 'bg-purple-600'}`}
          onPress={runSimulation}
          disabled={isSimulating}
        >
          {isSimulating ? (
            <ActivityIndicator color="#fff" className="mr-2" />
          ) : (
            <Feather name="activity" size={20} color="#fff" className="mr-2" />
          )}
          <Text className="text-white font-bold text-lg">
            {isSimulating ? 'Simulating Impact...' : 'Run Simulation'}
          </Text>
        </TouchableOpacity>

        {/* Simulation Results */}
        {simulation && (
          <View className="mb-10">
            <Text className="text-white font-bold text-lg mb-4">Predicted Outcomes</Text>
            
            {/* Deltas */}
            {Object.entries(simulation.metric_deltas).map(([metric, data]) => renderDelta(metric, data))}

            {/* Side Effects */}
            {simulation.side_effects && simulation.side_effects.length > 0 && (
              <View className="mt-4 bg-amber-500/10 border border-amber-500/30 p-4 rounded-xl mb-4">
                <View className="flex-row items-center mb-2">
                  <Feather name="alert-circle" size={16} color="#F59E0B" />
                  <Text className="text-amber-500 font-bold ml-2 uppercase text-xs tracking-wider">Unintended Side Effects</Text>
                </View>
                {simulation.side_effects.map((effect: string, idx: number) => (
                  <Text key={idx} className="text-amber-400/80 text-sm mb-1">• {effect}</Text>
                ))}
              </View>
            )}

            {/* Costs */}
            <View className="flex-row mt-2">
              <View className="flex-1 bg-slate-900 border border-slate-800 p-4 rounded-xl mr-2">
                <Text className="text-slate-500 text-xs uppercase mb-1">Est. Cost</Text>
                <Text className="text-emerald-400 font-bold text-lg flex-wrap">Rs {simulation.cost_estimate_pkr.toLocaleString()}</Text>
              </View>
              <View className="flex-1 bg-slate-900 border border-slate-800 p-4 rounded-xl ml-2">
                <Text className="text-slate-500 text-xs uppercase mb-1">Risk if Delayed</Text>
                <Text className={`font-bold text-lg ${simulation.risk_if_delayed === 'CRITICAL' ? 'text-red-500' : 'text-orange-400'}`}>
                  {simulation.risk_if_delayed}
                </Text>
              </View>
            </View>
          </View>
        )}

      </ScrollView>
    </SafeAreaView>
  );
}
