<!-- components/actions/QuickActions.vue -->
<script setup>
import { TrendingUp, Globe, ArrowUpRight, Search, Clock } from 'lucide-vue-next'
import { ref, watch, computed } from 'vue'
import { useQuickActions } from '@/composables/useQuickActions'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const {
  searchText,
  selectedIndex,
  suggestions,
  getSmartTemplate,
  handleKeyNavigation
} = useQuickActions(props.modelValue)

// Computed for container positioning
const containerClasses = computed(() => ({
  'opacity-0 translate-y-2': !props.show,
  'opacity-100 translate-y-0': props.show,
  'pointer-events-none': props.isLoading
}))

// Watch for model value changes
watch(() => props.modelValue, (newValue) => {
  searchText.value = newValue
})

const handleSuggestionClick = (suggestion) => {
  if (props.isLoading) return
  const template = getSmartTemplate(suggestion)
  emit('select', template)
}

const handleKeydown = (e) => {
  const template = handleKeyNavigation(e)
  if (template) {
    emit('select', template)
  }
}
</script>

<template>
  <div 
    v-show="show && suggestions.length > 0"
    class="quick-actions-container mt-4 transform transition-all duration-300 ease-out"
    :class="containerClasses"
  >
    <!-- Glass-morphic Container -->
    <div class="bg-white/80 dark:bg-primary-900/80 rounded-xl 
                border border-neutral-200/50 dark:border-primary-700/50
                overflow-hidden">
      
      <!-- Search Section -->
      <div class="p-3 border-b border-neutral-200/50 dark:border-primary-700/50">
        <div class="flex items-center gap-3 px-3 py-2 rounded-lg
                    bg-neutral-50/50 dark:bg-primary-800/50
                    hover:bg-neutral-100/50 dark:hover:bg-primary-700/50
                    transition-colors duration-200 group cursor-pointer"
             @click="handleSuggestionClick(suggestions[0])">
          <Search class="w-5 h-5 text-accent-500 dark:text-accent-400
                        group-hover:scale-110 transition-transform duration-200" />
          <span class="text-sm text-neutral-700 dark:text-neutral-200">
            Search templates...
          </span>
        </div>
      </div>
      
      <!-- Suggestions List -->
      <div class="max-h-[300px] overflow-y-auto custom-scrollbar">
        <!-- Recent Section -->
        <div class="px-3 py-2 flex items-center gap-2">
          <Clock class="w-4 h-4 text-neutral-400 dark:text-neutral-500" />
          <span class="text-xs font-medium text-neutral-500 dark:text-neutral-400">
            Recently Used
          </span>
        </div>
        
        <!-- Suggestions -->
        <div class="space-y-1 p-2">
          <button
            v-for="(suggestion, index) in suggestions"
            :key="suggestion.id"
            @click="handleSuggestionClick(suggestion)"
            class="w-full p-3 flex items-center gap-3 rounded-lg group
                   hover:bg-neutral-50/70 dark:hover:bg-primary-800/50
                   focus:outline-none focus:ring-2 focus:ring-accent-400/30
                   transition-all duration-200 relative overflow-hidden"
            :class="{
              'bg-neutral-50/70 dark:bg-primary-800/50': index === selectedIndex
            }"
          >
            <!-- Hover Effect Background -->
            <div class="absolute inset-0 bg-gradient-to-r from-accent-400/0 to-accent-400/5
                      dark:from-accent-500/0 dark:to-accent-500/10
                      opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            </div>
            
            <!-- Icon Container -->
            <div class="relative flex-shrink-0 w-10 h-10 flex items-center justify-center
                        rounded-lg bg-accent-50/50 dark:bg-accent-900/30
                        group-hover:bg-accent-100/50 dark:group-hover:bg-accent-800/30
                        transition-colors duration-200">
              <component
                :is="index < 2 ? TrendingUp : undefined"
                v-if="index < 2"
                class="w-5 h-5 text-accent-500 dark:text-accent-400
                       group-hover:scale-110 transition-transform duration-200"
              />
              <span
                v-else
                class="text-lg transform group-hover:scale-110 transition-transform duration-200"
                :class="[suggestion.iconColor]"
              >
                {{ suggestion.icon }}
              </span>
            </div>
            
            <!-- Content -->
            <div class="flex-1 flex items-center justify-between min-w-0">
              <div class="truncate">
                <div class="text-sm font-medium text-neutral-900 dark:text-neutral-100
                           group-hover:text-accent-500 dark:group-hover:text-accent-400
                           transition-colors duration-200">
                  {{ suggestion.label }}
                </div>
                <div class="text-xs text-neutral-500 dark:text-neutral-400">
                  {{ suggestion.category }}
                </div>
              </div>
              
              <!-- Action Icon -->
              <ArrowUpRight class="w-4 h-4 text-neutral-400 dark:text-neutral-500
                                  opacity-0 group-hover:opacity-100
                                  transform translate-x-2 group-hover:translate-x-0
                                  transition-all duration-200" />
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quick-actions-container {
  contain: content;
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.neutral.300') theme('colors.neutral.100');
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  @apply bg-neutral-100 dark:bg-primary-800 rounded-full;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-neutral-300 dark:bg-primary-600 rounded-full;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  @apply bg-neutral-400 dark:bg-primary-500;
}

/* Animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.quick-actions-container {
  animation: slideIn 0.3s ease-out;
}
</style>