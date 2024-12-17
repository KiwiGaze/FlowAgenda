// composables/useQuickActions.js
import { ref, computed } from 'vue'

export const useQuickActions = (initialText = '') => {
  const searchText = ref(initialText)
  const selectedIndex = ref(-1)

  // Simplified quick actions for ChatGPT-style interface
  const quickActions = [
    {
      id: 'team-meeting',
      category: 'Most used',
      label: 'Schedule a team meeting',
      icon: '👥',
      iconColor: 'text-blue-500',
      template: 'Schedule a team meeting next {day} at {time}'
    },
    {
      id: 'workshop',
      category: 'Most used',
      label: 'Create a workshop',
      icon: '💡',
      iconColor: 'text-amber-500',
      template: 'Organize a workshop for {day} afternoon'
    },
    {
      id: 'social',
      category: 'Trending',
      label: 'Plan social event',
      icon: '🎉',
      iconColor: 'text-purple-500',
      template: 'Plan a team social event for next {day}'
    },
    {
      id: 'lunch',
      category: 'Recent',
      label: 'Schedule lunch meeting',
      icon: '🍽️',
      iconColor: 'text-green-500',
      template: 'Schedule a lunch meeting for {day} at {time}'
    }
  ]

  // Simplified suggestion system
  const suggestions = computed(() => {
    if (!searchText.value) return quickActions

    const normalizedSearch = searchText.value.toLowerCase()
    return quickActions.filter(action => 
      action.label.toLowerCase().includes(normalizedSearch) ||
      action.category.toLowerCase().includes(normalizedSearch)
    )
  })

  // Smart template with simpler context
  const getSmartTemplate = (action) => {
    const now = new Date()
    const dayOfWeek = now.getDay()
    const hour = now.getHours()

    const defaultDay = dayOfWeek >= 5 ? 'next Monday' : 'tomorrow'
    const defaultTime = hour < 12 ? '10:00 AM' : '2:00 PM'

    return action.template
      .replace('{day}', defaultDay)
      .replace('{time}', defaultTime)
  }

  // Simplified key navigation
  const handleKeyNavigation = (e) => {
    const maxIndex = suggestions.value.length - 1

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        selectedIndex.value = selectedIndex.value === maxIndex ? -1 : selectedIndex.value + 1
        break
      case 'ArrowUp':
        e.preventDefault()
        selectedIndex.value = selectedIndex.value === -1 ? maxIndex : selectedIndex.value - 1
        break
      case 'Enter':
        if (selectedIndex.value >= -1) {
          e.preventDefault()
          const suggestion = selectedIndex.value === -1 
            ? suggestions.value[0] 
            : suggestions.value[selectedIndex.value]
          return getSmartTemplate(suggestion)
        }
        break
      case 'Escape':
        selectedIndex.value = -1
        break
    }
    return null
  }

  return {
    searchText,
    selectedIndex,
    suggestions,
    getSmartTemplate,
    handleKeyNavigation
  }
}