<!-- views/HistoryView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue';
import { 
  Calendar,
} from 'lucide-vue-next';
import TimelineGroup from '../components/history/TimelineGroup.vue';
import HistoryFilter from '../components/history/HistoryFilter.vue';
import HistorySearch from '../components/history/HistorySearch.vue';
import EmptyState from '../components/history/EmptyState.vue';
import { API_ENDPOINTS } from '../config/api';
import { ToastService } from '../components/toast';
import PaginationControls from '@/components/common/PaginationControls.vue';
import { downloadFile } from '../utils/downloadUtils';

// State
const isLoading = ref(true);
const groups = ref([]);
const selectedFilter = ref('all');
const searchQuery = ref('');
const showFilters = ref(false);
const sortOrder = ref('created_at_desc'); // Default sort
const currentPage = ref(1);
const totalPages = ref(1);
const pageSize = ref(20);
const totalItems = ref(0);

const handleDownload = async (event) => {
  try {
    const filename = `${event.title.toLowerCase().replace(/\s+/g, '_')}.ics`;
    const downloadUrl = API_ENDPOINTS.events.downloadIcs(event.id);
    
    await downloadFile(downloadUrl, filename);
    
    emit('download', { success: true });
  } catch (error) {
    console.error('Failed to download event:', error);
    emit('download', { success: false, error });
  }
};

// Filter counts
const filterCounts = computed(() => {
  if (!groups.value) return {
    all: 0,
    completed: 0,
    processing: 0,
    error: 0,
    meetings: 0,
    presentations: 0,
    reviews: 0
  };

  const counts = {
    all: groups.value.length,
    completed: 0,
    processing: 0,
    error: 0,
    meetings: 0,
    presentations: 0,
    reviews: 0
  };

  groups.value.forEach(group => {
    // Count processing statuses
    if (group.processing_error) counts.error++;
    else if (!group.processing_complete) counts.processing++;
    else counts.completed++;

    // Count event types in the group
    if (group.events) {
      group.events.forEach(event => {
        const title = event.title.toLowerCase();
        if (title.includes('meeting')) counts.meetings++;
        if (title.includes('presentation')) counts.presentations++;
        if (title.includes('review')) counts.reviews++;
      });
    }
  });

  return counts;
});

// Fetch groups with error handling
const fetchGroups = async () => {
  try {
    isLoading.value = true;
    
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      page_size: pageSize.value.toString()
    });

    // Safely add sort parameters
    if (sortOrder.value) {
      const [field, direction] = sortOrder.value.split('_');
      params.append('sort', field);
      params.append('order', direction || 'desc');
    } else {
      // Default sort if no sort order is set
      params.append('sort', 'created_at');
      params.append('order', 'desc');
    }

    // Add search parameter
    if (searchQuery.value) {
      params.append('search', searchQuery.value);
    }

    // Add filter parameter
    if (selectedFilter.value !== 'all') {
      if (['completed', 'processing', 'error'].includes(selectedFilter.value)) {
        params.append('status', selectedFilter.value);
      } else if (['meetings', 'presentations', 'reviews'].includes(selectedFilter.value)) {
        params.append('event_type', selectedFilter.value);
      }
    }

    const response = await fetch(
      `${API_ENDPOINTS.groups.list}?${params.toString()}`,
      {
        headers: {
          'Accept': 'application/json',
        }
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || 'Failed to fetch groups');
    }

    const data = await response.json();
    totalItems.value = data.count;
    totalPages.value = Math.ceil(data.count / pageSize.value);
    groups.value = data.results || [];

  } catch (error) {
    console.error('Error fetching groups:', error);
    ToastService.error(error.message || 'Failed to load events');
    groups.value = [];
  } finally {
    isLoading.value = false;
  }
};

// Computed property for filtered groups
const filteredGroups = computed(() => {
  if (!groups.value || groups.value.length === 0) return [];
  return groups.value;
});

// Handle search
const handleSearch = async (query) => {
  searchQuery.value = query;
  currentPage.value = 1;
  await fetchGroups();
};

// Handle filter change
const handleFilterChange = async (filter) => {
  selectedFilter.value = filter;
  currentPage.value = 1;
  await fetchGroups();
};

// Handle page change
const handlePageChange = async (page) => {
  currentPage.value = page;
  await fetchGroups();
};

// Handle event deletion
const handleEventDelete = async (eventId) => {
  try {
    const response = await fetch(`${API_ENDPOINTS.events.detail(eventId)}`, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error('Failed to delete event');
    }

    // Remove the event from the group
    groups.value = groups.value.map(group => ({
      ...group,
      events: (group.events || []).filter(e => e.id !== eventId)
    })).filter(group => group.events && group.events.length > 0);

    ToastService.success('Event deleted successfully');
  } catch (error) {
    console.error('Error deleting event:', error);
    ToastService.error(error.message || 'Failed to delete event');
  }
};

// Handle event export
const handleEventExport = async (eventId) => {
  ToastService.info('Export functionality coming soon');
};

onMounted(() => {
  fetchGroups();
});
</script>

<template>
  <div class="history-view">
    <div class="min-h-screen bg-primary-50 dark:bg-primary-900 transition-colors duration-300">
      <div class="max-w-5xl mx-auto px-4 py-8">
        <!-- Header -->
        <div class="space-y-6">
          <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold text-primary-500 dark:text-primary-100 flex items-center gap-2">
              <Calendar class="w-6 h-6" />
              Event History
            </h1>
          </div>

          <!-- Search and Filters -->
          <div class="space-y-4">
            <HistorySearch 
              v-model="searchQuery"
              @search="handleSearch"
            />
            
            <HistoryFilter
              v-if="showFilters"
              v-model="selectedFilter"
              :counts="filterCounts"
              @change="handleFilterChange"
            />
          </div>
        </div>

        <!-- Content -->
        <div class="mt-8">
          <!-- Loading State -->
          <div v-if="isLoading" class="space-y-6">
            <div 
              v-for="i in 3" 
              :key="i"
              class="animate-pulse"
            >
              <div class="h-6 w-32 bg-neutral-200 dark:bg-primary-700 rounded mb-4" />
              <div class="space-y-4">
                <div 
                  v-for="j in 2" 
                  :key="j"
                  class="bg-white dark:bg-primary-800 p-6 rounded-lg"
                >
                  <div class="h-4 w-3/4 bg-neutral-200 dark:bg-primary-700 rounded mb-3" />
                  <div class="h-4 w-1/2 bg-neutral-200 dark:bg-primary-700 rounded" />
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <EmptyState 
            v-else-if="!filteredGroups.length"
            :is-filtering="searchQuery.length > 0 || selectedFilter !== 'all'"
            @clear-filters="searchQuery = ''; selectedFilter = 'all'; fetchGroups();"
          />

          <!-- Groups Timeline -->
          <div v-else class="space-y-8">
            <TimelineGroup
              v-for="group in filteredGroups"
              :key="group.id"
              :group="group"
              @delete="handleEventDelete"
              @download="handleDownload"
            />
          </div>

          <!-- Pagination -->
          <PaginationControls
            v-if="!isLoading && filteredGroups.length > 0"
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="handlePageChange"
            class="mt-8"
          />
        </div>
      </div>
    </div>
  </div>
</template>