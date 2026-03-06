import { useState } from 'react';
import LoadingSpinner from '../shared/LoadingSpinner';
import styles from './Sidebar.module.css';

export default function Sidebar({ collections, activeCollectionId, onSelectCollection, onNewCollection, onDeleteCollection, loading }) {
  const [collectionsOpen, setCollectionsOpen] = useState(true);

  const handleDelete = (e, id) => {
    e.stopPropagation();
    if (window.confirm('Delete this collection? Prompts in it will be unlinked.')) {
      onDeleteCollection(id);
    }
  };

  const handleNewClick = (e) => {
    e.stopPropagation();
    onNewCollection();
  };

  return (
    <nav className={styles.sidebar} aria-label="Navigation">
      <ul className={styles.list}>
        {/* Collections - collapsible section */}
        <li>
          <button
            className={styles.sectionHeader}
            onClick={() => setCollectionsOpen((v) => !v)}
            aria-expanded={collectionsOpen}
          >
            <span className={styles.sectionLeft}>
              <span className={`${styles.chevron} ${collectionsOpen ? styles.chevronOpen : ''}`}>›</span>
              <span>Collections</span>
            </span>
            <span
              className={styles.addBtn}
              role="button"
              tabIndex={0}
              aria-label="New collection"
              onClick={handleNewClick}
              onKeyDown={(e) => { if (e.key === 'Enter') handleNewClick(e); }}
            >
              +
            </span>
          </button>

          {collectionsOpen && (
            loading ? <LoadingSpinner /> : (
              <ul className={styles.subList}>
                {collections.length === 0 && (
                  <li className={styles.emptyMsg}>No collections yet</li>
                )}
                {collections.map((c) => (
                  <li key={c.id}>
                    <button
                      className={`${styles.subItem} ${activeCollectionId === c.id ? styles.active : ''}`}
                      onClick={() => onSelectCollection(c.id)}
                      aria-current={activeCollectionId === c.id ? 'true' : undefined}
                    >
                      <span className={styles.itemName}>{c.name}</span>
                      <span
                        className={styles.deleteBtn}
                        role="button"
                        tabIndex={0}
                        aria-label={`Delete ${c.name}`}
                        onClick={(e) => handleDelete(e, c.id)}
                        onKeyDown={(e) => { if (e.key === 'Enter') handleDelete(e, c.id); }}
                      >
                        ×
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            )
          )}
        </li>

        {/* Prompts - below collections, same level */}
        <li>
          <button
            className={`${styles.sectionHeader} ${activeCollectionId === null ? styles.activeSection : ''}`}
            onClick={() => onSelectCollection(null)}
            aria-current={activeCollectionId === null ? 'true' : undefined}
          >
            <span className={styles.sectionLeft}>
              <span>Prompts</span>
            </span>
          </button>
        </li>
      </ul>
    </nav>
  );
}
