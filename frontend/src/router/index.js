// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import InputView from '../views/InputView.vue';
import ResultsView from '../views/ResultsView.vue';
import HistoryView from '../views/HistoryView.vue';
import LinkAccountView from '../views/LinkAccountView.vue';
import SettingsPage from '../views/SettingsPage.vue';
import EventsGroupView from '../views/EventsGroupView.vue';

const routes = [
  {
    path: '/',
    redirect: '/chat',
  },
  {
    path: '/chat',
    name: 'input',
    component: InputView
  },
  {
    path: '/events/:id',
    name: 'events',
    component: ResultsView,
    props: true
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView,
  },
  {
    path: '/accounts',
    name: 'accounts',
    component: LinkAccountView
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsPage,
  },
  {
    path: '/groups/:id',
    name: 'events-group',
    component: EventsGroupView,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;