// React Native/Expo Recipe Detail Screen
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  ScrollView,
  TouchableOpacity,
  Alert,
  TextInput
} from 'react-native';
import { recipesAPI, cartAPI } from '../expo-api-service';

export default function RecipeDetailScreen({ route, navigation }) {
  const { recipeId } = route.params;
  const [recipe, setRecipe] = useState(null);
  const [pricing, setPricing] = useState(null);
  const [people, setPeople] = useState(1);
  const [loading, setLoading] = useState(true);
  const [addingToCart, setAddingToCart] = useState(false);

  useEffect(() => {
    loadRecipe();
  }, [recipeId]);

  useEffect(() => {
    if (recipe) {
      loadPricing();
    }
  }, [recipe, people]);

  const loadRecipe = async () => {
    try {
      setLoading(true);
      const recipeData = await recipesAPI.getById(recipeId);
      setRecipe(recipeData);
    } catch (error) {
      Alert.alert('Error', error.message);
      navigation.goBack();
    } finally {
      setLoading(false);
    }
  };

  const loadPricing = async () => {
    try {
      const pricingData = await recipesAPI.getWithPricing(recipeId, people);
      setPricing(pricingData);
    } catch (error) {
      console.log('Error loading pricing:', error);
    }
  };

  const addToCart = async () => {
    if (!recipe) return;

    try {
      setAddingToCart(true);
      await cartAPI.addItem({
        recipe_id: recipe.id,
        quantity: people,
        price: pricing?.calculated_price || recipe.base_price
      });
      Alert.alert('Success', 'Recipe added to cart!');
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setAddingToCart(false);
    }
  };

  const adjustPeople = (change) => {
    const newPeople = people + change;
    if (newPeople >= 1 && newPeople <= 20) {
      setPeople(newPeople);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Loading recipe...</Text>
      </View>
    );
  }

  if (!recipe) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Recipe not found</Text>
        <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
          <Text style={styles.buttonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{recipe.name}</Text>
        <Text style={styles.category}>{recipe.category?.name}</Text>
        <View style={styles.difficultyContainer}>
          <Text style={styles.difficultyLabel}>Difficulty:</Text>
          <Text style={[styles.difficulty, styles[`difficulty${recipe.difficulty.charAt(0).toUpperCase() + recipe.difficulty.slice(1)}`]]}>
            {recipe.difficulty}
          </Text>
        </View>
      </View>

      <View style={styles.descriptionContainer}>
        <Text style={styles.descriptionTitle}>Description</Text>
        <Text style={styles.description}>{recipe.description}</Text>
      </View>

      <View style={styles.pricingContainer}>
        <Text style={styles.pricingTitle}>Pricing</Text>
        
        <View style={styles.peopleSelector}>
          <Text style={styles.peopleLabel}>Number of People:</Text>
          <View style={styles.peopleControls}>
            <TouchableOpacity 
              style={styles.peopleButton} 
              onPress={() => adjustPeople(-1)}
              disabled={people <= 1}
            >
              <Text style={styles.peopleButtonText}>-</Text>
            </TouchableOpacity>
            
            <TextInput
              style={styles.peopleInput}
              value={people.toString()}
              onChangeText={(text) => {
                const num = parseInt(text);
                if (!isNaN(num) && num >= 1 && num <= 20) {
                  setPeople(num);
                }
              }}
              keyboardType="numeric"
            />
            
            <TouchableOpacity 
              style={styles.peopleButton} 
              onPress={() => adjustPeople(1)}
              disabled={people >= 20}
            >
              <Text style={styles.peopleButtonText}>+</Text>
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.priceInfo}>
          <Text style={styles.basePrice}>Base Price: ${recipe.base_price}</Text>
          {pricing && (
            <Text style={styles.totalPrice}>
              Total for {people} {people === 1 ? 'person' : 'people'}: ${pricing.calculated_price}
            </Text>
          )}
        </View>
      </View>

      <View style={styles.actionsContainer}>
        <TouchableOpacity 
          style={[styles.addToCartButton, addingToCart && styles.buttonDisabled]} 
          onPress={addToCart}
          disabled={addingToCart}
        >
          {addingToCart ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.addToCartText}>Add to Cart</Text>
          )}
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    color: '#666',
    marginBottom: 20,
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  category: {
    fontSize: 16,
    color: '#007AFF',
    marginBottom: 10,
  },
  difficultyContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  difficultyLabel: {
    fontSize: 16,
    color: '#666',
    marginRight: 10,
  },
  difficulty: {
    fontSize: 16,
    fontWeight: '600',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  difficultyEasy: {
    backgroundColor: '#d4edda',
    color: '#155724',
  },
  difficultyMedium: {
    backgroundColor: '#fff3cd',
    color: '#856404',
  },
  difficultyHard: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
  },
  descriptionContainer: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  descriptionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  description: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  pricingContainer: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  pricingTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  peopleSelector: {
    marginBottom: 20,
  },
  peopleLabel: {
    fontSize: 16,
    color: '#333',
    marginBottom: 10,
  },
  peopleControls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  peopleButton: {
    backgroundColor: '#007AFF',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  peopleButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  peopleInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 10,
    marginHorizontal: 15,
    width: 60,
    textAlign: 'center',
    fontSize: 16,
  },
  priceInfo: {
    alignItems: 'center',
  },
  basePrice: {
    fontSize: 16,
    color: '#666',
    marginBottom: 5,
  },
  totalPrice: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#28a745',
  },
  actionsContainer: {
    padding: 20,
  },
  addToCartButton: {
    backgroundColor: '#28a745',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  addToCartText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

