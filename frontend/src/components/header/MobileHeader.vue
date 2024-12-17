<!-- components/header/MobileHeader.vue -->
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  Menu,
  X,
  Search,
  Clock,
  Settings,
  LogOut,
  MessageSquare,
  Moon,
  Sun
} from 'lucide-vue-next';
import Tooltip from '../Tooltip.vue';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';
import { useSearchStore } from '@/stores/searchStore';
import { useDebounce } from '@/composables/useDebounce';
import SearchResults from '@/components/search/SearchResults.vue';

const uiStore = useUiPreferencesStore();
const router = useRouter();
const isMenuOpen = ref(false);
const isScrolled = ref(false);

// Add search related refs and store
const searchStore = useSearchStore();
const searchQuery = ref('');

// Add debounced search function
const debouncedSearch = useDebounce((query) => {
  searchStore.search(query);
}, 300);

// Add search handlers
const handleSearchInput = (e) => {
  const query = e.target.value;
  searchQuery.value = query;
  if (!query.trim()) {
    searchStore.clearSearch();
    return;
  }
  debouncedSearch(query);
};

const handleResultSelect = () => {
  searchQuery.value = '';
  searchStore.clearSearch();
  closeMenu();
};

const navigationItems = [
  { name: 'Chat', path: '/', icon: MessageSquare },
  { name: 'History', path: '/history', icon: Clock },
];

const toggleDarkMode = () => {
  const newTheme = uiStore.theme === 'dark' ? 'light' : 'dark';
  uiStore.setTheme(newTheme);
};

onMounted(() => {
  const handleScroll = () => {
    isScrolled.value = window.scrollY > 0;
  };
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
});

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
  document.body.style.overflow = isMenuOpen.value ? 'hidden' : '';
  
  // Add subtle animation to menu button
  if (isMenuOpen.value) {
    gsapAnimation();
  }
};

const gsapAnimation = () => {
  // Stagger animation for nav items
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach((item, index) => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    setTimeout(() => {
      item.style.transition = 'all 0.3s ease-out';
      item.style.opacity = '1';
      item.style.transform = 'translateY(0)';
    }, 100 + (index * 50));
  });
};

const closeMenu = () => {
  isMenuOpen.value = false;
  document.body.style.overflow = '';
};

const handleLogout = () => {
  closeMenu();
  // Implement logout logic
  console.log('Logging out...');
};
</script>

