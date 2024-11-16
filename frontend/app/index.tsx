import { useAuth } from "@/provider/AuthProvider";
import { router } from "expo-router";
import {
  ImageBackground,
  SafeAreaView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function Index() {
  const {isAuthenticated} = useAuth()
  const handleLogin = ()=>{
    if(isAuthenticated){
      router.push("/(tabs)/home")
    }
    else{
      router.push("/login")
    }
  }

  return (
    <View className="bg-black h-full w-full">
      <SafeAreaView className="flex w-full h-full">
        <ImageBackground
          className="flex w-full h-full items-center"
          source={require("../assets/images/home-onboarding.jpg")}
        >
          <View className="flex h-full justify-around">
            <View className="flex w-[80%] space-y-2">
              <Text className="text-white text-3xl text-center font-semibold font-[Sora-SemiBold]">
                Fall in Love with Coffee in Blissful Delight!
              </Text>

              <Text className="pt-3 text-[#A2A2A2] text-center font-[Sora-Regular]">
                Welcome to our cozy coffee corner, where every cup is a
                delightful for you.
              </Text>
            </View>
            <View className="flex mt-10">
            <TouchableOpacity
                className="bg-[#C57C3E] mt-10 p-3 rounded-lg items-center"
                onPress = {handleLogin}
              >
                <Text className="text-2xl color-white font-[Sora-SemiBold]">
                  Get Started
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </ImageBackground>
      </SafeAreaView>
    </View>
  );
}
