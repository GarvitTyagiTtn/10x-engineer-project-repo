import Button from '../shared/Button';
import styles from './PromptDetail.module.css';

export default function PromptDetail({ prompt, collectionName, onEdit, onDelete, onBack }) {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${prompt.title}"? This cannot be undone.`)) {
      onDelete();
    }
  };

  return (
    <article className={styles.detail}>
      <div className={styles.header}>
        <h1 className={styles.title}>{prompt.title}</h1>
        <div className={styles.actions}>
          <Button variant="secondary" size="sm" onClick={onBack}>Back</Button>
          <Button size="sm" onClick={onEdit}>Edit</Button>
          <Button variant="danger" size="sm" onClick={handleDelete}>Delete</Button>
        </div>
      </div>
      <div className={styles.meta}>
        {collectionName && <span className={styles.badge}>{collectionName}</span>}
        <time dateTime={prompt.created_at}>Created {new Date(prompt.created_at).toLocaleDateString()}</time>
        {prompt.updated_at && (
          <time dateTime={prompt.updated_at}>Updated {new Date(prompt.updated_at).toLocaleDateString()}</time>
        )}
      </div>
      <div className={styles.contentBlock}>
        <h2 className={styles.sectionLabel}>Prompt Content</h2>
        <div className={styles.content}>{prompt.content}</div>
      </div>
      {prompt.description && (
        <div className={styles.descBlock}>
          <h2 className={styles.sectionLabel}>Description</h2>
          <p className={styles.description}>{prompt.description}</p>
        </div>
      )}
    </article>
  );
}
