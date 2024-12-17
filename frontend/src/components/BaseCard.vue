<!-- components/BaseCard.vue -->
<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  }
});
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm border border-neutral-200 overflow-hidden">
    <div class="p-4 border-b border-neutral-100" v-if="$slots.header || title">
      <slot name="header">
        <h3 class="text-lg font-semibold text-primary-500">{{ title }}</h3>
      </slot>
    </div>
    
    <div class="p-4">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="p-4 bg-neutral-50 border-t border-neutral-100">
      <slot name="footer"></slot>
    </div>
  </div>
</template>