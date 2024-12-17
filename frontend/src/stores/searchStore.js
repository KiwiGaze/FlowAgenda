// src/stores/searchStore.js
import { defineStore } from 'pinia';
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';

/**
 * @typedef {Object} SearchResult
 * @property {string} id - Format: 'event_uuid' or 'attendee_uuid'
 * @property {'event' | 'attendee'} type
 * @property {string} title
 * @property {string} url
 * @property {string} snippet
 */

/**
 * @typedef {Object} SearchResponse
 * @property {boolean} success
 * @property {SearchResult[]} data
 * @property {{message: string, status_code: number}} [error]
 */

export const useSearchStore = defineStore('search', {
  state: () => ({
    /** @type {string} */
    searchQuery: '',
    
    /** @type {SearchResult[]} */
    searchResults: [],
    
    /** @type {boolean} */
    isSearching: false,
    
    /** @type {string | null} */
    error: null,
    
    /** @type {number | null} */
    debounceTimeout: null,

    /** @type {number} */
    debounceDelay: 300
  }),

  actions: {
    /**
     * Perform search with debouncing.
     * @param {string} query - Search query.
     */
    async search(query) {
      // Clear existing timeout
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
      }

      // Update query state
      this.searchQuery = query;

      this.debounceTimeout = setTimeout(async () => {
        this.isSearching = true;
        this.error = null;
        
        try {
          const response = await axios.get(API_ENDPOINTS.search, {
            params: { q: query },
            headers: {
              'Accept': 'application/json'
            }
          });

          // Handle successful response (including empty results)
          if (response.data?.success) {
            this.searchResults = this.processSearchResults(response.data.data || []);
          } else {
            this.searchResults = [];
            this.error = response.data.error?.message || 'Failed to perform search';
          }

        } catch (error) {
          this.handleSearchError(error);
        } finally {
          this.isSearching = false;
        }
      }, this.debounceDelay);
    },

    /**
     * Clear search state.
     */
    clearSearch() {
      this.searchQuery = '';
      this.searchResults = [];
      this.error = null;
      this.isSearching = false;
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
        this.debounceTimeout = null;
      }
    },

    /**
     * Process and validate search results.
     * @param {SearchResult[]} results - Raw search results from backend.
     * @returns {SearchResult[]} - Processed and validated search results.
     */
    processSearchResults(results) {
      return results
        .filter(this.isValidResult)
        .map(result => ({
          ...result,
          url: this.processUrl(result.url)
        }));
    },

    /**
     * Handle search error based on backend error responses.
     * @param {Error} error - The error thrown during the search request.
     */
    handleSearchError(error) {
      if (error.response?.data?.error) {
        // Handle structured error from backend
        this.error = error.response.data.error.message;
      } else if (error.response?.status === 400) {
        // Handle validation errors
        this.error = 'Invalid search query';
      } else if (error.response?.status === 500) {
        // Handle server errors
        this.error = 'Server error occurred while searching';
      } else {
        // Handle other errors
        console.error('Search error:', error);
        this.error = 'Failed to perform search';
      }
      this.searchResults = [];
    },

    /**
     * Process URL to ensure full path.
     * @param {string} url - The URL to process.
     * @returns {string} - The processed full URL.
     */
    processUrl(url) {
      if (url.startsWith('http')) {
        return url;
      }
      return `${window.location.origin}${url}`;
    }
  },

  getters: {
    /**
     * Check if search has any results.
     */
    hasResults: (state) => state.searchResults.length > 0,

    /**
     * Check if search has no results but completed successfully.
     */
    hasNoResults: (state) => 
      !state.isSearching && 
      state.searchResults.length === 0 && 
      !state.error,

    /**
     * Group results by type.
     */
    groupedResults: (state) => {
      return state.searchResults.reduce((groups, result) => {
        const type = result.type;
        if (!groups[type]) {
          groups[type] = [];
        }
        groups[type].push(result);
        return groups;
      }, {});
    },

    /**
     * Get events only.
     */
    eventResults: (state) => 
      state.searchResults.filter(result => result.type === 'event'),

    /**
     * Get attendees only.
     */
    attendeeResults: (state) => 
      state.searchResults.filter(result => result.type === 'attendee'),

    /**
     * Check if currently searching.
     */
    isLoading: (state) => state.isSearching,

    /**
     * Check if has error.
     */
    hasError: (state) => !!state.error,

    /**
     * Get total results count.
     */
    totalResults: (state) => state.searchResults.length,

    /**
     * Check if has active search query.
     */
    hasActiveSearch: (state) => !!state.searchQuery.trim(),

    /**
     * Validate search result object.
     */
    isValidResult: () => (result) => {
      return (
        result &&
        typeof result === 'object' &&
        typeof result.id === 'string' &&
        (result.type === 'event' || result.type === 'attendee') &&
        typeof result.title === 'string' &&
        typeof result.url === 'string' &&
        typeof result.snippet === 'string'
      );
    }
  }
});
