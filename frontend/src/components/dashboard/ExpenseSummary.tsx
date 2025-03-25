import React from "react";
import styles from "./ExpenseSummary.module.css"; // ✅ Assicurati che il percorso sia corretto


const ExpenseSummary = () => {
  return (
    <div className={styles.expenseSummaryPlaceholder}>
      <p>💰 Placeholder per il riepilogo spese</p>
    </div>
  );
};

export default ExpenseSummary;
