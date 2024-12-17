<!-- components/settings/ModelSettings.vue -->
<script setup>
import { ref, watch, onMounted } from 'vue';
import { Bot, Key, ChevronRight, AlertCircle, Loader2, Check, X, ExternalLink, 
         Zap, Rocket, Brain, Sparkles, Cog, Settings, RotateCcw } from 'lucide-vue-next';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';
import Tooltip from '../Tooltip.vue';

const uiStore = useUiPreferencesStore();
const emit = defineEmits(['change']);

// Initialize from store
const selectedModel = ref(uiStore.modelSettings.selectedModel);
const showAdvancedSettings = ref(false);

const isTestingKey = ref(false);
const keyStatus = ref(null); // null | 'valid' | 'invalid'

// API Configuration
const baseUrl = ref(uiStore.modelSettings.baseUrl);
const defaultBaseUrl = 'https://api.openai.com/v1';

// API Keys with visibility toggles
// Safe way to access the API keys
const openaiApiKey = ref(uiStore.modelSettings?.apiKeys?.openai || '');
const deepseekApiKey = ref(uiStore.modelSettings?.apiKeys?.deepseek || '');
const claudeApiKey = ref(uiStore.modelSettings?.apiKeys?.claude || '');
const qwenApiKey = ref(uiStore.modelSettings?.apiKeys?.qwen || '');

const showOpenaiKey = ref(false);
const showDeepseekKey = ref(false);
const showClaudeKey = ref(false);
const showQwenKey = ref(false);

const models = [
  {
    id: 'gpt4o',
    name: 'GPT-4o',
    description: 'High-performance model for complex tasks',
    icon: Rocket,
    iconColor: 'text-green-500 dark:text-green-400',
    iconBg: 'bg-green-50 dark:bg-green-900/50',
    tag: 'Recommended',
    tagColor: 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400'
  },
  {
    id: 'gpt4o-mini',
    name: 'GPT-4 Mini',
    description: 'Lightweight version optimized for speed',
    icon: Zap,
    iconColor: 'text-blue-500 dark:text-blue-400',
    iconBg: 'bg-blue-50 dark:bg-blue-900/50',
    tag: 'Fast',
    tagColor: 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-400'
  },
  {
    id: 'deepseek',
    name: 'DeepSeek',
    description: 'Advanced code completion and generation',
    icon: Sparkles,
    iconColor: 'text-purple-500 dark:text-purple-400',
    iconBg: 'bg-purple-50 dark:bg-purple-900/50',
    tag: 'Beta',
    tagColor: 'bg-purple-100 text-purple-700 dark:bg-purple-900/50 dark:text-purple-400'
  },
  {
    id: 'claude',
    name: 'Claude 3',
    description: 'Advanced reasoning and analysis capabilities',
    icon: Brain,
    iconColor: 'text-amber-500 dark:text-amber-400',
    iconBg: 'bg-amber-50 dark:bg-amber-900/50',
    tag: 'Premium',
    tagColor: 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-400'
  },
  {
    id: 'qwen',
    name: 'Qwen-2.5',
    description: 'Multilingual model with strong reasoning abilities',
    icon: Bot,
    iconColor: 'text-teal-500 dark:text-teal-400',
    iconBg: 'bg-teal-50 dark:bg-teal-900/50',
    tag: 'New',
    tagColor: 'bg-teal-100 text-teal-700 dark:bg-teal-900/50 dark:text-teal-400'
  }
];

watch([selectedModel, baseUrl, openaiApiKey, deepseekApiKey, claudeApiKey, qwenApiKey], () => {
  uiStore.setModelSettings({
    selectedModel: selectedModel.value,
    baseUrl: baseUrl.value,
    apiKeys: {
      openai: openaiApiKey.value,
      deepseek: deepseekApiKey.value,
      claude: claudeApiKey.value,
      qwen: qwenApiKey.value
    }
  });
  emit('change');
});

