<!-- components/header/DesktopHeader.vue -->
<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';
import { 
  Search, 
  Clock,
  Settings,
  LogOut,
  MessageSquare,
  Moon,
  Sun
} from 'lucide-vue-next';
import Tooltip from '../Tooltip.vue';
import { Teleport } from 'vue';
import { useUiPreferencesStore } from '@/stores/uiPreferencesStore';
import { useSearchStore } from '@/stores/searchStore';
import SearchResults from '@/components/search/SearchResults.vue';
import { useDebounce } from '@/composables/useDebounce';

const uiStore = useUiPreferencesStore();
const router = useRouter();
const isScrolled = ref(false);
const showProfileMenu = ref(false);
const dropdownRef = ref(null);
const showSearch = ref(false);
const searchInput = ref(null);
const searchRef = ref(null);

// Add to existing setup
const searchStore = useSearchStore();
const searchQuery = ref('');

// Debounced search
const debouncedSearch = useDebounce((query) => {
  searchStore.search(query);
}, 300);

const handleSearchInput = (e) => {
  const query = e.target.value;
  searchQuery.value = query;
  if (!query.trim()) {
    searchStore.clearSearch();  // Clear results if query is empty
    return;
  }
  debouncedSearch(query);
};

const handleResultSelect = () => {
  closeSearch();
  searchQuery.value = '';
  searchStore.clearSearch();
};

const navigationItems = [
  { name: 'Chat', path: '/chat', icon: MessageSquare },
  { name: 'History', path: '/history', icon: Clock },
];

const toggleDarkMode = () => {
  const newTheme = uiStore.theme === 'dark' ? 'light' : 'dark';
  uiStore.setTheme(newTheme);
};

const toggleSearch = () => {
  showSearch.value = !showSearch.value;
  nextTick(() => {
    searchInput.value?.focus();
  });
};

const closeSearch = () => {
  showSearch.value = false;
  searchQuery.value = '';  
  searchStore.clearSearch();  // Make sure this is being called
};

const handleSearchClickOutside = (event) => {
  if (event.target === event.currentTarget) {
    closeSearch();
  }
};

const handleSearch = (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault();
    toggleSearch();
  } else if (event.key === 'Escape' && showSearch.value) {
    closeSearch();
  }
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showProfileMenu.value = false;
  }
  if (showSearch.value && searchRef.value && !searchRef.value.contains(event.target)) {
    showSearch.value = false;
  }
};

onMounted(() => {
  const handleScroll = () => {
    isScrolled.value = window.scrollY > 0;
  };
  window.addEventListener('scroll', handleScroll);
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('keydown', handleSearch);
  
  return () => {
    window.removeEventListener('scroll', handleScroll);
    document.removeEventListener('click', handleClickOutside);
    document.removeEventListener('keydown', handleSearch);
  };
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleSearch);
});

const handleLogout = () => {
  // Implement logout logic
  console.log('Logging out...');
};

watch(showSearch, (newValue) => {
  if (!newValue) {
    searchStore.clearSearch();
    searchQuery.value = '';
  }
});

defineProps({
  class: String // Define the class prop
});
</script>

