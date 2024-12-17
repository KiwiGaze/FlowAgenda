<!-- components/settings/LanguageSettings.vue -->
<script setup>
import { ref, watch, onMounted } from 'vue';
import { Languages, Check } from 'lucide-vue-next';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';

const emit = defineEmits(['change']);
const uiStore = useUiPreferencesStore();

// Initialize from store
const selectedLanguage = ref(uiStore.language);

const languages = [
  {
    id: 'en',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸'
  },
  {
    id: 'zh-CN',
    name: 'Simplified Chinese',
    nativeName: '简体中文',
    flag: '🇨🇳'
  },
  {
    id: 'zh-TW',
    name: 'Traditional Chinese',
    nativeName: '繁體中文',
    flag: '🇭🇰'
  }
];

watch(selectedLanguage, (newLang) => {
  uiStore.setLanguage(newLang);
  emit('change');
});

const handleLanguageSelect = async (langId) => {
  if (selectedLanguage.value === langId) return;
  selectedLanguage.value = langId;
};

onMounted(() => {
  selectedLanguage.value = uiStore.language;
});
</script>

<template>
  <section class="space-y-6">
    <!-- Section Header -->
    <div class="flex items-center gap-2">
      <Languages class="w-5 h-5 text-accent-400" />
      <h2 class="text-lg font-semibold text-primary-500 dark:text-primary-100">Language</h2>
    </div>

    <!-- Language Selection -->
    <div class="bg-white dark:bg-primary-800 rounded-lg border border-neutral-200 dark:border-primary-700 divide-y divide-neutral-100 dark:divide-primary-700 overflow-hidden">
      <div
        v-for="language in languages"
        :key="language.id"
        class="relative"
      >
        <button
          class="w-full px-4 py-3 flex items-center justify-between hover:bg-neutral-50 dark:hover:bg-primary-700/50 transition-colors"
          :class="{ 
            'bg-neutral-50 dark:bg-primary-700': selectedLanguage === language.id 
          }"
          @click="handleLanguageSelect(language.id)"
        >
          <div class="flex items-center gap-3">
            <span class="text-2xl">{{ language.flag }}</span>
            <div class="text-left">
              <div class="font-medium text-neutral-900 dark:text-neutral-100">
                {{ language.name }}
              </div>
              <div class="text-sm text-neutral-600 dark:text-neutral-400">
                {{ language.nativeName }}
              </div>
            </div>
          </div>

          <div 
            class="w-5 h-5 rounded-full border flex items-center justify-center transition-colors"
            :class="[
              selectedLanguage === language.id
                ? 'border-accent-400 bg-accent-400 dark:border-accent-500 dark:bg-accent-500'
                : 'border-neutral-300 dark:border-neutral-600'
            ]"
          >
            <Check 
              v-if="selectedLanguage === language.id"
              class="w-3 h-3 text-white" 
            />
          </div>
        </button>
      </div>
    </div>

    <!-- Language Info -->
    <div class="p-4 bg-neutral-50 dark:bg-primary-800/50 rounded-lg text-sm text-neutral-600 dark:text-neutral-400 flex items-center justify-center gap-2">
      <Languages class="w-4 h-4 mt-0.5 text-neutral-400 dark:text-neutral-500" />
      <div class="space-y-2 text-center">
        <p>
          This will change the language for the entire application. Some content may not be available in all languages.
        </p>
        <p class="text-neutral-500 dark:text-neutral-500">
          App content, emails, and notifications will be displayed in your selected language.
        </p>
      </div>
    </div>
  </section>
</template>