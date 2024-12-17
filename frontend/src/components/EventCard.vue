# components/EventCard.vue
<script setup>
import { ref, computed } from 'vue';
import { 
  Calendar, 
  Clock, 
  MapPin, 
  Users, 
  Building2, 
  StickyNote 
} from 'lucide-vue-next';
import DateTimeInput from './DateTimeInput.vue';
import CollapsibleInfoCard from './CollapsibleInfoCard.vue';
import { 
  isValidDateTimeRange, 
  formatDateTimeForDisplay, 
  createBackendDateTime,
  convertTo12Hour,
  convertTo24Hour 
} from '../utils/datetime';

const props = defineProps({
  startDate: {
    type: String,
    required: true
  },
  startTime: {
    type: String,
    required: true
  },
  endDate: {
    type: String,
    required: false,
    default: null
  },
  endTime: {
    type: String,
    required: false,
    default: null
  },
  location: {
    type: String,
    default: ''
  },
  venue: {
    type: String,
    default: ''
  },
  attendees: {
    type: Array,
    default: () => []
  },
  notes: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update']);

// Convert the 24h time from backend to 12h format for display
const displayStartTime = computed(() => {
  if (!props.startTime) return '';
  return convertTo12Hour(props.startTime);
});

const displayEndTime = computed(() => {
  if (!props.endTime) return '';
  return convertTo12Hour(props.endTime);
});

// Computed property to check datetime validity
const isValidDateTime = computed(() => {
  // Convert times to 24h format before validation
  const start24h = convertTo24Hour(props.startTime);
  const end24h = convertTo24Hour(props.endTime);
  
  return isValidDateTimeRange(
    props.startDate,
    start24h,
    props.endDate,
    end24h
  );
});

// Update handlers
const handleStartDateChange = (value) => {
  emit('update', { 
    field: 'startDate', 
    value,
    isoDateTime: createBackendDateTime(value, convertTo24Hour(displayStartTime.value))
  });
};

const handleStartTimeChange = (value) => {
  emit('update', { 
    field: 'startTime', 
    value: convertTo24Hour(value),  // Convert to 24h for backend
    isoDateTime: createBackendDateTime(props.startDate, convertTo24Hour(value))
  });
};

const handleEndDateChange = (value) => {
  emit('update', { 
    field: 'endDate', 
    value,
    isoDateTime: createBackendDateTime(value, props.endTime ? convertTo24Hour(displayEndTime.value) : convertTo24Hour(displayStartTime.value))
  });
};

const handleEndTimeChange = (value) => {
  emit('update', { 
    field: 'endTime', 
    value: convertTo24Hour(value),  // Convert to 24h for backend
    isoDateTime: createBackendDateTime(props.endDate || props.startDate, convertTo24Hour(value))
  });
};

const handleUpdate = (field, value) => {
  emit('update', { field, value });
};

const handleAttendeesUpdate = (value) => {
  const newAttendees = value.split('\n')
    .filter(name => name.trim())
    .map(name => {
      // Parse name and email if format is "name <email>"
      const match = name.match(/^(.+?)\s*(?:<(.+?)>)?$/);
      if (match) {
        const [_, attendeeName, email] = match;
        return {
          name: attendeeName.trim(),
          email: email ? email.trim() : null
        };
      }
      // If no email format found, just use name with null email
      return {
        name: name.trim(),
        email: null
      };
    });
  
  emit('update', { field: 'attendees', value: newAttendees });
};

const formatAttendees = (attendees) => {
  return attendees.map(attendee => {
    if (attendee.email) {
      return `${attendee.name} <${attendee.email}>`;
    }
    return attendee.name;
  }).join('\n');
};
</script>

<template>
  <div class="space-y-3">
    <!-- Start Date and Time -->
    <div class="bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700 p-4 start-date-card">
      <div class="flex items-center gap-3 mb-4">
        <div class="p-2 rounded-lg bg-accent-50 dark:bg-accent-400/20">
          <Calendar class="w-5 h-5 text-accent-400 dark:text-accent-300" />
        </div>
        <h3 class="font-medium text-neutral-900 dark:text-neutral-100">
          Start Date & Time
        </h3>
      </div>
      <div class="flex gap-4">
        <DateTimeInput
          :model-value="startDate"
          type="date"
          @update:model-value="handleStartDateChange"
          class="w-1/2 calendar-selector"
        />
        <DateTimeInput
          :model-value="displayStartTime"
          type="time"
          @update:model-value="handleStartTimeChange"
          class="w-1/2"
        />
      </div>
    </div>

    <!-- End Date and Time -->
    <div class="bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700 p-4 end-date-card">
      <div class="flex items-center gap-3 mb-4">
        <div class="p-2 rounded-lg bg-accent-50 dark:bg-accent-400/20">
          <Clock class="w-5 h-5 text-accent-400 dark:text-accent-300" />
        </div>
        <h3 class="font-medium text-neutral-900 dark:text-neutral-100">
          End Date & Time
        </h3>
      </div>
      <div class="flex gap-4">
        <DateTimeInput
          :model-value="endDate || ''"
          type="date"
          :min-date="startDate"
          @update:model-value="handleEndDateChange"
          class="w-1/2"
        />
        <DateTimeInput
          :model-value="displayEndTime"
          type="time"
          @update:model-value="handleEndTimeChange"
          class="w-1/2"
        />
      </div>
    </div>

    <!-- Validation Message -->
    <div 
      v-if="!isValidDateTime && endDate && endTime" 
      class="text-red-500 dark:text-red-400 text-sm px-4"
    >
      End date and time must be after start date and time.
    </div>

    <!-- Location -->
    <CollapsibleInfoCard
      :icon="MapPin"
      title="Location"
      :content="location"
      @update:content="value => handleUpdate('location', value)"
    />
    
    <!-- Venue -->
    <CollapsibleInfoCard
      :icon="Building2"
      title="Venue"
      :content="venue"
      @update:content="value => handleUpdate('venue', value)"
    />
    
    <!-- Attendees -->
    <CollapsibleInfoCard
      :icon="Users"
      title="Attendees"
      :content="formatAttendees(attendees)"
      @update:content="handleAttendeesUpdate"
    />
    
    <!-- Notes -->
    <CollapsibleInfoCard
      :icon="StickyNote"
      title="Notes"
      :content="notes"
      @update:content="value => handleUpdate('notes', value)"
    />
  </div>
</template>

<style scoped>
.space-y-3 > * {
  position: relative;
}

.start-date-card {
  z-index: 20;
}

.end-date-card {
  z-index: 10;
}

.calendar-selector {
  z-index: 30;
}

.start-date-card,
.end-date-card {
  overflow: visible;
}
</style>