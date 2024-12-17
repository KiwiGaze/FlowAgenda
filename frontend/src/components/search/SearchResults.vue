<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Calendar, Clock, Users, Search } from 'lucide-vue-next';

const props = defineProps({
  results: {
    type: Array,
    default: () => []
  },
  isLoading: Boolean
});

const router = useRouter();
const emit = defineEmits(['select']);

const getIcon = (type) => {
  switch (type) {
    case 'event': return Calendar;
    case 'history': return Clock;
    case 'attendee': return Users;
    default: return Search;
  }
};

const getTypeBadgeColor = (type) => {
  switch (type) {
    case 'event': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    case 'history': return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300';
    case 'attendee': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
  }
};

const handleSelect = (result) => {
  emit('select', result);
  window.location.href = result.url;
};

// Add hover state tracking for result items
const hoveredResult = ref(null);
</script>

<template>
  <div class="mt-2 max-h-96 overflow-y-auto custom-scrollbar rounded-xl bg-white dark:bg-gray-800/95 shadow-lg border border-gray-200/50 dark:border-gray-700/50 backdrop-blur-sm results-container">
    <!-- Results Count - Enhanced -->
    <div v-if="!isLoading && results.length" 
         class="sticky top-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white/95 dark:bg-gray-800/95 backdrop-blur-sm z-10">
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
        {{ results.length }} results found
      </span>
    </div>

    <!-- Loading State - Enhanced -->
    <div v-if="isLoading" class="p-4 space-y-4">
      <div v-for="i in 3" :key="i" 
           class="animate-pulse flex space-x-4 opacity-70"
           :style="{ 'animation-delay': `${i * 0.1}s` }">
        <div class="rounded-lg bg-gray-200 dark:bg-gray-700 h-12 w-12"></div>
        <div class="flex-1 space-y-3 py-1">
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded-full w-3/4"></div>
          <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full w-1/2"></div>
        </div>
      </div>
    </div>
    
    <!-- No Results State - Enhanced -->
    <div v-else-if="!results.length" 
         class="p-12 text-center">
      <Search class="w-16 h-16 text-gray-400 mx-auto mb-4 animate-bounce" />
      <p class="text-gray-500 dark:text-gray-400 font-medium">No matches found</p>
      <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">Try adjusting your search</p>
    </div>
    
    <!-- Results List - Enhanced -->
    <div v-else class="divide-y divide-gray-200/75 dark:divide-gray-700/75">
      <!-- Result Item Enhancement -->
      <button
        v-for="result in results"
        :key="result.id"
        class="w-full px-5 py-4 flex items-start gap-4 text-left group 
               transition-all duration-200 
               hover:bg-gray-50/80 dark:hover:bg-gray-750/50
               hover:shadow-sm dark:hover:shadow-dark-sm
               focus:outline-none focus:ring-2 focus:ring-accent-500/50
               relative"
        @click="handleSelect(result)"
        @mouseenter="hoveredResult = result.id"
        @mouseleave="hoveredResult = null"
        :aria-label="`Select ${result.title}`"
        role="button"
        tabindex="0"
      >
        <!-- Icon with enhanced animation -->
        <div class="relative flex-shrink-0">
          <component 
            :is="getIcon(result.type)"
            class="w-6 h-6 text-gray-400 dark:text-gray-500 
                   transition-all duration-200 
                   group-hover:scale-110 group-hover:text-accent-500 
                   dark:group-hover:text-accent-400"
            :aria-label="result.type"
          />
          <div class="absolute inset-0 bg-accent-500/10 dark:bg-accent-400/10 
                      rounded-full scale-0 group-hover:scale-150 
                      transition-transform duration-300 -z-10"></div>
        </div>

        <!-- Content with enhanced typography -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-2">
            <h3 class="font-medium text-gray-900 dark:text-white truncate 
                       group-hover:text-accent-600 dark:group-hover:text-accent-400 
                       transition-colors duration-200">
              {{ result.title }}
            </h3>
            <span 
              :class="[
                getTypeBadgeColor(result.type),
                'text-xs px-2.5 py-1 rounded-full capitalize font-medium tracking-wide transition-all duration-200 group-hover:scale-105 group-hover:shadow-sm'
              ]"
            >
              {{ result.type }}
            </span>
          </div>
          
          <!-- Enhanced metadata display -->
          <div class="flex items-center gap-3 mb-1.5">
            <span v-if="result.date" class="text-xs text-gray-500 dark:text-gray-400 
                  flex items-center gap-1">
              <Clock class="w-3 h-3" />
              {{ result.date }}
            </span>
          </div>

          <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 
                    group-hover:text-gray-600 dark:group-hover:text-gray-300 
                    transition-colors duration-200">
            {{ result.snippet }}
          </p>
        </div>

        <!-- Enhanced hover indicator -->
        <div class="absolute right-2 top-1/2 -translate-y-1/2 
                    transition-all duration-200 
                    opacity-0 group-hover:opacity-100 
                    translate-x-2 group-hover:translate-x-0">
          <div class="text-accent-500 dark:text-accent-400 
                      p-2 rounded-full bg-accent-50/50 dark:bg-accent-900/50">
            <svg xmlns="http://www.w3.org/2000/svg" 
                 class="h-5 w-5 transition-transform duration-200 
                        group-hover:translate-x-0.5" 
                 viewBox="0 0 20 20" 
                 fill="currentColor">
              <path fill-rule="evenodd" 
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" 
                    clip-rule="evenodd" />
            </svg>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.custom-scrollbar {
  /* Firefox */
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.3) transparent;
}

/* Chrome, Edge, Safari */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 8px;
  margin: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.3);
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.5);
}

/* Dark mode */
:root.dark .custom-scrollbar {
  scrollbar-color: rgba(75, 85, 99, 0.3) transparent;
}

:root.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.3);
}

:root.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(75, 85, 99, 0.5);
}

.results-container {
  transition: all 0.3s ease;
}

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

.animate-fadeIn {
  animation: slideIn 0.3s ease-out forwards;
}

/* Enhanced animations and transitions */
.group {
  transform-style: preserve-3d;
  perspective: 1000px;
}

.group:active {
  transform: scale(0.995);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}

/* Enhanced focus styles */
.group:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px theme('colors.accent.500/50');
}
</style>