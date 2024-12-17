// src/stores/apiKeysStore.js
import { defineStore } from 'pinia'

export const useApiKeysStore = defineStore('apiKeys', {
  state: () => ({
    keys: {
      openai: '',
      deepseek: '',
      claude: '',
      qwen: ''
    },
    lastUsed: {} // Track when each key was last used
  }),

  persist: {
    // Store ONLY in localStorage
    storage: localStorage,
    paths: ['keys', 'lastUsed'],
  },

  getters: {
    hasKey: (state) => (provider) => {
      return !!state.keys[provider]
    },

    getKey: (state) => (provider) => {
      if (state.keys[provider]) {
        // Update last used timestamp
        state.lastUsed[provider] = new Date().toISOString()
        return state.keys[provider]
      }
      return null
    },

    activeProviders: (state) => {
      return Object.entries(state.keys)
        .filter(([_, value]) => !!value)
        .map(([key]) => key)
    }
  },

  actions: {
    setKey(provider, key) {
      if (!key) {
        return false
      }

      // Basic key format validation
      const validations = {
        openai: (k) => k.startsWith('sk-'),
        deepseek: (k) => k.startsWith('dsk-'),
        claude: (k) => k.startsWith('sk-'),
        qwen: (k) => k.startsWith('qwk-')
      }

      if (validations[provider] && !validations[provider](key)) {
        throw new Error(`Invalid ${provider} API key format`)
      }

      this.keys[provider] = key
      this.lastUsed[provider] = new Date().toISOString()
      return true
    },

    removeKey(provider) {
      if (this.keys[provider]) {
        this.keys[provider] = ''
        delete this.lastUsed[provider]
        return true
      }
      return false
    },

    clearAllKeys() {
      this.keys = Object.fromEntries(
        Object.keys(this.keys).map(key => [key, ''])
      )
      this.lastUsed = {}
    }
  }
})