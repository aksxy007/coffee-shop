import { Image, Text, View } from "react-native";
import React, { useEffect, useState } from "react";
import { Product, ProductCategory } from "@/types/types";
import { fetchProducts } from "@/services/productService";
import {
  GestureHandlerRootView,
  TouchableOpacity,
  FlatList,
} from "react-native-gesture-handler";
import { SafeAreaView } from "react-native-safe-area-context";
import FontAwesome6 from "@expo/vector-icons/FontAwesome6";
import SearchArea from "@/components/SearchArea";
import GetLocation, {
  Location,
  LocationErrorCode,
  isLocationError,
} from "react-native-get-location";
import Banner from "@/components/Banner";
import { router } from "expo-router";
import { useCart } from "@/components/CartContext";
import Toast from "react-native-root-toast";

const home = () => {
  const {addToCart} = useCart();

  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState<Location | null>(null);
  const [locationError, setLocationError] = useState<LocationErrorCode | null>(
    null
  );
  const [shownProducts, setShownProducts] = useState<Product[]>([]);
  const [productCategories, setProductCatgories] = useState<ProductCategory[]>(
    []
  );
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [error, setError] = useState<string | null>(null);

  const requestLocation = () => {
    setLoading(true);
    setLocation(null);
    setLocationError(null);

    GetLocation.getCurrentPosition({
      enableHighAccuracy: true,
      timeout: 30000,
      rationale: {
        title: "Location permission",
        message: "The app needs the permission to request your location.",
        buttonPositive: "Ok",
      },
    })
      .then((newLocation) => {
        setLoading(false);
        setLocation(newLocation);
      })
      .catch((ex) => {
        if (isLocationError(ex)) {
          const { code, message } = ex;
          console.warn(code, message);
          setLocationError(code);
        } else {
          console.warn(ex);
        }
        setLoading(false);
        setLocation(null);
      });
  };

  useEffect(() => {
    const uniqueCategories = Array.from(productCategories).map((category) => ({
      id: category.id,
      selected: selectedCategory === category.id,
    }));
    setProductCatgories(uniqueCategories);

    if (selectedCategory === "All") {
      setShownProducts(products);
    } else {
      const filteredProducts = products.filter(
        (product) => product.category === selectedCategory
      );
      setShownProducts(filteredProducts);
    }
  }, [selectedCategory]);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const productsData = await fetchProducts();
        const categories = productsData.map((product) => product.category);
        categories.unshift("All");
        const uniqueCategories = Array.from(new Set(categories)).map(
          (category) => ({
            id: category,
            selected: selectedCategory === category,
          })
        );
        setShownProducts(productsData);
        setProductCatgories(uniqueCategories);
        setProducts(productsData);
      } catch (error) {
        console.error(error);
        setError("Error fetching products" + error);
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
    // if(!location)
    //     requestLocation();
  }, []);

  if (loading) {
    return <Text>Loading...</Text>;
  }
  if (error) return <Text>{error}</Text>;

  const addButton = (name:string) => {
    addToCart(name, 1);
    Toast.show(`${name} added to cart`, {
      duration: Toast.durations.SHORT,
    });

    console.log("here")
  };

  return (
    <GestureHandlerRootView className="h-full">
      <SafeAreaView className="w-full h-full">
        <FlatList
          horizontal={false}
          numColumns={2}
          columnWrapperStyle={{
            justifyContent: "space-between",
            marginLeft: 15,
            marginRight: 15,
          }}
          keyExtractor={(item, index) => index.toString()}
          data={shownProducts}
          renderItem={({ item }) => (
            <View className="w-[48%] mt-2 bg-white rounded-2xl p-2 flex justify-between">
              <TouchableOpacity
                onPress={() =>
                  router.push({
                    pathname: "/details",
                    params: {
                      name: item.name,
                      type: item.category,
                      price: item.price,
                      rating: item.rating,
                      description: item.description,
                      imageUrl: item.image_url,
                    },
                  })
                }
              >
                <Image
                  className="w-full h-32 rounded-2xl"
                  source={{ uri: item.image_url }}
                />
                <Text className="text-[#242424] text-lg font-[Sora-Semibold] ml-1 ">
                  {item.name}
                </Text>
                <Text className="text-[#a2a2a2] text-sm font-[Sora-Regular] ml-1 ">
                  {item.category}
                </Text>
              </TouchableOpacity>

              <View
                className="flex flex-row justify-between items-center ml-1 mt-5 mb-2
                    "
              >
                <Text className="text-[#050505] text-lg font-[Sora-Semibold] ">
                  ${item.price}
                </Text>
                <TouchableOpacity onPress = {() => addButton(item.name)}>
                  <View className="mr-2 p-2 bg-app_orange_color rounded-xl">
                    <FontAwesome6 name="add" size={24} color="white" />
                  </View>
                </TouchableOpacity>
              </View>
            </View>
          )}
          ListHeaderComponent={() => (
            <View className="flex">
              <SearchArea />
              <Banner />
              <View className="flex items-center">
                <FlatList
                  className="mt-6 w-[90%] mb-2"
                  data={productCategories}
                  horizontal={true}
                  renderItem={({ item }) => (
                    <TouchableOpacity
                      onPress={() => setSelectedCategory(item.id)}
                    >
                      <Text
                        className={`text-sm mr-4 font-[Sora-Regular] p-3 rounded-lg 
                        ${item.selected ? "text-white" : "text-[#313131]"}
                        ${
                          item.selected
                            ? "bg-app_orange_color "
                            : "bg-[#EDEDED] "
                        }
                        `}
                      >
                        {item.id}
                      </Text>
                    </TouchableOpacity>
                  )}
                />
              </View>
            </View>
          )}
        />
      </SafeAreaView>
    </GestureHandlerRootView>
  );
};

export default home;
