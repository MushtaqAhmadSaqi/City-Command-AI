import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { View, Text } from 'react-native';

const DummyScreen = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0F172A' }}>
    <Text style={{ color: 'white' }}>CityCommand AI Loading...</Text>
  </View>
);

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <DummyScreen />
    </NavigationContainer>
  );
}
export {};
