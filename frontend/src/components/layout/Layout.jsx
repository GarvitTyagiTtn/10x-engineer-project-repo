import { useState } from 'react';
import Header from './Header';
import styles from './Layout.module.css';

export default function Layout({ children, sidebar, onNewPrompt }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className={styles.layout}>
      <Header
        onNewPrompt={onNewPrompt}
        onToggleSidebar={() => setSidebarOpen((v) => !v)}
      />
      <div className={styles.body}>
        <aside className={`${styles.sidebar} ${sidebarOpen ? styles.sidebarOpen : ''}`}>
          {sidebar}
        </aside>
        {sidebarOpen && (
          <div
            className={styles.overlay}
            onClick={() => setSidebarOpen(false)}
            aria-hidden="true"
          />
        )}
        <main className={styles.main}>{children}</main>
      </div>
    </div>
  );
}
