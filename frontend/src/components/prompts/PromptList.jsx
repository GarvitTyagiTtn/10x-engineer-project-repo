import PromptCard from './PromptCard';
import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './PromptList.module.css';

export default function PromptList({ prompts, onSelectPrompt, collections, loading, error, onRetry, emptyMessage }) {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={onRetry} />;
  if (!prompts.length) {
    return (
      <div className={styles.emptyState}>
        <span className={styles.emptyIcon} aria-hidden="true">📝</span>
        <p className={styles.emptyText}>{emptyMessage || 'No prompts yet. Create your first prompt!'}</p>
      </div>
    );
  }

  const collectionMap = Object.fromEntries((collections || []).map((c) => [c.id, c.name]));

  return (
    <div className={styles.grid} role="list" aria-label="Prompts">
      {prompts.map((p) => (
        <PromptCard
          key={p.id}
          prompt={p}
          onClick={() => onSelectPrompt(p.id)}
          collectionName={collectionMap[p.collection_id]}
        />
      ))}
    </div>
  );
}
