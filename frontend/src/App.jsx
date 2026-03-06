import { useState, useEffect, useCallback } from 'react';
import { getPrompts, getPrompt, createPrompt, updatePrompt, deletePrompt } from './api/prompts';
import { getCollections, createCollection, deleteCollection } from './api/collections';
import Layout from './components/layout/Layout';
import Sidebar from './components/layout/Sidebar';
import SearchBar from './components/shared/SearchBar';
import Modal from './components/shared/Modal';
import PromptList from './components/prompts/PromptList';
import PromptDetail from './components/prompts/PromptDetail';
import PromptForm from './components/prompts/PromptForm';
import CollectionForm from './components/collections/CollectionForm';
import styles from './App.module.css';

export default function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [promptsLoading, setPromptsLoading] = useState(true);
  const [promptsError, setPromptsError] = useState(null);
  const [collectionsLoading, setCollectionsLoading] = useState(true);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [activeCollectionId, setActiveCollectionId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [view, setView] = useState('list');
  const [showCollectionForm, setShowCollectionForm] = useState(false);
  const [saving, setSaving] = useState(false);

  const fetchPrompts = useCallback(async () => {
    setPromptsLoading(true);
    setPromptsError(null);
    try {
      const params = {};
      if (activeCollectionId) params.collection_id = activeCollectionId;
      if (searchQuery) params.search = searchQuery;
      const data = await getPrompts(params);
      setPrompts(data.prompts);
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setPromptsLoading(false);
    }
  }, [activeCollectionId, searchQuery]);

  const fetchCollections = useCallback(async () => {
    setCollectionsLoading(true);
    try {
      const data = await getCollections();
      setCollections(data.collections);
    } catch {
      /* sidebar will just be empty */
    } finally {
      setCollectionsLoading(false);
    }
  }, []);

  useEffect(() => { fetchCollections(); }, [fetchCollections]);
  useEffect(() => { fetchPrompts(); }, [fetchPrompts]);

  const handleSelectPrompt = async (id) => {
    try {
      const data = await getPrompt(id);
      setSelectedPrompt(data);
      setView('detail');
    } catch (err) {
      setPromptsError(err.message);
    }
  };

  const handleCreatePrompt = async (formData) => {
    setSaving(true);
    try {
      await createPrompt(formData);
      setView('list');
      fetchPrompts();
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleUpdatePrompt = async (formData) => {
    setSaving(true);
    try {
      await updatePrompt(selectedPrompt.id, formData);
      setView('list');
      setSelectedPrompt(null);
      fetchPrompts();
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeletePrompt = async () => {
    try {
      await deletePrompt(selectedPrompt.id);
      setView('list');
      setSelectedPrompt(null);
      fetchPrompts();
    } catch (err) {
      setPromptsError(err.message);
    }
  };

  const handleCreateCollection = async (formData) => {
    setSaving(true);
    try {
      await createCollection(formData);
      setShowCollectionForm(false);
      fetchCollections();
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteCollection = async (id) => {
    try {
      await deleteCollection(id);
      if (activeCollectionId === id) setActiveCollectionId(null);
      fetchCollections();
      fetchPrompts();
    } catch (err) {
      setPromptsError(err.message);
    }
  };

  const collectionName = (id) => collections.find((c) => c.id === id)?.name;
  const activeCollectionName = activeCollectionId ? collectionName(activeCollectionId) : null;

  const sidebar = (
    <Sidebar
      collections={collections}
      activeCollectionId={activeCollectionId}
      onSelectCollection={(id) => { setActiveCollectionId(id); setView('list'); setSelectedPrompt(null); }}
      onNewCollection={() => setShowCollectionForm(true)}
      onDeleteCollection={handleDeleteCollection}
      loading={collectionsLoading}
    />
  );

  return (
    <Layout sidebar={sidebar} onNewPrompt={() => { setSelectedPrompt(null); setView('create'); }}>
      {view === 'list' && (
        <>
          <div className={styles.searchRow}>
            <SearchBar value={searchQuery} onChange={setSearchQuery} />
          </div>
          <PromptList
            prompts={prompts}
            collections={collections}
            onSelectPrompt={handleSelectPrompt}
            loading={promptsLoading}
            error={promptsError}
            onRetry={fetchPrompts}
            emptyMessage={
              activeCollectionName
                ? `No prompts in "${activeCollectionName}" yet.`
                : searchQuery
                  ? `No prompts matching "${searchQuery}".`
                  : 'No prompts yet. Create your first prompt!'
            }
          />
        </>
      )}
      {view === 'detail' && selectedPrompt && (
        <PromptDetail
          prompt={selectedPrompt}
          collectionName={collectionName(selectedPrompt.collection_id)}
          onEdit={() => setView('edit')}
          onDelete={handleDeletePrompt}
          onBack={() => { setView('list'); setSelectedPrompt(null); }}
        />
      )}
      {view === 'create' && (
        <PromptForm
          collections={collections}
          onSubmit={handleCreatePrompt}
          onCancel={() => setView('list')}
          saving={saving}
        />
      )}
      {view === 'edit' && selectedPrompt && (
        <PromptForm
          prompt={selectedPrompt}
          collections={collections}
          onSubmit={handleUpdatePrompt}
          onCancel={() => setView('detail')}
          saving={saving}
        />
      )}
      <Modal isOpen={showCollectionForm} onClose={() => setShowCollectionForm(false)} title="New Collection">
        <CollectionForm
          onSubmit={handleCreateCollection}
          onCancel={() => setShowCollectionForm(false)}
          saving={saving}
        />
      </Modal>
    </Layout>
  );
}
