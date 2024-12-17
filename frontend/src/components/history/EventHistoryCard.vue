<!-- components/history/EventHistoryCard.vue -->
<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { 
  Clock, 
  MapPin, 
  Users, 
  MoreVertical,
  Trash2,
  Download,
  Edit,
  AlertCircle
} from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { formatDateTimeForDisplay } from '@/utils/datetime';

const router = useRouter();
const props = defineProps({
  event: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['delete', 'download']);
const showMenu = ref(false);

// Format date and time for display
const formattedDateTime = computed(() => {
  return formatDateTimeForDisplay(props.event.start_datetime);
});

const getStatusColor = computed(() => {
  if (props.event.processing_error) return 'bg-red-400';
  if (!props.event.processing_complete) return 'bg-yellow-400';
  return 'bg-green-400';
});

const formatAttendees = computed(() => {
  const attendees = props.event.attendees;
  if (!attendees?.length) return 'No attendees';
  if (attendees.length <= 2) return attendees.map(a => a.name).join(', ');
  return `${attendees[0].name}, ${attendees[1].name} +${attendees.length - 2} more`;
});

const handleAction = (action) => {
  showMenu.value = false;
  if (action === 'edit') {
    router.push(`/events/${props.event.id}`);
    return;
  }
  emit(action, props.event.id);
};

const formatLocation = computed(() => {
  const { location, venue } = props.event;
  if (venue) return `${location} - ${venue}`;
  return location || 'No location specified';
});

const closeMenu = (e) => {
  if (!e.target.closest('.menu-container')) {
    showMenu.value = false;
  }
};

// Add/remove event listeners
onMounted(() => {
  document.addEventListener('click', closeMenu);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', closeMenu);
});
</script>

<template>
  <div 
    class="group bg-white dark:bg-primary-800 rounded-lg border border-neutral-200 dark:border-primary-700 hover:border-neutral-300 dark:hover:border-primary-600 transition-all duration-200"
  >
    <div class="p-4 sm:p-6">
      <!-- Header -->
      <div class="flex items-start justify-between gap-4">
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h3 class="text-lg font-medium text-primary-500 dark:text-primary-100 truncate">
              {{ event.title }}
            </h3>
            <span 
              class="w-2 h-2 rounded-full"
              :class="getStatusColor"
            />
            
            <!-- Processing Error Indicator -->
            <span v-if="event.processing_error" 
                  class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400">
              <AlertCircle class="w-3 h-3" />
              Error
            </span>
          </div>
          
          <!-- Event Details -->
          <div class="space-y-2">
            <div class="flex items-center gap-2 text-sm text-neutral-600 dark:text-neutral-400">
              <Clock class="w-4 h-4" />
              <span>{{ formattedDateTime }}</span>
            </div>
            
            <div class="flex items-center gap-2 text-sm text-neutral-600 dark:text-neutral-400">
              <MapPin class="w-4 h-4" />
              <span>{{ formatLocation }}</span>
            </div>
            
            <div class="flex items-center gap-2 text-sm text-neutral-600 dark:text-neutral-400">
              <Users class="w-4 h-4" />
              <span>{{ formatAttendees }}</span>
            </div>

            <!-- Suggestions -->
            <div v-if="event.suggestions" 
                 class="text-sm text-neutral-600 dark:text-neutral-400 mt-2 whitespace-pre-line">
              {{ event.suggestions }}
            </div>
          </div>
        </div>

        <!-- Action Menu -->
        <div class="relative menu-container">
          <button 
            @click.stop="showMenu = !showMenu"
            class="p-1 text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300 rounded-lg transition-colors"
            :class="{ 'bg-neutral-50 dark:bg-primary-700': showMenu }"
          >
            <MoreVertical class="w-5 h-5" />
          </button>

          <!-- Dropdown Menu -->
          <div 
            v-if="showMenu"
            class="absolute right-0 mt-2 w-48 bg-white dark:bg-primary-800 rounded-lg shadow-lg border border-neutral-200 dark:border-primary-700 py-1 z-10"
          >
            <button 
              v-for="action in [
                { icon: Edit, label: 'Edit', emit: 'edit' },
                { icon: Download, label: 'Export', emit: 'download' },
                { icon: Trash2, label: 'Delete', emit: 'delete', dangerous: true }
              ]"
              :key="action.label"
              @click="handleAction(action.emit)"
              class="w-full px-4 py-2 text-sm flex items-center gap-2 hover:bg-neutral-50 dark:hover:bg-primary-700 transition-colors"
              :class="action.dangerous ? 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20' : 'text-neutral-700 dark:text-neutral-200'"
            >
              <component :is="action.icon" class="w-4 h-4" />
              {{ action.label }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>