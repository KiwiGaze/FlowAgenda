<!-- components/history/HistoryFilter.vue -->
<script setup>
import { 
  CalendarDays, 
  Users, 
  Presentation, 
  ClipboardList,
  AlertCircle,
  CheckCircle2,
  Clock,
  X,
  Calendar
} from 'lucide-vue-next';

const props = defineProps({
  modelValue: {
    type: String,
    default: 'all'
  },
  counts: {
    type: Object,
    default: () => ({
      all: 0,
      completed: 0,
      processing: 0,
      error: 0,
      meetings: 0,
      presentations: 0,
      reviews: 0
    })
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const filters = computed(() => [
  { 
    id: 'all', 
    label: 'All Groups', 
    icon: Calendar,
    count: props.counts.all,
    description: 'Show all event groups'
  },
  // Processing Status Filters
  { 
    id: 'completed', 
    label: 'Completed', 
    icon: CheckCircle2,
    count: props.counts.completed,
    description: 'Fully processed groups',
    category: 'status' 
  },
  { 
    id: 'processing', 
    label: 'Processing', 
    icon: Clock,
    count: props.counts.processing,
    description: 'Groups being processed',
    category: 'status'
  },
  { 
    id: 'error', 
    label: 'Failed', 
    icon: AlertCircle,
    count: props.counts.error,
    description: 'Groups with processing errors',
    category: 'status',
    variant: 'error'
  },
  // Event Type Filters
  { 
    id: 'meetings', 
    label: 'Meetings', 
    icon: Users,
    count: props.counts.meetings,
    description: 'Groups with meeting events',
    category: 'type'
  },
  { 
    id: 'presentations', 
    label: 'Presentations', 
    icon: Presentation,
    count: props.counts.presentations,
    description: 'Groups with presentation events',
    category: 'type'
  },
  { 
    id: 'reviews', 
    label: 'Reviews', 
    icon: ClipboardList,
    count: props.counts.reviews,
    description: 'Groups with review events',
    category: 'type'
  }
]);

const statusFilters = computed(() => 
  filters.value.filter(f => f.category === 'status')
);

const typeFilters = computed(() => 
  filters.value.filter(f => f.category === 'type')
);

const handleFilterChange = (filterId) => {
  emit('update:modelValue', filterId);
  emit('change', filterId);
};

const getFilterStyle = (filter) => {
  // Base classes
  const baseClasses = 'flex items-center gap-3 p-3 rounded-lg border text-left transition-all duration-200';
  
  // Selected state classes
  const selectedClasses = {
    default: 'border-accent-400 bg-accent-50 dark:bg-accent-900/20 text-accent-400 dark:text-accent-300',
    error: 'border-red-400 bg-red-50 dark:bg-red-900/20 text-red-400 dark:text-red-300'
  };
  
  // Unselected state classes
  const unselectedClasses = {
    default: 'border-neutral-200 dark:border-primary-700 hover:border-neutral-300 dark:hover:border-primary-600 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-50 dark:hover:bg-primary-700/50',
    error: 'border-neutral-200 dark:border-primary-700 hover:border-red-300 dark:hover:border-red-600 text-neutral-600 dark:text-neutral-400 hover:bg-red-50 dark:hover:bg-red-900/20'
  };

  const isSelected = props.modelValue === filter.id;
  const styleVariant = filter.variant || 'default';

  return `${baseClasses} ${isSelected ? selectedClasses[styleVariant] : unselectedClasses[styleVariant]}`;
};
</script>

<template>
  <div class="bg-white dark:bg-primary-800 rounded-lg border border-neutral-200 dark:border-primary-700 p-4 space-y-6 transition-colors duration-200">
    <!-- Header with Clear Option -->
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-sm font-medium text-primary-500 dark:text-primary-100">
        Filter Events
      </h3>
      <button 
        v-if="modelValue !== 'all'"
        @click="handleFilterChange('all')"
        class="text-xs text-neutral-600 dark:text-neutral-400 hover:text-accent-400 dark:hover:text-accent-300 transition-colors flex items-center gap-1"
      >
        <X class="w-3 h-3" />
        Clear
      </button>
    </div>

    <!-- All Groups Filter -->
    <div>
      <button
        :class="getFilterStyle(filters[0])"
        @click="handleFilterChange(filters[0].id)"
        class="w-full"
      >
        <component 
          :is="filters[0].icon"
          class="w-5 h-5"
          :class="modelValue === filters[0].id 
            ? 'text-accent-400 dark:text-accent-300' 
            : 'text-neutral-400 dark:text-neutral-500'"
        />
        <div class="flex-1 text-left">
          <div class="text-sm font-medium">
            {{ filters[0].label }}
          </div>
          <div class="text-xs opacity-75">
            {{ filters[0].description }}
          </div>
        </div>
        <div class="text-sm opacity-75">
          {{ filters[0].count }}
        </div>
      </button>
    </div>

    <!-- Processing Status Filters -->
    <div class="space-y-2">
      <h4 class="text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase">
        Processing Status
      </h4>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
        <button
          v-for="filter in statusFilters"
          :key="filter.id"
          :class="getFilterStyle(filter)"
          @click="handleFilterChange(filter.id)"
        >
          <component 
            :is="filter.icon"
            class="w-5 h-5"
            :class="modelValue === filter.id 
              ? filter.variant === 'error' ? 'text-red-400' : 'text-accent-400 dark:text-accent-300'
              : 'text-neutral-400 dark:text-neutral-500'"
          />
          <div class="flex-1">
            <div class="text-sm font-medium">
              {{ filter.label }}
            </div>
            <div class="text-xs opacity-75">
              {{ filter.count }}
            </div>
          </div>
        </button>
      </div>
    </div>

    <!-- Event Type Filters -->
    <div class="space-y-2">
      <h4 class="text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase">
        Event Types
      </h4>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
        <button
          v-for="filter in typeFilters"
          :key="filter.id"
          :class="getFilterStyle(filter)"
          @click="handleFilterChange(filter.id)"
        >
          <component 
            :is="filter.icon"
            class="w-5 h-5"
            :class="modelValue === filter.id 
              ? 'text-accent-400 dark:text-accent-300' 
              : 'text-neutral-400 dark:text-neutral-500'"
          />
          <div class="flex-1">
            <div class="text-sm font-medium">
              {{ filter.label }}
            </div>
            <div class="text-xs opacity-75">
              {{ filter.count }}
            </div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>