const handleModelSelect = (modelId) => {
  selectedModel.value = modelId;
};

const testApiKey = async () => {
  if (!apiKey.value || isTestingKey.value) return;
  
  isTestingKey.value = true;
  keyStatus.value = null;
  
  try {
    // Simulate API key validation
    await new Promise(resolve => setTimeout(resolve, 1500));
    keyStatus.value = 'valid';
  } catch (error) {
    keyStatus.value = 'invalid';
  } finally {
    isTestingKey.value = false;
  }
};

const getKeyStatusColor = () => {
  switch (keyStatus.value) {
    case 'valid':
      return 'text-green-500 dark:text-green-400';
    case 'invalid':
      return 'text-red-500 dark:text-red-400';
    default:
      return 'text-neutral-400 dark:text-neutral-500';
  }
};

const getStatusMessage = () => {
  switch (keyStatus.value) {
    case 'valid':
      return 'API key is valid and ready to use';
    case 'invalid':
      return 'Invalid API key. Please check and try again';
    default:
      return '';
  }
};

onMounted(() => {
  // Initialize from store
  selectedModel.value = uiStore.modelSettings.selectedModel;
  baseUrl.value = uiStore.modelSettings.baseUrl;
  openaiApiKey.value = uiStore.modelSettings.apiKeys.openai;
  deepseekApiKey.value = uiStore.modelSettings.apiKeys.deepseek;
  claudeApiKey.value = uiStore.modelSettings.apiKeys.claude;
  qwenApiKey.value = uiStore.modelSettings.apiKeys.qwen;
});
</script>

