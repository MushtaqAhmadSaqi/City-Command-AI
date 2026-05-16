import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator, Alert, KeyboardAvoidingView, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useRoute, useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { fetchApi } from '../store/api';
import { useIncidentStore } from '../store/incidentStore';
import { useResourceStore } from '../store/resourceStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'Recovery'>;

export default function RecoveryScreen() {
  const route = useRoute<any>();
  const navigation = useNavigation<NavigationProp>();
  const incidentId = route.params?.incidentId;

  const { fetchIncidentDetail, fetchIncidents } = useIncidentStore();
  const { fetchResources } = useResourceStore();

  const [reason, setReason] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleRollback = async () => {
    if (reason.trim().length < 5) {
      Alert.alert("Reason Required", "Please provide a brief explanation for the false alarm.");
      return;
    }

    Alert.alert(
      "Confirm Teardown",
      "This will release all assigned resources, retract pending notifications, and mark the incident as resolved. Are you sure?",
      [
        { text: "Cancel", style: "cancel" },
        { 
          text: "Confirm Rollback", 
          style: "destructive",
          onPress: executeRollback
        }
      ]
    );
  };

  const executeRollback = async () => {
    setIsProcessing(true);
    try {
      await fetchApi(`/recovery/${incidentId}/false-alarm`, {
        method: 'POST',
        body: JSON.stringify({ reason })
      });
      
      // Refresh global state
      await fetchIncidentDetail(incidentId);
      await fetchIncidents();
      await fetchResources();

      Alert.alert(
        "Rollback Complete", 
        "The incident has been resolved and all units returned to available status.",
        [{ text: "OK", onPress: () => navigation.goBack() }]
      );
    } catch (err: any) {
      Alert.alert("Recovery Failed", err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        className="flex-1 px-5 justify-center"
      >
        <View className="bg-red-950/20 border border-red-900/50 p-6 rounded-2xl">
          <View className="items-center mb-6">
            <View className="bg-red-500/20 p-4 rounded-full mb-4">
              <Feather name="alert-octagon" size={48} color="#EF4444" />
            </View>
            <Text className="text-white font-bold text-2xl text-center">False Alarm Rollback</Text>
            <Text className="text-slate-400 text-center mt-2">
              You are about to execute an emergency teardown for this incident. This action is fully audited.
            </Text>
          </View>

          <View className="mb-6">
            <Text className="text-slate-300 font-bold mb-2 text-sm uppercase tracking-wider">Reason for Teardown</Text>
            <TextInput
              className="bg-slate-900 border border-slate-800 text-white p-4 rounded-xl h-24"
              placeholder="e.g., Operator confirmed via CCTV that smoke was from a controlled burn..."
              placeholderTextColor="#475569"
              multiline
              textAlignVertical="top"
              value={reason}
              onChangeText={setReason}
            />
          </View>

          <View className="space-y-4">
            <TouchableOpacity 
              className={`p-4 rounded-xl flex-row justify-center items-center ${isProcessing ? 'bg-red-900/50' : 'bg-red-600'}`}
              onPress={handleRollback}
              disabled={isProcessing}
            >
              {isProcessing ? (
                <ActivityIndicator color="#fff" className="mr-2" />
              ) : (
                <Feather name="power" size={20} color="#fff" className="mr-2" />
              )}
              <Text className="text-white font-bold text-lg">Execute Teardown</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              className="p-4 rounded-xl flex-row justify-center items-center border border-slate-700 bg-slate-900"
              onPress={() => navigation.goBack()}
              disabled={isProcessing}
            >
              <Text className="text-slate-300 font-bold text-lg">Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
