<!-- components/toast/ToastNotification.vue -->
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { XCircle, CheckCircle, AlertCircle, Info, X } from 'lucide-vue-next';

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'info', 'warning'].includes(value)
  },
  duration: {
    type: Number,
    default: 3000
  },
  position: {
    type: String,
    default: 'top-right',
    validator: (value) => [
      'top-right',
      'top-left',
      'bottom-right',
      'bottom-left',
      'top-center',
      'bottom-center'
    ].includes(value)
  }
});

const emit = defineEmits(['close']);
const progress = ref(100);
const isVisible = ref(false);
const isClosing = ref(false);
const isPaused = ref(false);
const remainingTime = ref(props.duration);

let rafId;
let startTime;
let lastUpdateTime;
let pauseStartTime;

const updateProgress = () => {
  if (isPaused.value) {
    lastUpdateTime = performance.now();
    rafId = requestAnimationFrame(updateProgress);
    return;
  }

  const currentTime = performance.now();
  const deltaTime = currentTime - lastUpdateTime;
  lastUpdateTime = currentTime;

  remainingTime.value = Math.max(0, remainingTime.value - deltaTime);
  progress.value = (remainingTime.value / props.duration) * 100;

  if (remainingTime.value <= 0) {
    closeToast();
    return;
  }

  rafId = requestAnimationFrame(updateProgress);
};

const startTimer = () => {
  isPaused.value = false;
  startTime = performance.now();
  lastUpdateTime = startTime;
  rafId = requestAnimationFrame(updateProgress);
};

const pauseTimer = () => {
  isPaused.value = true;
  pauseStartTime = performance.now();
};

const resumeTimer = () => {
  if (!isPaused.value) return;

  const pauseDuration = performance.now() - pauseStartTime;
  startTime += pauseDuration;
  lastUpdateTime = performance.now();
  isPaused.value = false;
};

onMounted(() => {
  // Trigger entrance animation
  setTimeout(() => {
    isVisible.value = true;
  }, 50);

  if (props.duration) {
    startTimer();
  }
});

onBeforeUnmount(() => {
  if (rafId) {
    cancelAnimationFrame(rafId);
  }
});

const closeToast = () => {
  if (rafId) {
    cancelAnimationFrame(rafId);
  }
  isClosing.value = true;
  // Allow animation to complete before emitting close
  setTimeout(() => {
    emit('close', props.id);
  }, 300);
};

const getIcon = () => {
  switch (props.type) {
    case 'success':
      return CheckCircle;
    case 'error':
      return XCircle;
    case 'warning':
      return AlertCircle;
    default:
      return Info;
  }
};

const getTypeClasses = () => {
  const baseClasses = 'relative overflow-hidden';
  
  switch (props.type) {
    case 'success':
      return `${baseClasses} bg-green-50 border-green-200 dark:bg-green-900 dark:border-green-800`;
    case 'error':
      return `${baseClasses} bg-red-50 border-red-200 dark:bg-red-900 dark:border-red-800`;
    case 'warning':
      return `${baseClasses} bg-yellow-50 border-yellow-200 dark:bg-yellow-900 dark:border-yellow-800`;
    default:
      return `${baseClasses} bg-blue-50 border-blue-200 dark:bg-blue-900 dark:border-blue-800`;
  }
};

const getIconColor = () => {
  switch (props.type) {
    case 'success':
      return 'text-green-500 dark:text-green-400';
    case 'error':
      return 'text-red-500 dark:text-red-400';
    case 'warning':
      return 'text-yellow-500 dark:text-yellow-400';
    default:
      return 'text-blue-500 dark:text-blue-400';
  }
};

const getProgressColor = () => {
  switch (props.type) {
    case 'success':
      return 'bg-green-500/20 dark:bg-green-400/20';
    case 'error':
      return 'bg-red-500/20 dark:bg-red-400/20';
    case 'warning':
      return 'bg-yellow-500/20 dark:bg-yellow-400/20';
    default:
      return 'bg-blue-500/20 dark:bg-blue-400/20';
  }
};

const getTextColor = () => {
  switch (props.type) {
    case 'success':
      return 'text-green-800 dark:text-green-200';
    case 'error':
      return 'text-red-800 dark:text-red-200';
    case 'warning':
      return 'text-yellow-800 dark:text-yellow-200';
    default:
      return 'text-blue-800 dark:text-blue-200';
  }
};
</script>

<template>
  <div
    class="group flex items-start gap-3 px-4 py-3 rounded-lg border shadow-md w-[320px] max-w-[420px] transition-all duration-300"
    :class="[
      getTypeClasses(),
      {
        'translate-x-0 opacity-100': isVisible && !isClosing,
        'translate-x-full opacity-0': !isVisible || isClosing,
      }
    ]"
    @mouseenter="pauseTimer"
    @mouseleave="resumeTimer"
  >
    <!-- Icon -->
    <component 
      :is="getIcon()" 
      class="w-5 h-5 flex-shrink-0 mt-0.5 transition-colors"
      :class="getIconColor()"
    />

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <p 
        class="text-sm break-words transition-colors"
        :class="getTextColor()"
      >
        {{ message }}
      </p>
    </div>

    <!-- Close Button -->
    <button
      class="p-1 -mr-1 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-black/5 dark:hover:bg-white/5"
      :class="getIconColor()"
      @click="closeToast"
    >
      <X class="w-4 h-4" />
    </button>

    <!-- Progress Bar -->
    <div
      v-if="props.duration"
      class="absolute bottom-0 left-0 h-1 transition-all duration-[50ms]"
      :class="[getProgressColor(), { 'opacity-0': isClosing }]"
      :style="{ width: `${progress}%` }"
    />
  </div>
</template>

<style scoped>
.group {
  will-change: transform, opacity;
  backface-visibility: hidden;
  transform-origin: right center;
}
</style>