<template>
  <header 
    class="md:hidden fixed top-0 left-0 right-0 z-50 bg-white dark:bg-gray-900 transition-all duration-200 border-b border-neutral-200 dark:border-gray-800"
    :class="{ 'shadow-sm dark:shadow-none': isScrolled }"
  >
    <!-- Main Header -->
    <div class="px-4 h-16 flex items-center justify-between">
      <!-- Logo -->
      <a href="www.qiyijiazhen.com" target="_blank" class="flex items-center gap-2">
        <img 
          src="/src/assets/logo.svg" 
          alt="FlowAgenda" 
          class="w-8 h-8"
        />
        <span class="text-xl sm:text-2xl font-bold bg-gradient-to-r from-neutral-600 to-neutral-400 dark:from-neutral-300 dark:to-neutral-500 bg-clip-text text-transparent">
          FlowAgenda
        </span>
      </a>

      <!-- Header Actions -->
      <div class="flex items-center gap-2">

        <!-- Dark Mode Toggle -->
        <Tooltip :content="uiStore.theme === 'dark' ? 'Light Mode' : 'Dark Mode'" position="bottom">
          <button 
            @click="toggleDarkMode"
            class="p-2 text-neutral-600 dark:text-neutral-400 hover:text-accent-400 dark:hover:text-accent-300 hover:bg-accent-50 dark:hover:bg-accent-900/20 rounded-lg transition-colors"
          >
            <Sun v-if="uiStore.theme === 'dark'" class="w-5 h-5" />
            <Moon v-else class="w-5 h-5" />
          </button>
        </Tooltip>

        <!-- Menu Toggle -->
        <button 
          @click="toggleMenu"
          class="p-2 text-neutral-600 dark:text-neutral-400 hover:text-accent-400 dark:hover:text-accent-300 rounded-lg transition-colors"
        >
          <Menu v-if="!isMenuOpen" class="w-6 h-6" />
          <X v-else class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 -translate-x-full"
      enter-to-class="opacity-100 translate-x-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-x-0"
      leave-to-class="opacity-0 -translate-x-full"
    >
      <div 
        v-show="isMenuOpen"
        class="fixed inset-0 top-16 bg-white dark:bg-gray-900 z-40 overflow-y-auto pb-safe"
      >
        <!-- Search Bar -->
        <div class="p-4 border-b border-neutral-100 dark:border-gray-800">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400 dark:text-neutral-500" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              @input="handleSearchInput"
              class="w-full pl-10 pr-4 py-2.5 bg-neutral-50 dark:bg-gray-800 border border-neutral-200 dark:border-gray-700 rounded-lg text-neutral-900 dark:text-white placeholder:text-neutral-400 dark:placeholder:text-neutral-500 focus:ring-2 focus:ring-accent-400 focus:border-transparent transition-all"
            />
            
            <!-- Add Search Results -->
            <SearchResults
              v-if="searchQuery"
              :results="searchStore.searchResults"
              :is-loading="searchStore.isSearching"
              @select="handleResultSelect"
              class="absolute left-0 right-0 top-full mt-2 max-h-[60vh] overflow-y-auto z-50"
            />
          </div>
        </div>

        <!-- Navigation -->
        <nav class="px-2 py-4">
          <!-- Navigation Links -->
          <div class="space-y-1">
            <router-link
              v-for="item in navigationItems"
              :key="item.path"
              :to="item.path"
              class="nav-item flex items-center gap-3 px-4 py-3 rounded-lg text-neutral-600 dark:text-neutral-400 hover:bg-neutral-50 dark:hover:bg-gray-800 transition-colors"
              :class="{ 'bg-accent-50 dark:bg-accent-900/20 text-accent-400 dark:text-accent-300': $route.path === item.path }"
              @click="closeMenu"
            >
              <component :is="item.icon" class="w-5 h-5" />
              <span class="font-medium">{{ item.name }}</span>
            </router-link>
          </div>
        </nav>

        <!-- User Section -->
        <div class="px-4 py-4 border-t border-neutral-100 dark:border-gray-800">
          <div class="flex items-center gap-3 mb-4 px-2">
            <img 
              src="https://ui-avatars.com/api/?name=Kiwi&background=random" 
              alt="User avatar" 
              class="w-10 h-10 rounded-full bg-neutral-200 dark:bg-gray-700"
            />
            <div>
              <div class="font-medium text-neutral-900 dark:text-white">Kiwi</div>
              <div class="text-sm text-neutral-500 dark:text-neutral-400">kiwi@example.com</div>
            </div>
          </div>

          <!-- User Actions -->
          <div class="space-y-1">
            <button 
            to="/settings"
            @click="closeMenu"
              class="nav-item w-full flex items-center gap-3 px-6 py-3 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-50 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              <Settings class="w-5 h-5" />
              <span class="font-medium">Settings</span>
            </button>
            
            <button 
              @click="handleLogout"
              class="w-full flex items-center gap-3 px-6 py-3 text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
            >
              <LogOut class="w-5 h-5" />
              <span class="font-medium">Sign out</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </header>

  <!-- Backdrop -->
  <Transition
    enter-active-class="transition-opacity duration-300 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-200 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div 
      v-show="isMenuOpen"
      class="md:hidden fixed inset-0 bg-black/50 dark:bg-black/70 z-40 backdrop-blur-sm"
      @click="closeMenu"
    ></div>
  </Transition>
</template>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 1rem);
}
</style>