// stores/eventsGroupStore.js
import { defineStore } from 'pinia';
import { API_ENDPOINTS } from '../config/api';

export const useEventsGroupStore = defineStore('eventsGroup', {
  state: () => ({
    currentGroup: null,
    isLoading: false,
    isProcessing: false,
    error: null,
    processingStatus: {
      complete: false,
      error: null
    }
  }),

  getters: {
    hasError: (state) => !!state.error || !!state.processingStatus.error,
    errorMessage: (state) => state.error || state.processingStatus.error || 'An error occurred',
    showLoader: (state) => state.isLoading || state.isProcessing
  },

  actions: {
    setProcessing(value) {
      this.isProcessing = value;
    },

    isProcessingOrLoading: (state) => state.isLoading || state.isProcessing || 
      (state.currentGroup && !state.currentGroup.processing_complete),

    async createFromText(text, useLLM = true) {
      this.isLoading = true;
      this.error = null;
      this.isProcessing = true; // Set processing state

      try {
        const response = await fetch(API_ENDPOINTS.groups.createFromText, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ text, use_llm: useLLM })
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error?.message || 'Failed to create events');
        }

        if (!data.success) {
          throw new Error(data.error?.message || 'Failed to process events');
        }

        this.currentGroup = data.data.group;
        // Keep processing state true until complete
        this.isProcessing = !data.data.group.processing_complete;
        this.processingStatus = {
          complete: data.data.group.processing_complete,
          error: data.data.group.processing_error
        };

        return data.data;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    async fetchGroupDetails(groupId) {
      if (!groupId) return;

      // Don't set loading if we're already processing
      if (!this.isProcessing) {
        this.isLoading = true;
      }

      try {
        const response = await fetch(API_ENDPOINTS.groups.detail(groupId), {
          headers: {
            'Accept': 'application/json'
          }
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error?.message || 'Failed to fetch group details');
        }

        this.currentGroup = data.data;
        
        // Update processing status
        this.isProcessing = !data.data.processing_complete;
        this.processingStatus = {
          complete: data.data.processing_complete,
          error: data.data.processing_error
        };

        return data.data;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    clearCurrentGroup() {
      this.currentGroup = null;
      this.error = null;
      this.isLoading = false;
      this.isProcessing = false;
      this.processingStatus = {
        complete: false,
        error: null
      };
    },

    async deleteEvent(eventId) {
      try {
        // Call API to delete event
        const response = await fetch(API_ENDPOINTS.events.detail(eventId), {
          method: 'DELETE',
          headers: {
            'Accept': 'application/json',
          }
        });
  
        if (!response.ok) {
          throw new Error('Failed to delete event');
        }
  
        // Update local state by removing the deleted event
        if (this.currentGroup && this.currentGroup.events) {
          this.currentGroup.events = this.currentGroup.events.filter(
            event => event.id !== eventId
          );
        }
  
        return true;
      } catch (error) {
        console.error('Error deleting event:', error);
        throw error;
      }
    }
  },
});