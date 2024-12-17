<!-- components/Tooltip.vue -->
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  position: {
    type: String,
    default: 'top',
    validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value)
  },
  delay: {
    type: Number,
    default: 0
  }
});

const tooltipVisible = ref(false);
const tooltipRef = ref(null);
let showTimeout = null;
let hideTimeout = null;

const showTooltip = () => {
  clearTimeout(hideTimeout);
  if (props.delay) {
    showTimeout = setTimeout(() => {
      tooltipVisible.value = true;
    }, props.delay);
  } else {
    tooltipVisible.value = true;
  }
};

const hideTooltip = () => {
  clearTimeout(showTimeout);
  hideTimeout = setTimeout(() => {
    tooltipVisible.value = false;
  }, 100);
};

// Position classes based on the position prop
const positionClasses = {
  top: '-top-2 left-1/2 -translate-x-1/2 -translate-y-full',
  bottom: '-bottom-2 left-1/2 -translate-x-1/2 translate-y-full',
  left: 'top-1/2 -left-2 -translate-x-full -translate-y-1/2',
  right: 'top-1/2 -right-2 translate-x-full -translate-y-1/2'
};

// Arrow classes based on the position prop
const arrowClasses = {
  top: 'bottom-[-6px] left-1/2 -translate-x-1/2 border-t-neutral-700 border-x-transparent border-b-transparent',
  bottom: 'top-[-6px] left-1/2 -translate-x-1/2 border-b-neutral-700 border-x-transparent border-t-transparent',
  left: 'right-[-6px] top-1/2 -translate-y-1/2 border-l-neutral-700 border-y-transparent border-r-transparent',
  right: 'left-[-6px] top-1/2 -translate-y-1/2 border-r-neutral-700 border-y-transparent border-l-transparent'
};

onBeforeUnmount(() => {
  clearTimeout(showTimeout);
  clearTimeout(hideTimeout);
});
</script>

<template>
  <div 
    class="relative inline-block"
    @mouseenter="showTooltip"
    @mouseleave="hideTooltip"
    @focus="showTooltip"
    @blur="hideTooltip"
  >
    <slot></slot>
    
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div 
        v-if="tooltipVisible"
        ref="tooltipRef"
        class="absolute z-50 px-2 py-1 text-sm text-white bg-neutral-700 rounded-md shadow-lg whitespace-nowrap pointer-events-none"
        :class="positionClasses[position]"
        role="tooltip"
      >
        {{ content }}
        <div 
          class="absolute w-0 h-0 border-4"
          :class="arrowClasses[position]"
        ></div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>