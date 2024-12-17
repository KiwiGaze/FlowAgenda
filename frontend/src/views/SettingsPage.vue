<!--views/SettingsView.vue-->
<script setup>
import { ref, onMounted, computed } from 'vue';
import { Settings, Moon, Globe, Cpu, ChevronDown} from 'lucide-vue-next';
import { useRouter, useRoute } from 'vue-router';
import AppearanceSettings from '../components/settings/AppearanceSettings.vue';
import OllamaSettings from '../components/settings/OllamaSettings.vue';
import { ToastService } from '../components/toast';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';
import OllamaIcon from '../components/icons/OllamaIcon.vue';

const router = useRouter();
const route = useRoute();
const uiStore = useUiPreferencesStore();
const isMenuOpen = ref(false);

// Reactive loading state
const isSaving = computed(() => uiStore.isSaving);

// Get component key for dynamic component rendering
const getComponentKey = (tab) => `settings-${tab}`;

// Get initial active tab from route query or default to 'model'
const activeTab = ref(route.query.tab || 'ollama');

const tabs = [
  { 
    id: 'ollama', 
    name: 'Ollama', 
    icon: OllamaIcon,
    description: 'Configure Ollama model settings and connectivity'
  },
  { 
    id: 'appearance', 
    name: 'Appearance', 
    icon: Moon,
    description: 'Customize the application theme and visual preferences'
  }
];

const handleSettingsChange = async () => {
  try {
    await uiStore.saveSettings();
    ToastService.success('Settings saved successfully');
  } catch (error) {
    ToastService.error('Failed to save settings');
    console.error('Settings save error:', error);
  }
};

const setActiveTab = async (tabId) => {
  activeTab.value = tabId;
  isMenuOpen.value = false;
  
  // Update URL query parameter when tab changes
  await router.replace({ 
    query: { 
      ...route.query,
      tab: tabId 
    } 
  });
};

// Initialize active tab from URL on mount
onMounted(async () => {
  // If there's a tab in the URL, use it
  if (route.query.tab && tabs.some(tab => tab.id === route.query.tab)) {
    activeTab.value = route.query.tab;
  } else {
    // If no valid tab in URL, set default and update URL
    await setActiveTab('ollama');
  }
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 dark:bg-primary-900 transition-colors duration-300">
    <div class="max-w-5xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-bold text-primary-500 dark:text-primary-100 flex items-center gap-2">
          <Settings class="w-6 h-6" />
          Settings
        </h1>

        <!-- Auto-save indicator -->
        <div v-if="isSaving" class="flex items-center gap-2 text-sm text-neutral-500 dark:text-neutral-400">
          <svg class="animate-spin w-4 h-4" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Saving...
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="mb-6">
        <!-- Desktop Navigation -->
        <nav class="hidden sm:flex space-x-4 border-b border-neutral-200 dark:border-primary-700">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="setActiveTab(tab.id)"
            class="flex items-center gap-2 px-4 py-3 -mb-px text-sm font-medium
                   border-b-2 transition-colors duration-200"
            :class="[
              activeTab === tab.id
                ? 'text-accent-400 dark:text-accent-300'
                : 'border-transparent text-neutral-600 dark:text-neutral-400 hover:text-primary-500 dark:hover:text-primary-300'
            ]"
          >
            <component 
              :is="tab.icon" 
              class="w-5 h-5"
              :class="[
                activeTab === tab.id
                  ? 'text-accent-400 dark:text-accent-300'
                  : 'text-neutral-400 dark:text-neutral-500'
              ]"
            />
            {{ tab.name }}
          </button>
        </nav>

        <!-- Mobile Navigation -->
        <div class="sm:hidden">
          <button 
            @click="isMenuOpen = !isMenuOpen"
            class="w-full flex items-center justify-between p-4 rounded-lg
                   bg-white dark:bg-primary-800 shadow-sm
                   border border-neutral-200 dark:border-primary-700"
          >
            <span class="flex items-center gap-2">
              <component 
                :is="tabs.find(t => t.id === activeTab).icon"
                class="w-5 h-5 text-primary-500 dark:text-primary-300"
              />
              <span class="font-medium text-neutral-900 dark:text-white">
                {{ tabs.find(t => t.id === activeTab).name }}
              </span>
            </span>
            <ChevronDown
              class="w-5 h-5 text-neutral-400 dark:text-neutral-500 transition-transform duration-200"
              :class="{ 'rotate-180': isMenuOpen }"
            />
          </button>

          <div 
            v-if="isMenuOpen"
            class="mt-2 rounded-lg overflow-hidden
                   bg-white dark:bg-primary-800 
                   border border-neutral-200 dark:border-primary-700
                   shadow-lg"
          >
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="setActiveTab(tab.id)"
              class="w-full flex items-center gap-3 p-4 text-left
                     transition-colors duration-200"
              :class="[
                activeTab === tab.id
                  ? 'bg-primary-50 dark:bg-primary-700/50'
                  : 'hover:bg-neutral-50 dark:hover:bg-primary-700/30'
              ]"
            >
              <component 
                :is="tab.icon"
                class="w-5 h-5"
                :class="[
                  activeTab === tab.id
                    ? 'text-primary-500 dark:text-primary-300'
                    : 'text-neutral-400 dark:text-neutral-500'
                ]"
              />
              <div>
                <div class="font-medium"
                     :class="[
                       activeTab === tab.id
                         ? 'text-primary-500 dark:text-primary-300'
                         : 'text-neutral-900 dark:text-white'
                     ]"
                >
                  {{ tab.name }}
                </div>
                <div class="text-sm text-neutral-500 dark:text-neutral-400">
                  {{ tab.description }}
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="relative bg-white dark:bg-primary-800 rounded-lg shadow-sm
                  border border-neutral-200 dark:border-primary-700">
        <div class="p-6">
            <component
              :key="getComponentKey(activeTab)"
              :is="
                    activeTab === 'appearance' ? AppearanceSettings :
                    activeTab === 'ollama' ? OllamaSettings :
                    null"
              @change="handleSettingsChange"
              :initial-model="activeTab === 'model' ? uiStore.modelSettings : undefined"
              :initial-theme="activeTab === 'appearance' ? uiStore.theme : undefined"
              :initial-ollama-settings="activeTab === 'ollama' ? uiStore.ollamaSettings : undefined"
            />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Fade transition styles */
.settings-fade-enter-active,
.settings-fade-leave-active {
  transition: all 0.15s ease-out;
}

.settings-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.settings-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Ensure absolute positioning during transition */
.settings-fade-move {
  transition: all 0.15s ease-in-out;
}

/* Keep components in place during transition */
.settings-fade-enter-active,
.settings-fade-leave-active {
  position: absolute;
  width: 100%;
}

/* Ensure parent has space */
.settings-fade-leave-active {
  position: absolute;
  width: 100%;
}

/* Custom scrollbar styles remain the same */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  @apply bg-neutral-100 dark:bg-primary-800;
}

::-webkit-scrollbar-thumb {
  @apply bg-neutral-300 dark:bg-primary-600 rounded-full;
}

::-webkit-scrollbar-thumb:hover {
  @apply bg-neutral-400 dark:bg-primary-500;
}
</style>