<template>
  <div> <!-- Add root element -->
    <header 
      class="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-gray-900 transition-all duration-300 border-b border-neutral-300 dark:border-gray-800"
      :class="{ 'shadow-sm dark:shadow-none': isScrolled }"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-16">
          <!-- Logo and Navigation -->
          <div class="flex items-center gap-8">
            <!-- Logo -->
            <a href="https://www.qiyijiazhen.com" class="flex items-center gap-2" target="_blank">
              <img 
              src="/src/assets/logo.svg" 
              alt="FlowAgenda" 
              class="w-8 h-8"
              />
              <span class="text-xl sm:text-2xl font-bold bg-gradient-to-r from-neutral-600 to-neutral-400 dark:from-neutral-300 dark:to-neutral-500 bg-clip-text text-transparent">
              FlowAgenda
              </span>
            </a>

            <!-- Navigation -->
            <nav class="hidden md:flex items-center gap-1">
              <router-link
                v-for="item in navigationItems"
                :key="item.path"
                :to="item.path"
                class="px-4 py-2 rounded-lg text-neutral-600 dark:text-neutral-400 hover:text-accent-400 dark:hover:text-accent-300 hover:bg-accent-50 dark:hover:bg-accent-900/20 transition-colors flex items-center gap-2"
                :class="{ 
                  'bg-accent-50 text-accent-400 dark:bg-accent-900/20 dark:text-accent-300': 
                    $route.path === item.path 
                }"
              >
                <component :is="item.icon" class="w-4 h-4" />
                {{ item.name }}
              </router-link>
            </nav>
          </div>

          <!-- Right Actions -->
          <div class="flex items-center gap-2">
            <div ref="searchRef">
              <!-- Search -->
              <Tooltip content="Quick Search. Press ⌘ + k" position="bottom">
                <button 
                  @click="toggleSearch"
                  class="p-2 hover:bg-accent-50 dark:hover:bg-accent-900/20 rounded-lg text-neutral-600 dark:text-neutral-400 hover:text-accent-400 dark:hover:text-accent-300 transition-colors"
                >
                  <Search class="w-5 h-5" />
                </button>
              </Tooltip>
            </div>

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

            <!-- Profile Menu -->
            <div class="relative" ref="dropdownRef">
              <button 
                @click="showProfileMenu = !showProfileMenu"
                class="flex items-center gap-2 p-1 rounded-lg hover:bg-neutral-50 dark:hover:bg-gray-800 transition-colors"
              >
                <img 
                  src="https://ui-avatars.com/api/?name=Kiwi&background=random" 
                  alt="User avatar" 
                  class="w-8 h-8 rounded-full bg-neutral-300 dark:bg-gray-700"
                />
              </button>

              <!-- Dropdown Menu -->
              <div 
                v-if="showProfileMenu"
                class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-neutral-300 dark:border-gray-700 py-1"
              >
                <div class="px-4 py-2 border-b border-neutral-100 dark:border-gray-700">
                  <div class="font-medium text-neutral-900 dark:text-white">Kiwi</div>
                  <div class="text-sm text-neutral-500 dark:text-neutral-400">kiwi@example.com</div>
                </div>
                
                <div class="py-1">
                  <button 
                    @click="router.push('/settings')"
                    class="w-full px-4 py-2 text-sm text-left text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-gray-700 transition-colors flex items-center gap-2"
                  >
                    <Settings class="w-4 h-4" />
                    Settings
                  </button>
                  <button 
                    @click="handleLogout"
                    class="w-full px-4 py-2 text-sm text-left text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors flex items-center gap-2"
                  >
                    <LogOut class="w-4 h-4" />
                    Sign out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Search Modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-400 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-400 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="showSearch" 
          class="fixed inset-0 z-50 flex items-center justify-center"
          @click="handleSearchClickOutside"
        >
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/50 dark:bg-black/70 transition-opacity backdrop-blur-sm" />
          
          <!-- Search Modal -->
          <Transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="transition duration-300 ease-in"
            leave-from-class="opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div 
              class="relative bg-white dark:bg-gray-800 rounded-full shadow-xl w-full max-w-2xl mx-4 p-4"
              @click.stop
            >
              <div class="flex items-center gap-2">
                <Search class="w-5 h-5 text-gray-400 dark:text-gray-500" />
                <input
                  ref="searchInput"
                  type="text"
                  placeholder="Search..."
                  class="w-full p-2 bg-transparent focus:outline-none text-neutral-900 dark:text-white placeholder-neutral-400 dark:placeholder-gray-500"
                  @keydown.esc="closeSearch"
                  @input="handleSearchInput"
                />
              </div>
              <!-- Add search results -->
              <SearchResults
                v-if="searchQuery"
                :results="searchStore.searchResults"
                :is-loading="searchStore.isSearching"
                @select="handleResultSelect"
                class="absolute left-0 right-0 top-full"
              />
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div> <!-- Close root element -->
</template>

<style scoped>
.fixed {
  position: fixed;
}
.transform {
  transform-origin: top;
}
.transition {
  transition-property: all;
}
.backdrop-blur-sm {
  -webkit-backdrop-filter: blur(4px);
  backdrop-filter: blur(4px);
}
</style>