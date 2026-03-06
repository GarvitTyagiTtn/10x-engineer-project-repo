import { useState } from 'react';
import Button from '../shared/Button';
import styles from './PromptForm.module.css';

export default function PromptForm({ prompt, collections, onSubmit, onCancel, saving }) {
  const [form, setForm] = useState({
    title: prompt?.title || '',
    content: prompt?.content || '',
    description: prompt?.description || '',
    collection_id: prompt?.collection_id || '',
  });
  const [errors, setErrors] = useState({});

  const isEdit = Boolean(prompt);

  const validate = () => {
    const errs = {};
    if (!form.title.trim()) errs.title = 'Title is required.';
    if (!form.content.trim()) errs.content = 'Content is required.';
    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    onSubmit({ ...form, collection_id: form.collection_id || null });
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      <h2 className={styles.heading}>{isEdit ? 'Edit Prompt' : 'Create Prompt'}</h2>
      <div className={styles.field}>
        <label htmlFor="title">Title <span className={styles.required}>*</span></label>
        <input
          id="title"
          name="title"
          value={form.title}
          onChange={handleChange}
          className={errors.title ? styles.inputError : undefined}
          aria-invalid={errors.title ? 'true' : undefined}
          aria-describedby={errors.title ? 'title-error' : undefined}
        />
        {errors.title && <p id="title-error" className={styles.error}>{errors.title}</p>}
      </div>
      <div className={styles.field}>
        <label htmlFor="content">Content <span className={styles.required}>*</span></label>
        <textarea
          id="content"
          name="content"
          className={`${styles.content} ${errors.content ? styles.inputError : ''}`}
          value={form.content}
          onChange={handleChange}
          aria-invalid={errors.content ? 'true' : undefined}
          aria-describedby={errors.content ? 'content-error' : undefined}
        />
        {errors.content && <p id="content-error" className={styles.error}>{errors.content}</p>}
      </div>
      <div className={styles.field}>
        <label htmlFor="description">Description</label>
        <textarea id="description" name="description" rows={3} value={form.description} onChange={handleChange} />
      </div>
      <div className={styles.field}>
        <label htmlFor="collection_id">Collection</label>
        <select id="collection_id" name="collection_id" value={form.collection_id} onChange={handleChange}>
          <option value="">No Collection</option>
          {(collections || []).map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>
      <div className={styles.actions}>
        <Button type="submit" disabled={saving}>{saving ? 'Saving...' : isEdit ? 'Save Changes' : 'Create'}</Button>
        <Button variant="secondary" onClick={onCancel} disabled={saving}>Cancel</Button>
      </div>
    </form>
  );
}
