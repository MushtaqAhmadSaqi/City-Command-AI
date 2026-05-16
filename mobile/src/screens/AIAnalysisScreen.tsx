import React, { useEffect } from 'react';
import { View, Text, ScrollView, RefreshControl, ActivityIndicator, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { useIncidentStore } from '../store/incidentStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'AIAnalysis'>;

export default function AIAnalysisScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<any>();
  const incidentId = route.params?.incidentId;

  const { aiAnalysis, fetchAiAnalysis, isLoading } = useIncidentStore();

  useEffect(() => {
    if (incidentId) {
      fetchAiAnalysis(incidentId);
    }
  }, [incidentId]);

  const onRefresh = React.useCallback(() => {
    if (incidentId) fetchAiAnalysis(incidentId);
  }, [incidentId]);

  if (isLoading && !aiAnalysis) {
    return (
      <SafeAreaView className="flex-1 bg-slate-950 justify-center items-center">
        <ActivityIndicator size="large" color="#A855F7" />
      </SafeAreaView>
    );
  }

  if (!aiAnalysis) {
    return (
      <SafeAreaView className="flex-1 bg-slate-950 items-center justify-center">
        <Text className="text-slate-400">Analysis data unavailable.</Text>
      </SafeAreaView>
    );
  }

  const { credibility, priority, classification, human_review_required } = aiAnalysis;

  const renderProgressBar = (label: string, value: number, max: number, colorClass: string) => {
    const percentage = Math.min(100, Math.max(0, (value / max) * 100));
    return (
      <View className="mb-3" key={label}>
        <View className="flex-row justify-between mb-1">
          <Text className="text-slate-300 text-xs">{label}</Text>
          <Text className="text-slate-400 text-xs">{value.toFixed(2)}</Text>
        </View>
        <View className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
          <View className={`h-full ${colorClass}`} style={{ width: `${percentage}%` }} />
        </View>
      </View>
    );
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <ScrollView 
        className="flex-1 px-4"
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={onRefresh} tintColor="#A855F7" />}
      >
        {/* Header Title */}
        <Text className="text-white font-bold text-xl mb-6 mt-4">AI Credibility & Classification</Text>

        {human_review_required && (
          <View className="bg-amber-500/20 border border-amber-500/50 p-4 rounded-xl flex-row items-start mb-6">
            <Feather name="alert-triangle" size={20} color="#F59E0B" className="mr-3 mt-1" />
            <View className="flex-1">
              <Text className="text-amber-500 font-bold mb-1">Human Review Recommended</Text>
              <Text className="text-amber-400/80 text-xs leading-5">
                The AI model detected low confidence or alternate hypotheses. Please verify the signal sources before dispatch.
              </Text>
            </View>
          </View>
        )}

        {/* Credibility Breakdown */}
        <View className="bg-slate-900 rounded-xl border border-slate-800 p-5 mb-6">
          <View className="flex-row items-center mb-4 border-b border-slate-800 pb-4">
            <View className="bg-purple-500/20 p-2 rounded-lg mr-3">
              <Feather name="shield" size={20} color="#A855F7" />
            </View>
            <View>
              <Text className="text-slate-400 text-xs uppercase tracking-wider">Credibility Score</Text>
              <Text className="text-white font-bold text-2xl">{(credibility.confidence * 100).toFixed(1)}%</Text>
            </View>
          </View>

          <Text className="text-slate-500 text-xs font-bold mb-3 uppercase tracking-widest">Factor Breakdown</Text>
          {Object.entries(credibility.factors).map(([key, val]: [string, any]) => {
            if (val === 0) return null;
            const isPenalty = val < 0;
            return renderProgressBar(
              key.replace(/_/g, ' '), 
              Math.abs(val), 
              1, 
              isPenalty ? 'bg-red-500' : 'bg-purple-500'
            );
          })}
        </View>

        {/* Classification Engine */}
        <View className="bg-slate-900 rounded-xl border border-slate-800 p-5 mb-6">
          <View className="flex-row items-center mb-4">
            <View className="bg-sky-500/20 p-2 rounded-lg mr-3">
              <Feather name="tag" size={20} color="#38BDF8" />
            </View>
            <Text className="text-white font-bold text-lg">Classification</Text>
          </View>

          <View className="bg-slate-950 p-4 rounded-lg border border-slate-800 mb-4">
            <Text className="text-slate-500 text-xs mb-1">PRIMARY HYPOTHESIS</Text>
            <View className="flex-row justify-between items-center">
              <Text className="text-sky-400 font-bold text-lg">{classification.primary_type.toUpperCase()}</Text>
              <Text className="text-slate-300">Score: {classification.primary_score.toFixed(2)}</Text>
            </View>
            {classification.evidence_keywords?.length > 0 && (
              <View className="flex-row flex-wrap mt-3">
                {classification.evidence_keywords.map((kw: string) => (
                  <View key={kw} className="bg-slate-800 px-2 py-1 rounded mr-2 mb-2">
                    <Text className="text-slate-400 text-xs">{kw}</Text>
                  </View>
                ))}
              </View>
            )}
          </View>

          {classification.alternate_hypotheses?.length > 0 && (
            <View>
              <Text className="text-slate-500 text-xs mb-2">ALTERNATE HYPOTHESES</Text>
              {classification.alternate_hypotheses.map((alt: any, idx: number) => (
                <View key={idx} className="flex-row justify-between items-center mb-2">
                  <Text className="text-slate-400">{alt.type}</Text>
                  <Text className="text-slate-500 text-xs">{alt.confidence.toFixed(2)}</Text>
                </View>
              ))}
            </View>
          )}
        </View>

        {/* Priority Score Breakdown */}
        <View className="bg-slate-900 rounded-xl border border-slate-800 p-5 mb-8">
          <View className="flex-row items-center mb-4 border-b border-slate-800 pb-4">
            <View className="bg-orange-500/20 p-2 rounded-lg mr-3">
              <Feather name="bar-chart-2" size={20} color="#F97316" />
            </View>
            <View>
              <Text className="text-slate-400 text-xs uppercase tracking-wider">Priority Ranking Score</Text>
              <Text className="text-white font-bold text-2xl">{priority.total_score.toFixed(1)} <Text className="text-slate-500 text-lg">/ 100</Text></Text>
            </View>
          </View>

          {Object.entries(priority.breakdown).map(([key, val]: [string, any]) => {
            return renderProgressBar(
              key.replace(/_/g, ' '), 
              val, 
              40, // Max individual weight is roughly 40 (severity)
              'bg-orange-500'
            );
          })}
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}
