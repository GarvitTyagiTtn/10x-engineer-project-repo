import { useState } from 'react';
import Button from '../shared/Button';
import styles from './CollectionForm.module.css';

export default function CollectionForm({ onSubmit, onCancel, saving }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) { setError('Name is required.'); return; }
    setError('');
    onSubmit({ name: name.trim(), description: description.trim() || undefined });
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      {error && <p className={styles.error} role="alert">{error}</p>}
      <div className={styles.field}>
        <label htmlFor="col-name">Name <span className={styles.required}>*</span></label>
        <input
          id="col-name"
          value={name}
          onChange={(e) => { setName(e.target.value); if (error) setError(''); }}
          className={error ? styles.inputError : undefined}
          aria-invalid={error ? 'true' : undefined}
        />
      </div>
      <div className={styles.field}>
        <label htmlFor="col-desc">Description</label>
        <textarea id="col-desc" rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div className={styles.actions}>
        <Button type="submit" disabled={saving}>{saving ? 'Creating...' : 'Create'}</Button>
        <Button variant="secondary" onClick={onCancel} disabled={saving}>Cancel</Button>
      </div>
    </form>
  );
}
