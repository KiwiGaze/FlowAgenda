<!-- components/DateTimeInput.vue-->
<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { Calendar, Clock, ChevronLeft, ChevronRight } from 'lucide-vue-next';
import { convertTo12Hour, convertTo24Hour } from '../utils/datetime';

// Constants
const TIME_REGEX = /^(0?[1-9]|1[0-2]):([0-5][0-9])(AM|PM)$/i;

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'datetime'
  },
  label: {
    type: String,
    default: ''
  },
  minDate: {
    type: String,
    default: null
  },
  maxDate: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['update:modelValue']);

const showCalendar = ref(false);
const inputRef = ref(null);
const inputValue = ref('');
const isInputFocused = ref(false);
const validationError = ref('');

// Time input segments
const hours = ref('');
const minutes = ref('');
const period = ref('AM');

// Date boundaries
const minDate = computed(() => props.minDate ? new Date(props.minDate) : new Date('1900-01-01'));
const maxDate = computed(() => props.maxDate ? new Date(props.maxDate) : new Date('2100-12-31'));

// Calendar state
const currentMonth = ref(new Date());
const selectedDate = ref(props.modelValue ? new Date(props.modelValue) : new Date());

// Parse incoming time value
const parseTimeValue = (value) => {
  if (!value) return;
  
  const match = value.match(/^(\d{1,2}):(\d{2})(AM|PM)$/i);
  if (match) {
    const [_, h, m, p] = match;
    hours.value = h.padStart(2, '0');
    minutes.value = m;
    period.value = p.toUpperCase();
    inputValue.value = `${hours.value}:${minutes.value}`;
  }
};

// Format complete time string
const formatTimeValue = () => {
  if (!hours.value || !minutes.value) return '';
  return `${hours.value.padStart(2, '0')}:${minutes.value}${period.value}`;
};

// Handle time input changes
const handleTimeInput = (e) => {
  let value = e.target.value;
  value = value.replace(/[^\d:]/g, '');
  
  const match = value.match(/^(\d{0,2}):?(\d{0,2})$/);
  if (match) {
    let [_, h = '', m = ''] = match;
    
    if (h) {
      h = h.slice(0, 2);
      const hoursNum = parseInt(h);
      if (hoursNum > 12) h = '12';
      if (h.length === 2 && hoursNum < 1) h = '01';
      hours.value = h;
    }
    
    if (m) {
      m = m.slice(0, 2);
      const minutesNum = parseInt(m);
      if (minutesNum > 59) m = '59';
      minutes.value = m;
    }
    
    if (h.length === 2 && !value.includes(':')) {
      value = h + ':' + m;
    }
  }
  
  inputValue.value = value;
  const timeWith12h = `${inputValue.value}${period.value}`;
  validateTime(timeWith12h);
  
  if (TIME_REGEX.test(timeWith12h)) {
    // Keep the original 12h format when emitting
    emit('update:modelValue', timeWith12h);
  }
};

// Update togglePeriod to maintain consistent format
const togglePeriod = () => {
  period.value = period.value === 'AM' ? 'PM' : 'AM';
  const timeWith12h = `${inputValue.value}${period.value}`;
  if (TIME_REGEX.test(timeWith12h)) {
    // Keep the original 12h format when emitting
    emit('update:modelValue', timeWith12h);
  }
};

// Time validation
const validateTime = (value) => {
  if (!value) {
    validationError.value = '';
    return;
  }
  
  if (!TIME_REGEX.test(formatTimeValue())) {
    validationError.value = 'Invalid time format (HH:MM AM/PM)';
    return;
  }
  
  validationError.value = '';
};

// Calendar selection handler
const selectDate = (day) => {
  if (!day) return;
  
  const selectedDate = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth(),
    day
  );

  if (!isDateSelectable(selectedDate)) {
    validationError.value = 'Selected date is outside allowed range';
    return;
  }

  const formattedDate = formatDateToISO(selectedDate);
  inputValue.value = formattedDate;
  emit('update:modelValue', formattedDate);
  showCalendar.value = false;
};

// Format date to ISO (YYYY-MM-DD)
const formatDateToISO = (date) => {
  return date.toISOString().split('T')[0];
};

// Calendar navigation
const prevMonth = () => {
  currentMonth.value = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth() - 1
  );
};

const nextMonth = () => {
  currentMonth.value = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth() + 1
  );
};

// Calendar computed properties
const daysInMonth = computed(() => {
  const year = currentMonth.value.getFullYear();
  const month = currentMonth.value.getMonth();
  return new Date(year, month + 1, 0).getDate();
});

