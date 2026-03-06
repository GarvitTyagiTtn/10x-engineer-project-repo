import styles from './PromptCard.module.css';

export default function PromptCard({ prompt, onClick, collectionName }) {
  return (
    <button className={styles.card} onClick={onClick} type="button" role="listitem" aria-label={`View prompt: ${prompt.title}`}>
      <h3 className={styles.title}>{prompt.title}</h3>
      {prompt.description && <p className={styles.description}>{prompt.description}</p>}
      <div className={styles.footer}>
        {collectionName ? <span className={styles.badge}>{collectionName}</span> : <span />}
        <time className={styles.date} dateTime={prompt.updated_at || prompt.created_at}>
          {new Date(prompt.updated_at || prompt.created_at).toLocaleDateString()}
        </time>
      </div>
    </button>
  );
}
