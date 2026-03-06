import { get, post, del } from './client.js';

export function getCollections() {
  return get('/collections');
}

export function getCollection(id) {
  return get(`/collections/${id}`);
}

export function createCollection(data) {
  return post('/collections', data);
}

export function deleteCollection(id) {
  return del(`/collections/${id}`);
}
