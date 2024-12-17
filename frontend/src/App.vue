<!-- App.vue -->
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';
import { ToastContainer } from './components/toast';
import { ToastService } from './components/toast';
import { useUiPreferencesStore } from './stores/uiPreferencesStore';

const uiStore = useUiPreferencesStore();

// Get reactive toasts array
const toasts = ToastService.getToasts();

const router = useRouter();
const isTransitioning = ref(false);

const handleBeforeLeave = () => {
  if (typeof window !== 'undefined') {
    isTransitioning.value = true;
    document.documentElement.style.overflow = 'hidden';
  }
};

const handleAfterLeave = () => {
  if (typeof window !== 'undefined') {
    isTransitioning.value = false;
    document.documentElement.style.overflow = '';
  }
};

// Clean up on component unmount
onMounted(() => {
  return () => {
    if (typeof window !== 'undefined') {
      document.documentElement.style.overflow = '';
    }
  };
});

// Apply initial theme and watch for system theme changes
onMounted(() => {
  // Apply initial theme
  uiStore.applyTheme();

  // Watch for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  mediaQuery.addEventListener('change', () => {
    if (uiStore.theme === 'system') {
      uiStore.applyTheme();
    }
  });
});
</script>

<template>
  <div 
    class="min-h-screen bg-primary-50 dark:bg-primary-900 flex flex-col"
    :class="{ 'overflow-hidden': isTransitioning }"
  >
    <AppHeader />

    <!-- Add some spaces between header and footer during transition -->
    <div class="flex-1 min-h-[90vh]">
      <router-view v-slot="{ Component }">
        <transition 
          name="page" 
          mode="out-in"
          @before-leave="handleBeforeLeave"
          @after-leave="handleAfterLeave"
        >
          <component 
            :is="Component" 
            :key="router.currentRoute.value.path" 
          />
        </transition>
      </router-view>
    </div>
    <AppFooter />
    <!-- Toast Container -->
    <ToastContainer 
      :toasts="toasts"
      @close="ToastService.remove"
    />
  </div>
</template>

<style>
/* Page transition styles */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Prevent layout shift during transitions */
.page-leave-active {
  position: absolute;
  width: 100%;
}

/* Smooth scrolling */
@media (prefers-reduced-motion: no-preference) {
  html {
    scroll-behavior: smooth;
  }
}

/* Base styles */
#app {
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

/* Container styles */
.max-w-3xl {
  position: relative;
}

/* Ensure consistent spacing */
main {
  min-height: calc(100vh - 4rem);
  position: relative;
  width: 100%;
}
</style>