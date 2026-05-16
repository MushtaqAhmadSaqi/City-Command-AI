import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { useIncidentStore } from '../store/incidentStore';
import { RootStackParamList } from '../navigation/types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList, 'MainTabs'>;

export default function IncidentsScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { incidents, fetchIncidents, isLoading } = useIncidentStore();
  const [filter, setFilter] = useState<'active' | 'resolved'>('active');

  const onRefresh = React.useCallback(() => {
    fetchIncidents();
  }, []);

  const filteredIncidents = incidents
    .filter(i => (filter === 'active' ? i.status !== 'resolved' : i.status === 'resolved'))
    .sort((a, b) => {
      // Sort by priority_score DESC, then date DESC
      const diff = (b.priority_score || 0) - (a.priority_score || 0);
      if (diff !== 0) return diff;
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });

  const renderItem = ({ item }: { item: any }) => {
    const isCritical = item.severity === 'CRITICAL';
    const isHigh = item.severity === 'HIGH';

    return (
      <TouchableOpacity 
        className="bg-slate-900 mb-3 rounded-xl border border-slate-800 overflow-hidden"
        onPress={() => navigation.navigate('IncidentDetail', { incidentId: item.id })}
      >
        <View className="flex-row">
          <View className={`w-3 ${isCritical ? 'bg-red-500' : isHigh ? 'bg-orange-500' : 'bg-yellow-500'}`} />
          <View className="flex-1 p-4">
            <View className="flex-row justify-between items-start mb-2">
              <Text className="text-white font-bold text-lg flex-1 mr-2">{item.title}</Text>
              <View className={`px-2 py-1 rounded ${isCritical ? 'bg-red-500/20' : 'bg-slate-800'}`}>
                <Text className={`text-xs font-bold ${isCritical ? 'text-red-400' : 'text-slate-300'}`}>
                  {item.severity}
                </Text>
              </View>
            </View>
            
            <View className="flex-row items-center mb-3">
              <Feather name="map-pin" size={14} color="#64748B" />
              <Text className="text-slate-400 text-sm ml-1">{item.location?.area || 'Unknown Area'}</Text>
            </View>

            <View className="flex-row items-center justify-between border-t border-slate-800/50 pt-3">
              <Text className="text-slate-500 text-xs">
                Score: {item.priority_score?.toFixed(1) || 'N/A'}
              </Text>
              {item.human_review_required && (
                <View className="flex-row items-center">
                  <Feather name="eye" size={12} color="#F59E0B" />
                  <Text className="text-amber-500 text-xs ml-1 font-bold">Needs Review</Text>
                </View>
              )}
            </View>
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950 px-4">
      <View className="py-4">
        <Text className="text-white font-bold text-2xl mb-4">Incidents</Text>
        
        {/* Toggle Filter */}
        <View className="flex-row bg-slate-900 p-1 rounded-lg border border-slate-800 mb-4">
          <TouchableOpacity 
            className={`flex-1 py-2 rounded-md items-center ${filter === 'active' ? 'bg-slate-800' : ''}`}
            onPress={() => setFilter('active')}
          >
            <Text className={`font-bold ${filter === 'active' ? 'text-white' : 'text-slate-500'}`}>Active</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            className={`flex-1 py-2 rounded-md items-center ${filter === 'resolved' ? 'bg-slate-800' : ''}`}
            onPress={() => setFilter('resolved')}
          >
            <Text className={`font-bold ${filter === 'resolved' ? 'text-white' : 'text-slate-500'}`}>Resolved</Text>
          </TouchableOpacity>
        </View>
      </View>

      <FlatList
        data={filteredIncidents}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 20 }}
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={onRefresh} tintColor="#38BDF8" />}
        ListEmptyComponent={
          <View className="py-10 items-center">
            <Feather name="inbox" size={48} color="#334155" />
            <Text className="text-slate-400 mt-4 text-center">No {filter} incidents found.</Text>
          </View>
        }
      />
    </SafeAreaView>
  );
}
