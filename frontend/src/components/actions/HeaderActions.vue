<!-- components/actions/HeaderActions.vue -->
<script setup>
import { ArrowLeft, Search } from 'lucide-vue-next';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  showSearch: {
    type: Boolean,
    default: false
  },
  searchQuery: {
    type: String,
    default: ''
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  }
});

const emit = defineEmits(['back', 'update:searchQuery']);
</script>

<template>
  <header class="sticky top-0 z-40">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-16">
        <!-- Left Section -->
        <div class="flex items-center gap-4">
          <button 
            @click="$emit('back')" 
            class="p-2 text-neutral-600 dark:text-neutral-300 hover:bg-white/80 dark:hover:bg-primary-700/80 
                   rounded-lg transition-all duration-200 group focus:outline-none focus:ring-2 
                   focus:ring-accent-400/50 dark:focus:ring-accent-500/50"
            aria-label="Go back"
          >
            <ArrowLeft class="w-5 h-5 group-hover:scale-110 group-hover:-translate-x-0.5 transition-transform duration-200" />
          </button>
          <div class="flex flex-col">
            <h1 class="text-lg font-semibold bg-gradient-to-r from-primary-900 to-primary-700 dark:from-primary-100 dark:to-primary-300 
                       bg-clip-text text-transparent">
              {{ title }}
            </h1>
            <span v-if="subtitle" class="text-sm text-neutral-500 dark:text-neutral-400 font-medium">
              {{ subtitle }}
            </span>
          </div>
        </div>

        <!-- Right Section -->
        <div v-if="showSearch" class="flex items-center gap-3">
          <div class="relative group">
            <Search class="w-4 h-4 z-10 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400 
                         group-focus-within:text-accent-400 transition-colors duration-200" />
            <input
              :value="searchQuery"
              @input="$emit('update:searchQuery', $event.target.value)"
              type="search"
              :placeholder="searchPlaceholder"
              class="w-full sm:w-64 pl-10 pr-4 py-2 text-sm bg-white/80 dark:bg-primary-700/80 
                     backdrop-blur-sm border border-neutral-200 dark:border-neutral-600 rounded-lg
                     placeholder-neutral-400 dark:placeholder-neutral-500 shadow-sm
                     focus:outline-none focus:ring-2 focus:ring-accent-400/50 dark:focus:ring-accent-500/50
                     hover:border-neutral-300 dark:hover:border-neutral-500
                     transition-all duration-200"
            />
          </div>
        </div>
      </div>
    </div>
  </header>
</template>