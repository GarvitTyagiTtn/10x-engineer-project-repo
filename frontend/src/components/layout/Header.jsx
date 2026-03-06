import Button from '../shared/Button';
import styles from './Header.module.css';

export default function Header({ onNewPrompt, onToggleSidebar }) {
  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <button
          className={styles.menuBtn}
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
          type="button"
        >
          ☰
        </button>
        <span className={styles.logo}>PromptLab</span>
      </div>
      <Button onClick={onNewPrompt}>+ New Prompt</Button>
    </header>
  );
}
