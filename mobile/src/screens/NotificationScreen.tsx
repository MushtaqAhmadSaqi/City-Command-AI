import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, RefreshControl, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useRoute } from '@react-navigation/native';

import { useNotificationStore } from '../store/notificationStore';

export default function NotificationScreen() {
  const route = useRoute<any>();
  const incidentId = route.params?.incidentId;

  const { notifications, fetchNotifications, draftNotifications, updateStatus, isLoading } = useNotificationStore();
  const [isDrafting, setIsDrafting] = useState(false);

  useEffect(() => {
    if (incidentId) {
      fetchNotifications(incidentId);
    }
  }, [incidentId]);

  const onRefresh = React.useCallback(() => {
    if (incidentId) fetchNotifications(incidentId);
  }, [incidentId]);

  const handleDraft = async () => {
    setIsDrafting(true);
    try {
      await draftNotifications(incidentId);
    } catch (err: any) {
      Alert.alert('Drafting Failed', err.message);
    } finally {
      setIsDrafting(false);
    }
  };

  const handleAction = async (notifId: string, action: 'approve' | 'send' | 'retract') => {
    const targetStatus = action === 'approve' ? 'approved' : action === 'send' ? 'sent' : 'retracted';
    try {
      await updateStatus(notifId, targetStatus, incidentId);
    } catch (err: any) {
      Alert.alert('Update Failed', err.message);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'text-slate-400 bg-slate-800';
      case 'approved': return 'text-emerald-400 bg-emerald-500/20 border border-emerald-500/30';
      case 'sent': return 'text-sky-400 bg-sky-500/20 border border-sky-500/30';
      case 'retracted': return 'text-red-400 bg-red-500/20 border border-red-500/30';
      default: return 'text-slate-400';
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-slate-950" edges={['bottom', 'left', 'right']}>
      <ScrollView 
        className="flex-1 px-4"
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={onRefresh} tintColor="#10B981" />}
      >
        <Text className="text-white font-bold text-xl mt-4 mb-2">Stakeholder Notifications</Text>
        <Text className="text-slate-400 text-sm mb-6">
          Review, approve, and dispatch targeted messaging drafted by the AI for different audiences.
        </Text>

        {notifications.length === 0 ? (
          <View className="bg-slate-900 border border-slate-800 p-8 rounded-xl items-center mt-4">
            <Feather name="message-square" size={48} color="#334155" />
            <Text className="text-slate-300 font-bold mt-4 mb-2">No Drafts Generated</Text>
            <Text className="text-slate-500 text-center mb-6">
              The AI has not drafted messages for this incident yet.
            </Text>
            <TouchableOpacity 
              className={`flex-row items-center px-6 py-3 rounded-lg ${isDrafting ? 'bg-emerald-900/50' : 'bg-emerald-600'}`}
              onPress={handleDraft}
              disabled={isDrafting}
            >
              {isDrafting ? <ActivityIndicator color="#fff" className="mr-2" /> : <Feather name="cpu" size={18} color="#fff" className="mr-2" />}
              <Text className="text-white font-bold">{isDrafting ? 'Drafting...' : 'Trigger AI Drafter'}</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View className="mb-10">
            {notifications.map(notif => (
              <View key={notif.id} className="bg-slate-900 border border-slate-800 rounded-xl mb-4 overflow-hidden">
                <View className="p-4 border-b border-slate-800/50 flex-row justify-between items-center">
                  <View>
                    <Text className="text-slate-300 font-bold uppercase tracking-wider text-xs mb-1">
                      {notif.audience.replace('_', ' ')}
                    </Text>
                    <View className="flex-row items-center">
                      <Feather name="radio" size={12} color="#64748B" className="mr-1" />
                      <Text className="text-slate-500 text-xs">{notif.channel}</Text>
                    </View>
                  </View>
                  <View className={`px-2 py-1 rounded ${getStatusColor(notif.status)}`}>
                    <Text className="font-bold text-xs uppercase">{notif.status}</Text>
                  </View>
                </View>

                <View className="p-4">
                  <Text className="text-slate-300 leading-5 text-sm">{notif.message}</Text>
                  
                  {notif.requires_approval && notif.status === 'draft' && (
                    <View className="mt-4 flex-row items-center">
                      <Feather name="shield" size={14} color="#F59E0B" className="mr-2" />
                      <Text className="text-amber-500 text-xs font-bold uppercase tracking-widest">Operator Approval Required</Text>
                    </View>
                  )}
                </View>

                <View className="bg-slate-950 p-3 flex-row justify-end space-x-3">
                  {notif.status !== 'sent' && notif.status !== 'retracted' && (
                    <TouchableOpacity 
                      onPress={() => handleAction(notif.id, 'retract')}
                      className="px-4 py-2"
                    >
                      <Text className="text-slate-500 font-bold">Discard</Text>
                    </TouchableOpacity>
                  )}
                  
                  {notif.status === 'draft' && (
                    <TouchableOpacity 
                      onPress={() => handleAction(notif.id, notif.requires_approval ? 'approve' : 'send')}
                      className="bg-emerald-600 px-4 py-2 rounded-lg"
                    >
                      <Text className="text-white font-bold">{notif.requires_approval ? 'Approve' : 'Send Now'}</Text>
                    </TouchableOpacity>
                  )}

                  {notif.status === 'approved' && (
                    <TouchableOpacity 
                      onPress={() => handleAction(notif.id, 'send')}
                      className="bg-sky-500 px-4 py-2 rounded-lg flex-row items-center"
                    >
                      <Feather name="send" size={14} color="#fff" className="mr-2" />
                      <Text className="text-white font-bold">Dispatch Message</Text>
                    </TouchableOpacity>
                  )}
                </View>
              </View>
            ))}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
