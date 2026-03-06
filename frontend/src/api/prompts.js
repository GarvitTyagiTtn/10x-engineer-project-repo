import { get, post, put, patch, del } from './client.js';

export function getPrompts(params = {}) {
  const query = new URLSearchParams();
  if (params.collection_id) query.set('collection_id', params.collection_id);
  if (params.search) query.set('search', params.search);
  const qs = query.toString();
  return get(`/prompts${qs ? `?${qs}` : ''}`);
}

export function getPrompt(id) {
  return get(`/prompts/${id}`);
}

export function createPrompt(data) {
  return post('/prompts', data);
}

export function updatePrompt(id, data) {
  return put(`/prompts/${id}`, data);
}

export function patchPrompt(id, data) {
  return patch(`/prompts/${id}`, data);
}

export function deletePrompt(id) {
  return del(`/prompts/${id}`);
}
