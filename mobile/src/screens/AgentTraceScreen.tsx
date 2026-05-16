import React, { useEffect } from 'react';
import { View, Text, ScrollView, RefreshControl, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useRoute } from '@react-navigation/native';

import { useTraceStore } from '../store/traceStore';

export default function AgentTraceScreen() {
  const route = useRoute<any>();
  const incidentId = route.params?.incidentId;

  const { traces, fetchTraces, isLoading } = useTraceStore();

  useEffect(() => {
    fetchTraces(incidentId);
  }, [incidentId]);

  const onRefresh = React.useCallback(() => {
    fetchTraces(incidentId);
  }, [incidentId]);

  const getAgentColor = (agentName: string) => {
    switch (agentName) {
      case 'SignalIntakeAgent': return 'text-sky-400';
      case 'CredibilityScoringAgent': return 'text-purple-400';
      case 'ClassificationAgent': return 'text-emerald-400';
      case 'SeverityPredictionAgent': return 'text-orange-400';
      case 'ResourceAllocationAgent': return 'text-blue-400';
      case 'StakeholderNotificationAgent': return 'text-indigo-400';
      case 'SimulationAgent': return 'text-pink-400';
      case 'FalseAlarmRecoveryAgent': return 'text-red-400';
      default: return 'text-slate-400';
    }
  };

  const getAgentIcon = (agentName: string) => {
    switch (agentName) {
      case 'SignalIntakeAgent': return 'radio';
      case 'CredibilityScoringAgent': return 'shield';
      case 'ClassificationAgent': return 'tag';
      case 'SeverityPredictionAgent': return 'trending-up';
      case 'ResourceAllocationAgent': return 'truck';
      case 'StakeholderNotificationAgent': return 'message-square';
      case 'SimulationAgent': return 'activity';
      case 'FalseAlarmRecoveryAgent': return 'power';
      default: return 'cpu';
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <ScrollView 
        className="flex-1 px-4"
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={onRefresh} tintColor="#A855F7" />}
      >
        <Text className="text-white font-bold text-xl mt-4 mb-2">Agent Trace & Audit</Text>
        <Text className="text-slate-400 text-sm mb-6">
          Deterministic execution log of the multi-agent pipeline. Review inputs, logic steps, and fallback usage.
        </Text>

        {traces.length === 0 && !isLoading ? (
          <View className="bg-slate-900 border border-slate-800 p-8 rounded-xl items-center mt-4">
            <Feather name="file-text" size={48} color="#334155" />
            <Text className="text-slate-300 font-bold mt-4 mb-2">No Traces Found</Text>
            <Text className="text-slate-500 text-center">
              No agent execution logs exist for this incident yet.
            </Text>
          </View>
        ) : (
          <View className="mb-10">
            {traces.map((trace, index) => (
              <View key={trace.id} className="flex-row mb-6">
                {/* Timeline Line & Node */}
                <View className="items-center mr-4">
                  <View className="bg-slate-800 rounded-full p-2 border border-slate-700 z-10">
                    <Feather name={getAgentIcon(trace.agent_name)} size={16} color="#94A3B8" />
                  </View>
                  {index !== traces.length - 1 && (
                    <View className="w-0.5 flex-1 bg-slate-800 -mb-6 mt-1" />
                  )}
                </View>

                {/* Trace Card */}
                <View className="flex-1 bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <View className="flex-row justify-between items-start mb-2">
                    <View className="flex-1">
                      <Text className={`font-bold text-sm ${getAgentColor(trace.agent_name)}`}>
                        {trace.agent_name}
                      </Text>
                      <Text className="text-slate-500 text-xs mt-1">Step: {trace.step}</Text>
                    </View>
                    <Text className="text-slate-500 text-xs">
                      {new Date(trace.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    </Text>
                  </View>

                  <View className="bg-slate-950 p-3 rounded-lg border border-slate-800/50 mt-2 mb-2">
                    <Text className="text-slate-500 text-[10px] uppercase font-bold tracking-widest mb-1">Input Summary</Text>
                    <Text className="text-slate-300 text-xs">{trace.input_summary}</Text>
                  </View>

                  <View className="bg-slate-950 p-3 rounded-lg border border-slate-800/50 mb-3">
                    <Text className="text-slate-500 text-[10px] uppercase font-bold tracking-widest mb-1">Output Summary</Text>
                    <Text className="text-white text-sm">{trace.output_summary}</Text>
                  </View>

                  <View className="flex-row flex-wrap mt-1 border-t border-slate-800/50 pt-3 justify-between items-center">
                    <View className="flex-row items-center">
                      <Feather name="clock" size={12} color="#64748B" className="mr-1" />
                      <Text className="text-slate-400 text-xs">{trace.duration_ms} ms</Text>
                    </View>
                    
                    {trace.tool_calls.length > 0 && (
                      <View className="flex-row items-center bg-slate-800 px-2 py-1 rounded">
                        <Feather name="tool" size={10} color="#94A3B8" className="mr-1" />
                        <Text className="text-slate-300 text-xs">{trace.tool_calls.length} tools</Text>
                      </View>
                    )}

                    {trace.human_review_required && (
                      <View className="flex-row items-center bg-amber-500/20 px-2 py-1 rounded">
                        <Feather name="eye" size={10} color="#F59E0B" className="mr-1" />
                        <Text className="text-amber-500 font-bold text-[10px]">REVIEW REQUIRED</Text>
                      </View>
                    )}
                  </View>
                </View>
              </View>
            ))}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
