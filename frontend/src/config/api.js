// src/config/api.js
const API_BASE_URL = 'http://127.0.0.1:8000/api';// This is the base URL for the API defined in the Django project
const API_VERSION = 'v1';

export const API_ENDPOINTS = {
    events: {
        list: `${API_BASE_URL}/${API_VERSION}/events/`,
        detail: (id) => `${API_BASE_URL}/${API_VERSION}/events/${id}/`,
        status: (id) => `${API_BASE_URL}/${API_VERSION}/events/${id}/status/`,
        addNote: (id) => `${API_BASE_URL}/${API_VERSION}/events/${id}/add_note/`,
        addAttendee: (id) => `${API_BASE_URL}/${API_VERSION}/events/${id}/add_attendee/`,
        downloadIcs: (id) => `${API_BASE_URL}/${API_VERSION}/events/${id}/download_ics/`,
    },
    groups: {
        list: `${API_BASE_URL}/${API_VERSION}/groups/`,
        detail: (id) => `${API_BASE_URL}/${API_VERSION}/groups/${id}/`,
        createFromText: `${API_BASE_URL}/${API_VERSION}/groups/create-from-text/`,
        status: (id) => `${API_BASE_URL}/${API_VERSION}/groups/${id}/status/`
    },
    llmConfig: `${API_BASE_URL}/${API_VERSION}/llm-config/`,
    search: `${API_BASE_URL}/${API_VERSION}/search/`,
    ollama: {
        status: `${API_BASE_URL}/${API_VERSION}/ollama/status/`,
        models: `${API_BASE_URL}/${API_VERSION}/ollama/models/`,
    },
    preferences: {
        base: `${API_BASE_URL}/${API_VERSION}/preferences`,
        get: `${API_BASE_URL}/${API_VERSION}/preferences/`,
        update: `${API_BASE_URL}/${API_VERSION}/preferences/`,
        sync: `${API_BASE_URL}/${API_VERSION}/preferences/sync/`
    },
};