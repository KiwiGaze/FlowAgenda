//components/toast/ToastService.js
import { ref } from 'vue';

const toasts = ref([]);
let toastId = 0;

export const ToastService = {
  show(message, type = 'info', duration = 3000) {
    const id = ++toastId;
    toasts.value.push({ id, message, type, duration });
    return id;
  },

  success(message, duration) {
    return this.show(message, 'success', duration);
  },

  error(message, duration) {
    return this.show(message, 'error', duration);
  },

  warning(message, duration) {
    return this.show(message, 'warning', duration);
  },

  info(message, duration) {
    return this.show(message, 'info', duration);
  },

  remove(id) {
    const index = toasts.value.findIndex(toast => toast.id === id);
    if (index !== -1) {
      toasts.value.splice(index, 1);
    }
  },

  clear() {
    toasts.value = [];
  },

  getToasts() {
    return toasts;
  }
};