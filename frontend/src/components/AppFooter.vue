<!-- components/AppFooter.vue -->
<script setup>
import { ref, computed } from 'vue';
import { 
  Twitter, 
  Github, 
  Linkedin, 
  Heart,
  Sparkles,
  ChevronRight,
  ExternalLink,
  ArrowUpRight
} from 'lucide-vue-next';

const currentYear = computed(() => new Date().getFullYear());
const email = ref('');
const isSubscribing = ref(false);
const showSubscriptionSuccess = ref(false);

const footerLinks = {
  product: [
    { label: 'Features', href: '#'},
    { label: 'Pricing', href: '#' },
    { label: 'Integrations', href: '#', isNew: true },
    { label: 'Updates', href: '#', badge: 'Beta'}
  ],
  company: [
    { label: 'About', href: '#' },
    { label: 'Blog', href: '#' },
    { label: 'Careers', href: '#', badge: 'Hiring'},
    { label: 'Press', href: '#' }
  ],
  support: [
    { label: 'Help Center', href: '#' },
    { label: 'Documentation', href: '#' },
    { label: 'API Reference', href: '#', isExternal: true, badge: 'v2.0' },
    { label: 'Status', href: '#', statusDot: true, statusColor: 'bg-green-400' }
  ]
};

const socialLinks = [
  { 
    icon: Twitter, 
    href: '#', 
    label: 'Twitter',
    color: 'hover:text-blue-400 dark:hover:text-blue-300'
  },
  { 
    icon: Github, 
    href: '#', 
    label: 'GitHub',
    color: 'hover:text-gray-900 dark:hover:text-white'
  },
  { 
    icon: Linkedin, 
    href: '#', 
    label: 'LinkedIn',
    color: 'hover:text-blue-600 dark:hover:text-blue-300'
  },
];

const handleSubscribe = async () => {
  if (!email.value || isSubscribing.value) return;
  
  try {
    isSubscribing.value = true;
    await new Promise(resolve => setTimeout(resolve, 1000));
    showSubscriptionSuccess.value = true;
    email.value = '';
    
    setTimeout(() => {
      showSubscriptionSuccess.value = false;
    }, 3000);
  } finally {
    isSubscribing.value = false;
  }
};
</script>

<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-neutral-100 dark:border-gray-800">
    <div class="max-w-7xl mx-auto px-4 pb-8 sm:px-6 lg:px-8">
      <!-- Bottom Bar -->
      <div class="mt-8">
        <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div class="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
            <span>Made with</span>
            <Heart class="w-4 h-4 text-red-400 dark:text-red-300" />
            <span>by Qi Yijiazhen • © {{ currentYear }}</span>
          </div>
          <div class="flex items-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
            <a href="#" class="hover:text-accent-500 dark:hover:text-accent-400 transition-colors">Terms</a>
            <a href="#" class="hover:text-accent-500 dark:hover:text-accent-400 transition-colors">Privacy</a>
            <a href="#" class="hover:text-accent-500 dark:hover:text-accent-400 transition-colors">Cookies</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.link-hover-animation {
  @apply relative;
}

.link-hover-animation::after {
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-accent-400 dark:bg-accent-500 transition-all duration-300;
  content: '';
}

.link-hover-animation:hover::after {
  @apply w-full;
}

.newsletter-pattern {
  mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 50%, transparent);
}
</style>