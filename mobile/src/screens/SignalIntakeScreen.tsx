import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator, Alert, KeyboardAvoidingView, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { useSignalStore } from '../store/signalStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'SignalIntake'>;

export default function SignalIntakeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { submitSignal } = useSignalStore();

  const [text, setText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Default to Islamabad coordinates for the hackathon demo
  const [lat, setLat] = useState('33.6844');
  const [lng, setLng] = useState('73.0479');

  const handleSubmit = async () => {
    if (text.trim().length < 10) {
      Alert.alert("Input Too Short", "Please provide a more detailed description of the incident.");
      return;
    }

    setIsSubmitting(true);
    try {
      await submitSignal(text, parseFloat(lat), parseFloat(lng));
      Alert.alert(
        "Signal Submitted", 
        "The signal has been ingested and the AI pipeline is processing it.",
        [{ text: "OK", onPress: () => navigation.goBack() }]
      );
    } catch (err: any) {
      Alert.alert("Submission Failed", err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        className="flex-1 px-5 justify-center"
      >
        <View className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
          <View className="items-center mb-6">
            <View className="bg-sky-500/20 p-4 rounded-full mb-4 border border-sky-500/30">
              <Feather name="radio" size={48} color="#38BDF8" />
            </View>
            <Text className="text-white font-bold text-2xl text-center">Manual Signal Intake</Text>
            <Text className="text-slate-400 text-center mt-2">
              Inject a raw text signal into the system to test the AI orchestrator's response.
            </Text>
          </View>

          <View className="mb-4">
            <Text className="text-slate-300 font-bold mb-2 text-sm uppercase tracking-wider">Raw Text Description</Text>
            <TextInput
              className="bg-slate-950 border border-slate-800 text-white p-4 rounded-xl h-24"
              placeholder="e.g., Heavy smoke and fire visible from the 3rd floor of the Centaurus Mall..."
              placeholderTextColor="#475569"
              multiline
              textAlignVertical="top"
              value={text}
              onChangeText={setText}
            />
          </View>

          <View className="flex-row space-x-4 mb-6">
            <View className="flex-1 mr-2">
              <Text className="text-slate-300 font-bold mb-2 text-xs uppercase tracking-wider">Latitude</Text>
              <TextInput
                className="bg-slate-950 border border-slate-800 text-white p-3 rounded-xl"
                keyboardType="numeric"
                value={lat}
                onChangeText={setLat}
              />
            </View>
            <View className="flex-1 ml-2">
              <Text className="text-slate-300 font-bold mb-2 text-xs uppercase tracking-wider">Longitude</Text>
              <TextInput
                className="bg-slate-950 border border-slate-800 text-white p-3 rounded-xl"
                keyboardType="numeric"
                value={lng}
                onChangeText={setLng}
              />
            </View>
          </View>

          <View className="space-y-4">
            <TouchableOpacity 
              className={`p-4 rounded-xl flex-row justify-center items-center ${isSubmitting ? 'bg-sky-900/50' : 'bg-sky-600'}`}
              onPress={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <ActivityIndicator color="#fff" className="mr-2" />
              ) : (
                <Feather name="send" size={20} color="#fff" className="mr-2" />
              )}
              <Text className="text-white font-bold text-lg">Inject Signal</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              className="p-4 rounded-xl flex-row justify-center items-center border border-slate-700 bg-slate-950"
              onPress={() => navigation.goBack()}
              disabled={isSubmitting}
            >
              <Text className="text-slate-400 font-bold text-lg">Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
