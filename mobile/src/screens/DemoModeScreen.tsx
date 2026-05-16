import React from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, Alert, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { useDemoStore } from '../store/demoStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'MainTabs'>;

export default function DemoModeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { isGenerating, triggerDemoScenario } = useDemoStore();

  const handleLaunchScenario = async () => {
    Alert.alert(
      "Launch Demo Scenario",
      "This will inject multiple concurrent emergencies (including the F-11 Heat Wave and G-10 Flood) into the system and trigger the AI pipeline.",
      [
        { text: "Cancel", style: "cancel" },
        { 
          text: "Launch", 
          style: "default",
          onPress: async () => {
            try {
              await triggerDemoScenario();
              Alert.alert("Scenario Active", "The pipeline has processed the events.", [
                { text: "View Dashboard", onPress: () => navigation.navigate('Dashboard' as any) }
              ]);
            } catch (err: any) {
              Alert.alert("Error", err.message);
            }
          }
        }
      ]
    );
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['top']}>
      <ScrollView className="flex-1 px-4">
        <View className="py-8 items-center border-b border-slate-800 mb-6">
          <View className="bg-sky-500/20 p-4 rounded-full mb-4">
            <Feather name="play-circle" size={48} color="#38BDF8" />
          </View>
          <Text className="text-white font-bold text-2xl text-center">Hackathon Demo Control</Text>
          <Text className="text-slate-400 text-center mt-2 px-4">
            Use these tools to showcase CityCommand AI's capabilities to the judges.
          </Text>
        </View>

        <Text className="text-slate-500 text-xs font-bold uppercase tracking-widest mb-3">Pre-configured Scenarios</Text>
        
        <TouchableOpacity 
          className={`p-5 rounded-2xl border border-sky-500/50 mb-6 ${isGenerating ? 'bg-sky-900/40' : 'bg-slate-900'}`}
          onPress={handleLaunchScenario}
          disabled={isGenerating}
        >
          <View className="flex-row items-start mb-3">
            <View className="bg-sky-500 p-2 rounded-lg mr-3 mt-1">
              {isGenerating ? <ActivityIndicator color="#fff" size="small" /> : <Feather name="zap" size={20} color="#fff" />}
            </View>
            <View className="flex-1">
              <Text className="text-white font-bold text-lg mb-1">Islamabad Crisis Scenario</Text>
              <Text className="text-slate-400 text-sm leading-5">
                Injects 5 concurrent raw signals simulating a severe heatwave in F-11 and localized urban flooding in G-10.
              </Text>
            </View>
          </View>
          
          <View className="bg-slate-950 p-3 rounded-lg flex-row justify-between items-center mt-2">
            <Text className="text-slate-500 text-xs font-mono">Will trigger 6-stage pipeline</Text>
            <Feather name="arrow-right" size={14} color="#38BDF8" />
          </View>
        </TouchableOpacity>

        <Text className="text-slate-500 text-xs font-bold uppercase tracking-widest mb-3">System Diagnostics</Text>
        <View className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <View className="flex-row justify-between items-center mb-3">
            <Text className="text-slate-300">Backend Connection</Text>
            <View className="flex-row items-center">
              <View className="w-2 h-2 bg-emerald-500 rounded-full mr-2" />
              <Text className="text-emerald-400 font-bold">Online</Text>
            </View>
          </View>
          <View className="flex-row justify-between items-center mb-3 border-t border-slate-800 pt-3">
            <Text className="text-slate-300">API Endpoint</Text>
            <Text className="text-slate-500 text-xs font-mono">http://10.0.2.2:8000</Text>
          </View>
          <View className="flex-row justify-between items-center border-t border-slate-800 pt-3">
            <Text className="text-slate-300">Pipeline State</Text>
            <Text className="text-slate-500 text-xs">Deterministic Mode</Text>
          </View>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}