<template>
  <section class="space-y-6">
    <!-- Section Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Cog class="w-5 h-5 text-accent-400 dark:text-accent-300" />
        <h2 class="text-lg font-semibold text-primary-500 dark:text-primary-300">AI Model Settings</h2>
      </div>
      
      <button 
        @click="showAdvancedSettings = !showAdvancedSettings"
        class="text-sm text-accent-400 dark:text-accent-300 hover:text-accent-500 dark:hover:text-accent-200 flex items-center gap-1 outline-none transition-colors"
      >
        {{ showAdvancedSettings ? 'Hide' : 'Show' }} Advanced Settings
        <ChevronRight 
          class="w-4 h-4 transition-transform duration-200"
          :class="{ 'rotate-90': showAdvancedSettings }"
        />
      </button>
    </div>

    <!-- Model Selection -->
    <div class="grid gap-4">
      <div 
        v-for="model in models" 
        :key="model.id"
        class="group relative bg-white dark:bg-primary-800 rounded-lg border transition-all duration-200"
        :class="[
          selectedModel === model.id
            ? 'border-accent-400 dark:border-accent-500 shadow-sm ring-1 ring-accent-400 dark:ring-accent-500 ring-opacity-50'
            : 'border-neutral-200 dark:border-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'
        ]"
      >
        <label class="block cursor-pointer">
          <div class="p-4 sm:p-5">
            <div class="flex items-start gap-4">
              <!-- Model Icon -->
              <div 
                class="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center transition-colors duration-200"
                :class="[
                  selectedModel === model.id 
                    ? 'bg-accent-50 dark:bg-accent-900/50' 
                    : model.iconBg
                ]"
              >
                <component 
                  :is="model.icon" 
                  class="w-5 h-5"
                  :class="selectedModel === model.id ? 'text-accent-400 dark:text-accent-300' : model.iconColor"
                />
              </div>

              <!-- Model Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <div class="font-medium text-neutral-900 dark:text-neutral-100">{{ model.name }}</div>
                  <span 
                    v-if="model.tag"
                    class="px-2 py-0.5 text-xs font-medium rounded-full"
                    :class="model.tagColor"
                  >
                    {{ model.tag }}
                  </span>
                </div>
                <div class="text-sm text-neutral-600 dark:text-neutral-400">{{ model.description }}</div>
              </div>

              <!-- Radio Button -->
              <div class="flex-shrink-0">
                <input
                  type="radio"
                  :name="model.id"
                  :value="model.id"
                  v-model="selectedModel"
                  class="w-4 h-4 text-accent-400 dark:text-accent-300 border-neutral-300 dark:border-neutral-600 focus:ring-accent-400 dark:focus:ring-accent-500 dark:bg-primary-700"
                  @change="handleModelSelect(model.id)"
                />
              </div>
            </div>
          </div>
        </label>

        <!-- Selection Indicator -->
        <div 
          class="absolute -left-px top-1/2 -translate-y-1/2 w-1 h-12 bg-accent-400 dark:bg-accent-500 rounded-r transition-all duration-200"
          :class="selectedModel === model.id ? 'opacity-100' : 'opacity-0'"
        ></div>
      </div>
    </div>

    <!-- API Configuration Section -->
    <div 
      class="bg-white dark:bg-primary-800 rounded-lg border border-neutral-200 dark:border-neutral-700 overflow-display transition-all duration-200"
      :class="{ 'ring-1 ring-accent-400 dark:ring-accent-500 ring-opacity-50': keyStatus === 'valid' }"
    >
      <!-- Main Settings -->
      <div class="p-5 space-y-5">
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-2 mb-1.5">
              <Key class="w-5 h-5 text-accent-400 dark:text-accent-300" />
              <h3 class="font-medium text-neutral-900 dark:text-neutral-100">API Configuration</h3>
            </div>
            <p class="text-sm text-neutral-600 dark:text-neutral-400">Configure your API access credentials and endpoints</p>
          </div>
          
          <Tooltip 
            v-if="selectedModel === 'openai'"
            content="Get your API key from OpenAI dashboard"
            position="left"
          >
            <a 
              href="https://platform.openai.com/account/api-keys" 
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm text-accent-400 dark:text-accent-300 bg-accent-50 dark:bg-accent-900/50 hover:bg-accent-100 dark:hover:bg-accent-900/70 rounded-lg transition-colors group"
            >
              Get API Key
              <ExternalLink class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
            </a>
          </Tooltip>
        </div>

        <!-- API Key Input -->
        <div class="space-y-4">
            <!-- OpenAI API Key -->
            <div class="space-y-2">
            <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">
              OpenAI API Key
            </label>
            <div class="relative">
              <input
              :type="showOpenaiKey ? 'text' : 'password'"
              v-model="openaiApiKey"
              placeholder="sk-..."
              class="w-full pl-4 pr-24 py-2.5 bg-white dark:bg-primary-700 border border-neutral-200 dark:border-neutral-600 rounded-lg text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 focus:border-transparent transition-all text-sm"
              />
              <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
              <button 
                class="text-xs text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200" 
                @click="showOpenaiKey = !showOpenaiKey"
              >
                {{ showOpenaiKey ? 'Hide' : 'Show' }}
              </button>
              </div>
            </div>
            </div>
            <!-- DeepSeek API Key -->
            <div class="space-y-2">
            <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">DeepSeek API Key</label>
            <div class="relative">
              <input
              :type="showDeepseekKey ? 'text' : 'password'"
              v-model="deepseekApiKey"
              placeholder="dsk-..."
              class="w-full pl-4 pr-24 py-2.5 bg-white dark:bg-primary-700 border border-neutral-200 dark:border-neutral-600 rounded-lg text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 focus:border-transparent transition-all text-sm"
              />
              <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
              <button class="text-xs text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200" @click="showDeepseekKey = !showDeepseekKey">
                {{ showDeepseekKey ? 'Hide' : 'Show' }}
              </button>
              </div>
            </div>
            </div>

            <!-- Claude API Key -->
            <div class="space-y-2">
            <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Claude API Key</label>
            <div class="relative">
              <input
              :type="showClaudeKey ? 'text' : 'password'"
              v-model="claudeApiKey"
              placeholder="sk-..."
              class="w-full pl-4 pr-24 py-2.5 bg-white dark:bg-primary-700 border border-neutral-200 dark:border-neutral-600 rounded-lg text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 focus:border-transparent transition-all text-sm"
              />
              <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
              <button class="text-xs text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200" @click="showClaudeKey = !showClaudeKey">
                {{ showClaudeKey ? 'Hide' : 'Show' }}
              </button>
              </div>
            </div>
            </div>

            <!-- Qwen API Key -->
            <div class="space-y-2">
            <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Qwen API Key</label>
            <div class="relative">
              <input
              :type="showQwenKey ? 'text' : 'password'"
              v-model="qwenApiKey"
              placeholder="qwk-..."
              class="w-full pl-4 pr-24 py-2.5 bg-white dark:bg-primary-700 border border-neutral-200 dark:border-neutral-600 rounded-lg text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 focus:border-transparent transition-all text-sm"
              />
              <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
              <button class="text-xs text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200" @click="showQwenKey = !showQwenKey">
                {{ showQwenKey ? 'Hide' : 'Show' }}
              </button>
              </div>
            </div>
            </div>

          <!-- Similar structure for DeepSeek, Claude, and Qwen API keys -->
          <!-- ... other API key inputs follow same pattern ... -->

          <!-- Status Message -->
          <Transition
            enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="opacity-0 -translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-2"
          >
            <div 
              v-if="keyStatus"
              class="flex items-center gap-2 mt-2 text-sm pl-1"
              :class="[
                keyStatus === 'valid' 
                  ? 'text-green-600 dark:text-green-400' 
                  : 'text-red-600 dark:text-red-400'
              ]"
            >
              <component 
                :is="keyStatus === 'valid' ? Check : AlertCircle"
                class="w-4 h-4"
              />
              <span>{{ getStatusMessage() }}</span>
            </div>
          </Transition>
        </div>
      </div>

      <!-- Advanced Settings -->
      <div class="border-t border-neutral-100 dark:border-neutral-700">
        <button 
          @click="showAdvancedSettings = !showAdvancedSettings"
          class="w-full px-5 py-3 text-left hover:bg-neutral-50 dark:hover:bg-primary-700/50 transition-colors outline-none"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Settings class="w-4 h-4 text-neutral-400 dark:text-neutral-500" />
              <span class="text-sm font-medium text-neutral-700 dark:text-neutral-300">
                Advanced Settings
              </span>
            </div>
            <ChevronRight 
              class="w-4 h-4 text-neutral-400 dark:text-neutral-500 transition-transform duration-200"
              :class="{ 'rotate-90': showAdvancedSettings }"
            />
          </div>
        </button>

        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="max-h-0 opacity-0"
          enter-to-class="max-h-[500px] opacity-100"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="max-h-[500px] opacity-100"
          leave-to-class="max-h-0 opacity-0"
        >
          <div v-if="showAdvancedSettings" class="px-5 pb-5">
            <div class="pt-4 space-y-4">
              <!-- Base URL Input -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
                  Base URL
                </label>
                <div class="relative">
                  <input
                    type="url"
                    v-model="baseUrl"
                    placeholder="https://api.openai.com/v1"
                    class="w-full pl-4 pr-10 py-2.5 bg-white dark:bg-primary-700 border border-neutral-200 dark:border-neutral-600 rounded-lg text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 focus:border-transparent transition-all text-sm"
                  />
                  <Tooltip content="Reset to default" position="right">
                    <button
                      @click="baseUrl = defaultBaseUrl"
                      class="absolute right-3 top-1/2 -translate-y-2/3 p-1 text-neutral-400 dark:text-neutral-500 hover:text-neutral-600 dark:hover:text-neutral-300 rounded-md transition-colors"
                    >
                      <RotateCcw class="w-4 h-4" />
                    </button>
                  </Tooltip>
                </div>
                <p class="mt-1.5 text-xs text-neutral-500 dark:text-neutral-400">
                  Only modify this if you're using a custom endpoint or proxy
                </p>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>