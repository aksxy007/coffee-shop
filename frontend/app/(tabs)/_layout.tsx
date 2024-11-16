import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { Tabs } from "expo-router";
import Entypo from "@expo/vector-icons/Entypo";
import Ionicons from '@expo/vector-icons/Ionicons';

const TabsLayout = () => {
  return (
    <>
      <Tabs
        screenOptions={{
          tabBarActiveTintColor: "#C67C4E",
        }}
      >
        <Tabs.Screen
          name="home"
          options={{
            headerShown: false,
            title: "Home",
            tabBarIcon: ({ color }) => (
              <Entypo name="home" size={24} color={color} />
            ),
          }}
        />
        <Tabs.Screen
          name="order"
          options={{ headerShown: true, title: "Cart",tabBarIcon: ({ color }) => (
            <Entypo name="shopping-cart" size={24} color={color} />
          ), }}
        />
        <Tabs.Screen
          name="chatRoom"
          options={{ headerShown: true, title: "Chat" ,tabBarIcon: ({ color }) => (
            <Ionicons name="chatbox-ellipses" size={24} color={color} />
          ),}}
        />
      </Tabs>
    </>
  );
};

export default TabsLayout;
