<!-- components/AppHeader.vue -->
<script setup>
import DesktopHeader from './header/DesktopHeader.vue';
import MobileHeader from './header/MobileHeader.vue';
</script>

<template>
  <div>
    <DesktopHeader class="hidden md:block" />
    <MobileHeader />
    <!-- Spacer to prevent content from going under fixed header -->
    <div class="h-16"></div>
  </div>
</template>