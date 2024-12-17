<!-- components/CollapsibleInfoCard.vue -->
<script setup>
import { ref, computed } from 'vue';
import { ChevronDown, Pencil, Check, X, Info } from 'lucide-vue-next';
import Tooltip from './Tooltip.vue';

const props = defineProps({
  icon: {
    type: [Object, Function], // Accept both Object and Function types
    required: true
  },
  title: {
    type: String,
    required: true
  },
  content: {
    type: [String, Array], // Accept both String and Array types
    required: true
  },
  hint: {
    type: String,
    default: ''
  },
  tooltip: {
    type: String,
    default: ''
  },
  tooltipPosition: {
    type: String,
    default: 'top'
  },
  initialExpanded: {
    type: Boolean,
    default: false
  }
});

const isExpanded = ref(props.initialExpanded);
const isEditing = ref(false);
const editedContent = ref(
  Array.isArray(props.content) ? props.content.join('\n') : props.content
);
const isHovered = ref(false);

const displayContent = computed(() => {
  if (!props.content) return '';
  if (typeof props.content === 'string') return props.content;
  if (Array.isArray(props.content)) return props.content.join('\n');
  return String(props.content);
});

const emit = defineEmits(['update:content']);

const toggleExpand = () => {
  if (!isEditing.value) {
    isExpanded.value = !isExpanded.value;
  }
};

const startEditing = (event) => {
  event.stopPropagation();
  editedContent.value = displayContent.value;
  isEditing.value = true;
  isExpanded.value = true;
};

const saveChanges = (event) => {
  event.stopPropagation();
  const newContent = Array.isArray(props.content)
    ? editedContent.value.split('\n')
    : editedContent.value;
  emit('update:content', newContent);
  isEditing.value = false;
};

const cancelEditing = (event) => {
  event.stopPropagation();
  editedContent.value = displayContent.value;
  isEditing.value = false;
};

</script>

<template>
  <div 
    class="bg-white dark:bg-neutral-800 rounded-lg shadow-sm border border-neutral-200 
          dark:border-neutral-700 overflow-hidden transition-all duration-200"
    :class="{ 
      'ring-1 ring-accent-400 ring-opacity-50': isEditing,
      'hover:border-neutral-300 dark:hover:border-neutral-600': !isEditing 
    }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- Header -->
    <div 
      @click="toggleExpand"
      class="p-4 flex items-center justify-between cursor-pointer transition-colors"
      :class="{ 'hover:bg-neutral-50 dark:hover:bg-neutral-700': !isEditing }"
    >
      <div class="flex items-center gap-3 flex-1 min-w-0">
        <!-- Icon -->
        <div 
          class="flex-shrink-0 p-2 rounded-lg transition-colors"
          :class="isExpanded 
            ? 'bg-accent-400' 
            : 'bg-accent-50 dark:bg-accent-400/20'"
        >
          <component 
            :is="icon" 
            class="w-5 h-5 transition-colors"
            :class="isExpanded 
              ? 'text-white' 
              : 'text-accent-400'"
          />
        </div>

        <!-- Title and Preview -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2">
            <h4 class="font-medium text-neutral-900 dark:text-neutral-100">
              {{ title }}
            </h4>
            <!-- Info Icon -->
            <div class="relative z-20">
              <Tooltip 
                v-if="tooltip"
                :content="tooltip"
                :position="tooltipPosition"
                :delay="300"
              >
                <button 
                  class="p-1 rounded-full hover:bg-neutral-100 dark:hover:bg-neutral-700 
                        transition-colors"
                  @click.stop
                >
                  <Info class="w-4 h-4 text-neutral-400 dark:text-neutral-500" />
                </button>
              </Tooltip>
            </div>
            <!-- Hint text -->
            <span 
              v-if="hint && isHovered && !isExpanded" 
              class="text-xs text-neutral-500 dark:text-neutral-400"
            >
              {{ hint }}
            </span>
          </div>
          <!-- Preview text with ellipsis -->
          <p 
            v-if="!isExpanded" 
            class="text-sm text-neutral-500 dark:text-neutral-400 truncate max-w-[calc(100%-4rem)]"
          >
            {{ displayContent }}
          </p>
        </div>
      </div>
      
      <!-- Actions -->
      <div class="flex items-center gap-2 flex-shrink-0">
        <Tooltip 
          v-if="!isEditing"
          content="Edit content"
          position="left"
          :delay="300"
        >
          <button 
            @click.stop="startEditing"
            class="p-1.5 text-neutral-400 dark:text-neutral-500 hover:text-accent-400 
                  dark:hover:text-accent-300 hover:bg-accent-50 dark:hover:bg-accent-400/20 
                  rounded-lg transition-all"
            :class="{ 'opacity-0': !isHovered, 'opacity-100': isHovered }"
          >
            <Pencil class="w-4 h-4" />
          </button>
        </Tooltip>

        <!-- Expand/Collapse Button -->
        <Tooltip 
          :content="isExpanded ? 'Collapse' : 'Expand'"
          position="left"
          :delay="300"
        >
          <ChevronDown 
            class="w-5 h-5 text-neutral-400 dark:text-neutral-500 transition-transform duration-200"
            :class="{ 'rotate-180': isExpanded }"
          />
        </Tooltip>
      </div>
    </div>
    
    <!-- Expanded Content -->
    <div 
      v-show="isExpanded"
      class="border-t border-neutral-100 dark:border-neutral-700"
    >
      <div class="p-4">
        <template v-if="isEditing">
          <textarea
            v-model="editedContent"
            class="w-full p-2 border border-neutral-200 dark:border-neutral-600 
                  bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 
                  rounded-lg focus:ring-2 focus:ring-accent-400 focus:border-transparent 
                  resize-y min-h-[6rem] transition-colors"
            :rows="Math.min(10, editedContent.split('\n').length + 1)"
            @keydown.esc="cancelEditing"
          ></textarea>
          
          <div class="flex justify-end items-center gap-2 mt-3">
            <Tooltip content="Cancel editing" position="top" :delay="300">
              <button
                @click="cancelEditing"
                class="flex items-center gap-2 px-3 py-1.5 text-neutral-600 dark:text-neutral-400 
                      hover:bg-neutral-50 dark:hover:bg-neutral-700 rounded-lg transition-colors"
              >
                <X class="w-4 h-4" />
                Cancel
              </button>
            </Tooltip>
            <Tooltip content="Save changes" position="top" :delay="300">
              <button
                @click="saveChanges"
                class="flex items-center gap-2 px-3 py-1.5 bg-accent-400 text-white 
                      rounded-lg hover:bg-accent-500 transition-colors"
              >
                <Check class="w-4 h-4" />
                Save
              </button>
            </Tooltip>
          </div>
        </template>
        <div 
          v-else 
          class="prose prose-neutral dark:prose-invert max-w-none"
        >
          <p class="text-neutral-700 dark:text-neutral-300 whitespace-pre-line break-words">
            {{ displayContent }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.prose {
  font-size: 0.9375rem;
  line-height: 1.6;
}

/* Add word-break for very long words */
.prose p {
  word-break: break-word;
  hyphens: auto;
}
</style>