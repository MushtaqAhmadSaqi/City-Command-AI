import React, { useEffect } from 'react';
import { View, Text, Animated, Easing } from 'react-native';
import { Feather } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'Splash'>;

export default function SplashScreen() {
  const navigation = useNavigation<NavigationProp>();
  const pulseAnim = new Animated.Value(0.8);
  const opacityAnim = new Animated.Value(0);

  useEffect(() => {
    // Pulse animation for the logo
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.1,
          duration: 1000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 0.8,
          duration: 1000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        })
      ])
    ).start();

    // Fade in text
    Animated.timing(opacityAnim, {
      toValue: 1,
      duration: 800,
      delay: 400,
      useNativeDriver: true,
    }).start();

    // Auto-navigate to MainTabs after 2.5 seconds
    const timer = setTimeout(() => {
      navigation.replace('MainTabs');
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View className="flex-1 bg-slate-950 justify-center items-center">
      <Animated.View style={{ transform: [{ scale: pulseAnim }] }} className="bg-sky-500/20 p-6 rounded-full border border-sky-500/30 mb-6">
        <Feather name="globe" size={64} color="#38BDF8" />
      </Animated.View>

      <Animated.View style={{ opacity: opacityAnim }} className="items-center">
        <Text className="text-white font-bold text-3xl tracking-widest uppercase mb-2">CityCommand</Text>
        <Text className="text-sky-400 font-bold text-sm tracking-[0.3em] uppercase">AI Orchestrator</Text>
        
        <View className="flex-row items-center mt-12">
          <View className="w-1.5 h-1.5 bg-emerald-500 rounded-full mr-2 animate-ping" />
          <Text className="text-slate-500 text-xs tracking-widest uppercase">Connecting to Grid...</Text>
        </View>
      </Animated.View>
    </View>
  );
}
