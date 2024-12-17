<!-- components/history/HistorySearch.vue -->
<script setup>
import { ref, watch } from 'vue';
import { Search, X } from 'lucide-vue-next';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'search']);
const localValue = ref(props.modelValue);
const isDebouncing = ref(false);

watch(localValue, (newValue) => {
  emit('update:modelValue', newValue);
  
  // Debounce search
  if (isDebouncing.value) return;
  isDebouncing.value = true;
  
  setTimeout(() => {
    emit('search', newValue);
    isDebouncing.value = false;
  }, 300);
});

const clearSearch = () => {
  localValue.value = '';
  emit('search', '');
};
</script>

<template>
  <div class="relative">
    <div class="relative">
      <Search 
        class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400 dark:text-neutral-500" 
      />
      
      <input
        v-model="localValue"
        type="text"
        placeholder="Search events..."
        class="w-full pl-10 pr-10 py-2.5 
               bg-white dark:bg-primary-800 
               border border-neutral-200 dark:border-primary-700 
               rounded-lg 
               text-neutral-900 dark:text-neutral-100 
               placeholder:text-neutral-400 dark:placeholder:text-neutral-500 
               focus:ring-2 focus:ring-accent-400 dark:focus:ring-accent-500 
               focus:border-transparent 
               hover:border-neutral-300 dark:hover:border-primary-600
               transition-all duration-200"
      />
      
      <button 
        v-if="localValue"
        @click="clearSearch"
        class="absolute right-3 top-1/2 -translate-y-1/2 p-1 
               text-neutral-400 dark:text-neutral-500 
               hover:text-neutral-600 dark:hover:text-neutral-300 
               rounded-full 
               hover:bg-neutral-100 dark:hover:bg-primary-700
               transition-colors duration-200"
      >
        <X class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>