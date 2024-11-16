// screens/LoginScreen.js
import { router } from 'expo-router';
import React, { useState } from 'react';
import { View, Text, TextInput, Button, TouchableOpacity, Image, ImageBackground, Alert } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useAuth } from '@/provider/AuthProvider';
import axios from 'axios';

export default function LoginScreen() {
  const {setIsAuthenticated} = useAuth()
  const [username,setUsername] = useState('')
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      const response = await axios.post("http://192.168.29.13:8000/auth/register", {
        username,
        email,
        password
      });

      console.log("register res",response.data)
      router.push("/login"); // Navigate to the next screen after successful login
    } catch (error) {
        console.error(error)
      Alert.alert("Registration Failed");
    }
  };

  return (
    <View className="h-full w-full bg-white">
        
        <ImageBackground className='h-full w-full absolute' source={require("../assets/images/index_bg_image.png")} blurRadius={2}/>
        <View className='h-full w-full flex justify-center items-center pt-40 pb-2'>
        <TouchableOpacity onPress={() => router.back()} className="absolute m-2 top-10 left-4">
      <Ionicons name="arrow-back" size={24} color="white" />
        </TouchableOpacity>
            <View className='flex items-center space-y-4 px-6 w-full h-[60%] justify-end'>

            <View className='flex items-center'>
            <Text className='text-white font-bold font-[Sora-Regular] tracking-wider text-5xl'>
                Register
            </Text>
            </View>
            <View className='bg-white p-5 rounded-2xl mt-6 w-full'>
            <TextInput
              placeholder='Username'
              placeholderTextColor={'gray'}
              value={username}
              onChangeText={setUsername}
              className="text-black"
            />
                </View>
                <View className='bg-white p-5 rounded-2xl mt-6 w-full'>
                <TextInput
              placeholder='Email'
              placeholderTextColor={'gray'}
              value={email}
              onChangeText={setEmail}
              className="text-black"
            />
                </View>
                <View className='bg-white p-5 rounded-2xl mt-6 w-full'>
                <TextInput
              placeholder='Password'
              placeholderTextColor={'gray'}
              value={password}
              onChangeText={setPassword}
              className="text-black"
            />
                </View>
                <View className='w-full'>
                    <TouchableOpacity className='w-full bg-app_orange_color p-3 rounded-2xl mb-3' onPress={handleRegister}>
                        <Text className='text-xl font-[Sora-SemiBold] text-white text-center p-1'>
                            Register
                        </Text>
                    </TouchableOpacity>
                </View>
                <View className='flex-row justify-center'>
                    <Text className='text-white'>
                        Already have an account? 
                    </Text>
                    <TouchableOpacity onPress={()=> router.push("/login")}>
                        <Text className='text-app_orange_color'>
                            Sign In
                        </Text>
                    </TouchableOpacity>
                </View>
            </View>
            
        </View>
    </View>
  );
}
