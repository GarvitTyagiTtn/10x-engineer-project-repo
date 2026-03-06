import Button from '../shared/Button';
import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './CollectionList.module.css';

export default function CollectionList({ collections, onSelect, onDelete, loading, error }) {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!collections.length) return <p className={styles.empty}>No collections yet.</p>;

  const handleDelete = (id) => {
    if (window.confirm('Delete this collection?')) onDelete(id);
  };

  return (
    <ul className={styles.list}>
      {collections.map((c) => (
        <li key={c.id} className={styles.item}>
          <button className={styles.info} onClick={() => onSelect(c.id)} type="button">
            <span className={styles.name}>{c.name}</span>
            {c.description && <span className={styles.desc}>{c.description}</span>}
          </button>
          <Button variant="danger" size="sm" onClick={() => handleDelete(c.id)}>Delete</Button>
        </li>
      ))}
    </ul>
  );
}
