import { defineStore } from 'pinia'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'
import { useApiKeysStore } from './apiKeysStore'

export const useUiPreferencesStore = defineStore('uiPreferences', {
  state: () => ({
    // Theme settings
    theme: 'system', 
    isSaving: false,
    isSyncing: false,
    lastSyncedAt: null,
    
    // Language settings
    language: 'en',
    
    // Model settings
    modelSettings: {
      selectedModel: 'gpt4o',
      baseUrl: 'https://api.openai.com/v1',
      apiKeys: {
        openai: '',
        deepseek: '',
        claude: '',
        qwen: ''
      }
    },
    
    // Ollama settings
    ollamaSettings: {
      baseUrl: 'http://localhost:11434',
      selectedModel: 'qwen2',
      isConnected: false,
      availableModels: []
    }
  }),

  persist: {
    paths: ['theme', 'language', 'modelSettings', 'ollamaSettings', 'lastSyncedAt'],
    storage: localStorage
  },

  getters: {
    currentTheme: (state) => {
      if (state.theme === 'system') {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      }
      return state.theme
    },
    
    isApiKeySet: () => (provider) => {
      const apiKeysStore = useApiKeysStore()
      return apiKeysStore.hasKey(provider)
    },
    
    isOllamaConnected: (state) => state.ollamaSettings.isConnected,
    
    activeModel: (state) => state.modelSettings.selectedModel,
    
    activeLanguage: (state) => state.language
  },

  actions: {
    // Theme actions
    setTheme(theme) {
      this.theme = theme
      this.applyTheme()
      this.saveSettings()
    },

    applyTheme() {
      document.documentElement.classList.toggle('dark', this.currentTheme === 'dark')
    },

    // Language actions
    setLanguage(lang) {
      this.language = lang
      this.saveSettings()
    },

    // Model settings actions
    setModelSettings(settings) {
      this.modelSettings = {
        ...this.modelSettings,
        ...settings
      }
      this.saveSettings()
    },

    setApiKey(provider, key) {
      const apiKeysStore = useApiKeysStore()
      apiKeysStore.setKey(provider, key)
    },

    setSelectedModel(model) {
      this.modelSettings.selectedModel = model
      this.saveSettings()
    },

    // Ollama settings actions
    setOllamaSettings(settings) {
      this.ollamaSettings = {
        ...this.ollamaSettings,
        ...settings
      }
      this.saveSettings()
    },

    updateOllamaConnection(status) {
      this.ollamaSettings.isConnected = status
      this.saveSettings()
    },

    setOllamaModels(models) {
      this.ollamaSettings.availableModels = models
    },

    // API Integration
    async makeApiCall(provider, endpoint, data) {
      const apiKeysStore = useApiKeysStore()
      const apiKey = apiKeysStore.getKey(provider)
      
      if (!apiKey) {
        throw new Error(`No API key found for ${provider}`)
      }

      try {
        return await axios.post(endpoint, data, {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
          }
        })
      } catch (error) {
        if (error.response?.status === 401) {
          apiKeysStore.removeKey(provider)
          throw new Error(`Invalid ${provider} API key`)
        }
        throw error
      }
    },

    // Backend sync
    async fetchPreferences() {
      try {
        const response = await axios.get(API_ENDPOINTS.preferences.get)
        
        if (response.data?.success) {
          const preferences = response.data.data // Assuming standard API response format
          
          // Update non-sensitive settings
          this.theme = preferences.theme || this.theme
          this.language = preferences.language || this.language
          
          if (preferences.model_settings) {
            this.modelSettings = {
              ...this.modelSettings,
              selectedModel: preferences.model_settings.selectedModel || this.modelSettings.selectedModel,
              baseUrl: preferences.model_settings.baseUrl || this.modelSettings.baseUrl
            }
          }
          
          if (preferences.ollama_settings) {
            this.ollamaSettings = {
              ...this.ollamaSettings,
              baseUrl: preferences.ollama_settings.baseUrl || this.ollamaSettings.baseUrl,
              selectedModel: preferences.ollama_settings.selectedModel || this.ollamaSettings.selectedModel
            }
          }
          
          this.lastSyncedAt = new Date().toISOString()
          this.applyTheme()
        }
      } catch (error) {
        console.error('Failed to fetch preferences:', error)
        // Fall back to local storage values
      }
    },

    async saveSettings() {
      if (this.isSaving) return

      try {
        this.isSaving = true
        
        // Prepare data for backend
        const syncData = {
          theme: this.theme,
          language: this.language,
          model_settings: {
            selectedModel: this.modelSettings.selectedModel,
            baseUrl: this.modelSettings.baseUrl
          },
          ollama_settings: {
            baseUrl: this.ollamaSettings.baseUrl,
            selectedModel: this.ollamaSettings.selectedModel
          }
        }

        // Save to backend
        const response = await axios.patch(API_ENDPOINTS.preferences.update, syncData)
        
        if (response.data?.success) {
          // Update local storage
          this.$persist()
          this.lastSyncedAt = new Date().toISOString()
          return true
        } else {
          throw new Error(response.data?.error?.message || 'Failed to save preferences')
        }
      } catch (error) {
        console.error('Failed to save settings:', error)
        throw error
      } finally {
        this.isSaving = false
      }
    },

    async initializeSettings() {
      // Apply theme from local storage first
      this.applyTheme()
      
      // Fetch latest settings from backend
      await this.fetchPreferences()
    }
  }
})