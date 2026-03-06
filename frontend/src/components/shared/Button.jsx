import styles from './Button.module.css';

export default function Button({ children, onClick, variant = 'primary', size = 'md', disabled = false, type = 'button' }) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${styles.btn} ${styles[variant]} ${styles[size]}`}
    >
      {children}
    </button>
  );
}