const firstDayOfMonth = computed(() => {
  const year = currentMonth.value.getFullYear();
  const month = currentMonth.value.getMonth();
  return new Date(year, month, 1).getDay();
});

const calendarDays = computed(() => {
  const days = [];
  const total = daysInMonth.value;
  const firstDay = firstDayOfMonth.value;

  for (let i = 0; i < firstDay; i++) {
    days.push(null);
  }

  for (let i = 1; i <= total; i++) {
    days.push(i);
  }

  return days;
});

// Date selectability check
const isDateSelectable = (date) => {
  return date >= minDate.value && date <= maxDate.value;
};

// Handle input changes
const handleInput = (e) => {
  if (props.type === 'date') {
    const value = e.target.value;
    // Ensure value is in ISO format (YYYY-MM-DD)
    if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
      emit('update:modelValue', value);
    }
  } else {
    handleTimeInput(e);
  }
};

// Event handlers for calendar popup
const handleClickOutside = (event) => {
  if (!event.target.closest('.datetime-picker')) {
    showCalendar.value = false;
  }
};

const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    showCalendar.value = false;
  }
};

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  if (props.type === 'date') {
    inputValue.value = newValue;
  } else if (props.type === 'time') {
    if (newValue.includes('AM') || newValue.includes('PM')) {
      // Value is already in 12-hour format
      inputValue.value = newValue.slice(0, 5); // Remove AM/PM for input display
      period.value = newValue.slice(-2);
      parseTimeValue(newValue);
    } else {
      // Value is in 24-hour format, convert to 12-hour
      const time12h = convertTo12Hour(newValue);
      inputValue.value = time12h.slice(0, 5); // Remove AM/PM for input display
      period.value = time12h.slice(-2);
      parseTimeValue(time12h);
    }
  }
}, { immediate: true });

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
  <div class="datetime-picker relative">
    <label 
      v-if="label" 
      class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1"
    >
      {{ label }}
    </label>
    
    <div class="relative">
      <!-- Date Input -->
      <div v-if="type === 'date'" class="date-input-wrapper">
        <input
          ref="inputRef"
          v-model="inputValue"
          type="date"
          :min="minDate ? formatDateToISO(minDate) : '1900-01-01'"
          :max="maxDate ? formatDateToISO(maxDate) : '2100-12-31'"
          class="w-full px-4 py-2 border border-neutral-300 dark:border-neutral-600 
                 bg-white dark:bg-neutral-800 rounded-lg shadow-sm 
                 text-neutral-900 dark:text-neutral-100
                 placeholder-neutral-400 dark:placeholder-neutral-500
                 transition-all duration-200"
          :class="{
            'focus:ring-2 focus:ring-accent-400 focus:border-transparent': !validationError,
            'border-red-300 dark:border-red-500 focus:ring-red-400 focus:border-red-300': validationError,
            'pr-10': true
          }"
          @focus="isInputFocused = true"
          @blur="isInputFocused = false"
          @input="handleInput"
        />
        
        <div 
          class="absolute right-3 top-1/2 -translate-y-1/2 transition-colors duration-200 cursor-pointer"
          :class="{
            'text-accent-400 dark:text-accent-300': isInputFocused && !validationError,
            'text-neutral-400 dark:text-neutral-500': !isInputFocused && !validationError,
            'text-red-400 dark:text-red-500': validationError
          }"
          @click="showCalendar = !showCalendar"
        >
          <Calendar class="w-5 h-5" />
        </div>
      </div>

      <!-- Time Input -->
      <div v-else class="time-input-wrapper flex">
        <div class="relative flex-1">
          <input
            ref="inputRef"
            v-model="inputValue"
            type="text"
            placeholder="HH:MM"
            maxlength="5"
            class="w-full px-4 py-2 border border-neutral-300 dark:border-neutral-600 
                   bg-white dark:bg-neutral-800 rounded-lg shadow-sm 
                   text-neutral-900 dark:text-neutral-100
                   placeholder-neutral-400 dark:placeholder-neutral-500
                   transition-all duration-200"
            :class="{
              'focus:ring-2 focus:ring-accent-400 focus:border-transparent': !validationError,
              'border-red-300 dark:border-red-500 focus:ring-red-400 focus:border-red-300': validationError,
              'pr-20': true
            }"
            @focus="isInputFocused = true"
            @blur="isInputFocused = false"
            @input="handleTimeInput"
          />

          <!-- Period Toggle Button -->
          <button
            @click="togglePeriod"
            type="button"
            class="absolute right-10 top-1/2 -translate-y-1/2 px-2 py-1 text-sm 
                   text-neutral-600 dark:text-neutral-400 
                   hover:text-accent-400 dark:hover:text-accent-300 
                   transition-colors"
          >
            {{ period }}
          </button>

          <div 
            class="absolute right-3 top-1/2 -translate-y-1/2 transition-colors duration-200"
            :class="{
              'text-accent-400 dark:text-accent-300': isInputFocused && !validationError,
              'text-neutral-400 dark:text-neutral-500': !isInputFocused && !validationError,
              'text-red-400 dark:text-red-500': validationError
            }"
          >
            <Clock class="w-5 h-5" />
          </div>
        </div>
      </div>
    </div>

    <!-- Validation Error Message -->
    <div
      v-if="validationError"
      class="text-red-500 dark:text-red-400 text-sm mt-1"
    >
      {{ validationError }}
    </div>

    <!-- Calendar Popup -->
    <div
      v-if="showCalendar && type === 'date'"
      class="absolute z-[100] mt-2 bg-white dark:bg-neutral-800 rounded-lg 
             shadow-lg border border-neutral-200 dark:border-neutral-700 p-4 w-80"
    >
      <!-- Month Navigation -->
      <div class="flex items-center justify-between mb-4">
        <button
          @click="prevMonth"
          class="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 
                 rounded-full transition-colors"
        >
          <ChevronLeft class="w-5 h-5 text-neutral-600 dark:text-neutral-400" />
        </button>
        
        <span class="font-medium text-neutral-900 dark:text-neutral-100">
          {{ currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) }}
        </span>
        
        <button
          @click="nextMonth"
          class="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 
                 rounded-full transition-colors"
        >
          <ChevronRight class="w-5 h-5 text-neutral-600 dark:text-neutral-400" />
        </button>
      </div>

      <!-- Calendar Grid -->
      <div class="grid grid-cols-7 gap-1">
        <!-- Weekday Headers -->
        <template v-for="day in ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']">
          <div class="text-center text-sm font-medium text-neutral-500 dark:text-neutral-400 p-2">
            {{ day }}
          </div>
        </template>

        <!-- Calendar Days -->
        <template v-for="(day, index) in calendarDays" :key="index">
          <button
            v-if="day"
            @click="selectDate(day)"
            class="p-2 rounded-full text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :class="{
              'bg-accent-400 text-white hover:bg-accent-500': 
                day === selectedDate.getDate() &&
                currentMonth.getMonth() === selectedDate.getMonth() &&
                currentMonth.getFullYear() === selectedDate.getFullYear(),
              'hover:bg-accent-50 dark:hover:bg-accent-400/20 text-neutral-900 dark:text-neutral-100': 
                !(day === selectedDate.getDate() &&
                currentMonth.getMonth() === selectedDate.getMonth() &&
                currentMonth.getFullYear() === selectedDate.getFullYear()),
              'text-neutral-300 dark:text-neutral-600': !isDateSelectable(new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day))
            }"
            :disabled="!isDateSelectable(new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day))"
          >
            {{ day }}
          </button>
          <div v-else class="p-2"></div>
        </template>
      </div>

      <!-- Current Date Shortcut -->
      <div class="mt-4 pt-4 border-t border-neutral-200 dark:border-neutral-700">
        <button
          @click="() => { selectDate(new Date().getDate()); currentMonth = new Date(); }"
          class="w-full px-3 py-2 text-sm text-center text-accent-400 dark:text-accent-300 
                 hover:bg-accent-50 dark:hover:bg-accent-400/20 rounded-lg transition-colors"
        >
          Today
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.datetime-picker {
  z-index: 1;
}

.datetime-picker:focus-within {
  z-index: 50;
}

.time-input-wrapper,
.date-input-wrapper {
  position: relative;
}

/* Time input specific styles */
input[type="text"] {
  font-variant-numeric: tabular-nums;
}

/* Remove browser default calendar icon for date input */
input[type="date"]::-webkit-calendar-picker-indicator {
  display: none;
}

input[type="date"] {
  position: relative;
}

/* Set placeholder color for date input */
input[type="date"]::-webkit-datetime-edit-fields-wrapper {
  color: inherit;
}

input[type="date"]::-webkit-datetime-edit-text {
  color: inherit;
  opacity: 1;
}

input[type="date"]::-webkit-datetime-edit-month-field,
input[type="date"]::-webkit-datetime-edit-day-field,
input[type="date"]::-webkit-datetime-edit-year-field {
  color: inherit;
}

/* Calendar specific styles */
.calendar-day {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-day:hover:not(:disabled) {
  background-color: rgba(59, 130, 246, 0.1);
}

.calendar-day.selected {
  background-color: #3b82f6;
  color: white;
}

.calendar-day.selected:hover {
  background-color: #2563eb;
}
</style>