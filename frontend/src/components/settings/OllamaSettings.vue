<!-- components/settings/OllamaSettings.vue -->
<script setup>
import { ref, watch, onMounted } from 'vue';
import { AlertCircle, Check, Server, List, Loader2 } from 'lucide-vue-next';
import { API_ENDPOINTS } from '@/config/api';
import { ToastService } from '../toast';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';

const emit = defineEmits(['change']);
const uiStore = useUiPreferencesStore();

// State
const baseUrl = ref(uiStore.ollamaSettings.baseUrl);
const isConnected = ref(uiStore.ollamaSettings.isConnected);
const isChecking = ref(false);
const availableModels = ref(uiStore.ollamaSettings.availableModels);
const isLoadingModels = ref(false);
const selectedModel = ref(uiStore.ollamaSettings.selectedModel);

// Watch for changes and update store
watch([baseUrl, selectedModel], () => {
  uiStore.setOllamaSettings({
    baseUrl: baseUrl.value,
    selectedModel: selectedModel.value,
    isConnected: isConnected.value,
    availableModels: availableModels.value
  });
  emit('change');
});

// Check Ollama connectivity
const checkConnectivity = async () => {
  isChecking.value = true;
  try {
    // Include base_url as query parameter
    const url = new URL(API_ENDPOINTS.ollama.status);
    url.searchParams.append('base_url', baseUrl.value);
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.success) {
      isConnected.value = data.data.is_connected;
      uiStore.updateOllamaConnection(isConnected.value);
      
      if (isConnected.value) {
        ToastService.success('Successfully connected to Ollama');
        await fetchAvailableModels();
      } else {
        ToastService.warning('Could not connect to Ollama server');
      }
    } else {
      throw new Error(data.error?.message || 'Failed to connect to Ollama');
    }
  } catch (error) {
    console.error('Failed to check Ollama status:', error);
    isConnected.value = false;
    uiStore.updateOllamaConnection(false);
    ToastService.error(error.message || 'Failed to connect to Ollama server');
  } finally {
    isChecking.value = false;
  }
};

const fetchAvailableModels = async () => {
  if (!isConnected.value) return;
  
  isLoadingModels.value = true;
  try {
    const url = new URL(API_ENDPOINTS.ollama.models);
    url.searchParams.append('base_url', baseUrl.value);
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.success) {
      availableModels.value = data.data.models;
      uiStore.setOllamaModels(availableModels.value);
    } else {
      throw new Error(data.error?.message || 'Failed to fetch models');
    }
  } catch (error) {
    console.error('Failed to fetch Ollama models:', error);
    ToastService.error(error.message || 'Failed to fetch available models');
    availableModels.value = [];
    uiStore.setOllamaModels([]);
  } finally {
    isLoadingModels.value = false;
  }
};

const handleModelSelect = (model) => {
  selectedModel.value = model;
};

// Initialize on component mount
onMounted(async () => {
  baseUrl.value = uiStore.ollamaSettings.baseUrl;
  selectedModel.value = uiStore.ollamaSettings.selectedModel;
  isConnected.value = uiStore.ollamaSettings.isConnected;
  availableModels.value = uiStore.ollamaSettings.availableModels;
  
  if (!isConnected.value) {
    await checkConnectivity();
  }
});
</script>

<template>
  <section class="space-y-6">
    <!-- Section Header -->
    <div class="flex items-center gap-2">
      <Server class="w-5 h-5 text-accent-400 dark:text-accent-300" />
      <h2 class="text-lg font-semibold text-primary-500 dark:text-primary-100">
        Ollama Settings
      </h2>
    </div>

    <!-- Connection Settings -->
    <div class="bg-white dark:bg-primary-800 rounded-lg border border-neutral-200 dark:border-primary-700 p-5">
      <!-- Base URL Input -->
      <div class="space-y-2">
        <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">
          Base URL
        </label>
        <div class="relative flex space-x-2">
          <input
            v-model="baseUrl"
            type="text"
            placeholder="http://localhost:11434"
            class="flex-grow px-4 py-2.5 bg-white dark:bg-primary-700 border border-neutral-200 dark:border-neutral-600 rounded-lg text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 focus:border-transparent transition-all text-sm"
          />
          <button
            @click="checkConnectivity"
            class="px-4 py-2 rounded-lg flex items-center gap-2 font-medium transition-colors"
            :class="[
              isConnected 
                ? 'bg-green-50 text-green-600 dark:bg-green-900/50 dark:text-green-400'
                : 'bg-neutral-50 text-neutral-600 dark:bg-primary-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-primary-600'
            ]"
            :disabled="isChecking"
          >
            <Loader2 v-if="isChecking" class="w-4 h-4 animate-spin" />
            <Check v-else-if="isConnected" class="w-4 h-4" />
            <AlertCircle v-else class="w-4 h-4" />
            {{ isChecking ? 'Checking...' : isConnected ? 'Connected' : 'Check Connection' }}
          </button>
        </div>
      </div>

      <!-- Available Models -->
      <div class="mt-6">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <List class="w-4 h-4 text-neutral-500 dark:text-neutral-400" />
            <h3 class="text-sm font-medium text-neutral-700 dark:text-neutral-300">
              Available Models
            </h3>
          </div>
          <button 
            v-if="isConnected"
            @click="fetchAvailableModels"
            class="text-sm text-accent-400 hover:text-accent-500 dark:text-accent-300 dark:hover:text-accent-200"
          >
            Refresh
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="isLoadingModels" class="py-8">
          <div class="flex justify-center items-center text-neutral-500 dark:text-neutral-400">
            <Loader2 class="w-5 h-5 animate-spin mr-2" />
            Loading models...
          </div>
        </div>

        <!-- No Connection State -->
        <div 
          v-else-if="!isConnected"
          class="py-8 text-center text-neutral-500 dark:text-neutral-400"
        >
          <AlertCircle class="w-5 h-5 mx-auto mb-2" />
          Connect to Ollama server to view available models
        </div>

        <!-- Models List -->
        <div 
          v-else-if="availableModels.length > 0" 
          class="divide-y divide-neutral-100 dark:divide-primary-700"
        >
          <div
            v-for="model in availableModels"
            :key="model"
            class="py-3 px-4 first:rounded-t-lg last:rounded-b-lg hover:bg-neutral-50 dark:hover:bg-primary-700/50 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="font-medium text-neutral-900 dark:text-neutral-100">
                {{ model }}
              </div>
            </div>
          </div>
        </div>

        <!-- No Models State -->
        <div 
          v-else
          class="py-8 text-center text-neutral-500 dark:text-neutral-400"
        >
          No models found on Ollama server
        </div>
      </div>
    </div>

    <!-- Info Text -->
    <div class="text-sm text-neutral-500 dark:text-neutral-400 flex items-start gap-2">
      <AlertCircle class="w-4 h-4 mt-0.5 flex-shrink-0" />
      <p class="text-neutral-500 dark:text-neutral-400">
        Ollama server needs to be running locally or accessible at the specified base URL. 
        Visit <a 
          href="https://ollama.ai" 
          target="_blank" 
          rel="noopener" 
          class="text-accent-400 hover:text-accent-500 dark:text-accent-300 dark:hover:text-accent-200"
        >
          ollama.ai
        </a> 
        for installation instructions.
      </p>
    </div>
  </section>
</template>