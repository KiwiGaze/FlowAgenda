<!-- components/settings/AppearanceSettings.vue -->
<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';
import { Sun, Moon, Monitor, Palette } from 'lucide-vue-next';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';

const props = defineProps({
  initialTheme: {
    type: String,
    default: 'system'
  }
});

const emit = defineEmits(['change']);

const uiStore = useUiPreferencesStore();
const selectedTheme = ref(uiStore.theme);

const systemTheme = ref('light');
let mediaQueryListener = null;

// System theme detection
onMounted(() => {
  const mediaQuery = window?.matchMedia?.('(prefers-color-scheme: dark)');
  if (mediaQuery) {
    systemTheme.value = mediaQuery.matches ? 'dark' : 'light';
    mediaQueryListener = (e) => {
      systemTheme.value = e.matches ? 'dark' : 'light';
    };
    mediaQuery.addEventListener('change', mediaQueryListener);
  }
});

onUnmounted(() => {
  if (mediaQueryListener) {
    const mediaQuery = window?.matchMedia?.('(prefers-color-scheme: dark)');
    if (mediaQuery) {
      mediaQuery.removeEventListener('change', mediaQueryListener);
    }
  }
});

const currentTheme = computed(() => {
  return selectedTheme.value === 'system' ? systemTheme.value : selectedTheme.value;
});

watch(selectedTheme, (newTheme) => {
  uiStore.setTheme(newTheme);
});

const themes = [
  {
    id: 'light',
    name: 'Light',
    icon: Sun,
    description: 'Light mode for daytime use'
  },
  {
    id: 'dark',
    name: 'Dark',
    icon: Moon,
    description: 'Dark mode for comfortable viewing'
  },
  {
    id: 'system',
    name: 'System',
    icon: Monitor,
    description: 'Follow system preferences'
  }
];

const getThemePreview = computed(() => (themeId) => {
  const effectiveTheme = themeId === 'system' ? systemTheme.value : themeId;
  
  switch (effectiveTheme) {
    case 'dark':
      return {
        background: 'bg-gray-900',
        text: 'text-white',
        accent: 'bg-accent-400',
        border: 'border-gray-700'
      };
    case 'light':
    default:
      return {
        background: 'bg-white',
        text: 'text-neutral-900',
        accent: 'bg-accent-400',
        border: 'border-neutral-200'
      };
  }
});
</script>

<template>
  <section class="space-y-6">
    <!-- Section Header -->
    <div class="flex items-center gap-2">
      <Palette class="w-5 h-5 text-accent-400" />
      <h2 class="text-lg font-semibold text-primary-500">Appearance</h2>
    </div>

    <!-- Theme Selection -->
    <div class="grid gap-4 sm:grid-cols-3">
      <div
        v-for="theme in themes"
        :key="theme.id"
        class="relative"
      >
        <input
          type="radio"
          :name="theme.id"
          :id="theme.id"
          :value="theme.id"
          v-model="selectedTheme"
          class="peer sr-only"
        />
        
        <label
          :for="theme.id"
          class="block cursor-pointer"
        >
          <!-- Theme Preview Card -->
          <div 
            class="aspect-[4/3] rounded-lg border transition-all duration-200 overflow-hidden"
            :class="[
              selectedTheme === theme.id
                ? 'border-accent-400 ring-1 ring-accent-400'
                : 'border-neutral-200 hover:border-neutral-300'
            ]"
          >
            <!-- Preview Content -->
            <div 
              class="h-full p-4 transition-colors"
              :class="getThemePreview(theme.id).background"
            >
              <!-- Mock UI Elements -->
              <div class="space-y-3">
                <div 
                  class="w-8 h-8 rounded-lg flex items-center justify-center"
                  :class="getThemePreview(theme.id).accent"
                >
                  <component 
                    :is="theme.icon"
                    class="w-5 h-5 text-white"
                  />
                </div>
                <div 
                  class="w-16 h-2 rounded"
                  :class="getThemePreview(theme.id).accent"
                ></div>
                <div 
                  class="w-12 h-2 rounded opacity-60"
                  :class="getThemePreview(theme.id).accent"
                ></div>
              </div>
            </div>
          </div>

          <!-- Theme Label -->
          <div class="mt-2">
            <div class="font-medium text-neutral-900">{{ theme.name }}</div>
            <div class="text-sm text-neutral-600">{{ theme.description }}</div>
          </div>
        </label>

        <!-- Selected Indicator -->
        <div 
          class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-accent-400 text-white flex items-center justify-center transform scale-0 transition-transform duration-200 peer-checked:scale-100"
        >
          <svg viewBox="0 0 24 24" class="w-3 h-3" fill="none" stroke="currentColor">
            <polyline points="20 6 9 17 4 12" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- System Theme Note -->
    <div 
      v-if="selectedTheme === 'system'"
      class="p-4 bg-neutral-50 rounded-lg text-sm text-neutral-600 flex flex-col items-center text-center"
    >
      <Monitor class="w-4 h-4 mb-2 text-neutral-400" />
      <div>
        <p>Your theme will automatically adjust based on your system preferences.</p>
        <p class="mt-1 text-sm text-neutral-500">
          Current system theme: {{ systemTheme === 'dark' ? 'Dark' : 'Light' }}
        </p>
      </div>
    </div>
  </section>
</template>