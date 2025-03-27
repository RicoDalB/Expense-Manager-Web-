import React, { useEffect, useState} from "react";
import { fetchExpenses, fetchExpensesByCategory, fetchSummaryStats } from "../../services/api";
import {format} from "date-fns";
import {Pie} from "react-chartjs-2";
import {ChartOptions, Chart as ChartJS, ArcElement, Tooltip, Legend, FontSpec } from "chart.js";
import styles from "./ExpenseSummary.module.css";
import Expenses from "../../pages/expense";

ChartJS.register(ArcElement, Tooltip, Legend);

interface Expense {
  id: number;
  amount: number;
  date: string;
  description: string;
  category: {
    id: number;
    name: string;
    icon: string;
  } | string; // <-- può essere anche stringa!
}


const MONTHS = [
  "gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
  "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre",
];

const COLORS = ["#A78BFA", "#FBBF24", "#60A5FA", "#34D399", "#F472B6", "#FCD34D"];

const ExpenseSummary = () => {
  const currentMonth = new Date().getMonth();
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth());
  const [filteredExpenses, setFilteredExpenses] = useState<Expense[]>([]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
     const loadData = async () => {
      const now = new Date();
      const currentMonth = now.getMonth();
      const currentYear = now.getFullYear();
      const displayYear = selectedMonth > currentMonth ? currentYear - 1 : currentYear;
      const startDate = new Date(displayYear, selectedMonth, 1);
      const ednDate = new Date(displayYear, selectedMonth+ 1, 0);
      try{
        const allExpense: Expense[] = await fetchExpenses();
        const filtred = allExpense.filter((exp) => {
          const date = new Date(exp.date);
          return (
            date.getFullYear() == displayYear && date.getMonth() === selectedMonth
          );
        });
        setFilteredExpenses(filtred);

        const totalSum = filtred.reduce((sum, exp) => sum + exp.amount, 0);
        setTotal(totalSum);
        
      }catch (error){
        console.error("Errore nel caricamento dei dati", error);
      }
    };
    loadData();
    
  }, [selectedMonth]);

  const getTopCategories = () => {
    const grouped: { [category: string]: number} = {};
    filteredExpenses.forEach((exp) => {
  const categoryName = typeof exp.category === "string"
    ? exp.category
    : exp.category?.name || "Sconosciuta";

  grouped[categoryName] = (grouped[categoryName] || 0) + exp.amount;
});


    return Object.entries(grouped)
    .map(([name, amount]) => ({ name, amount }))
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 6);
  };

  const topCategories = getTopCategories();

const data = {
  labels: topCategories.map((c) => c.name),
  datasets: [
    {
      data: topCategories.map((c) => c.amount),
      backgroundColor: COLORS.slice(0, topCategories.length),
      hoverBackgroundColor: COLORS.slice(0, topCategories.length), // 👈 Nessuna trasparenza
      borderWidth: 0,
      hoverOffset: 14,
      hoverBorderColor: "#fff", // crea il bordo “muro bianco”
      hoverBorderWidth: 2,
    },
  ],
};

const options: ChartOptions<'pie'> = {
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: "#ffffff",
      titleColor: "#000000",
      bodyColor: "#000000",
      titleFont: {
        size: 14,
        weight: 'bold',
      } as Partial<FontSpec>,
      bodyFont: {
        size: 13,
        weight: 500,
      } as Partial<FontSpec>,
      borderColor: "#e0e0e0",
      borderWidth: 1,
      cornerRadius: 4,
    },
  },
  layout: {
    padding: 10,
  },
  cutout: "70%",
  responsive: true,
  maintainAspectRatio: false,
  elements: {
    arc: {
      borderWidth: 0,
      hoverOffset: 14,
      hoverBorderColor: "#fff",
      hoverBorderWidth: 2,
    },
  },
};



  return (
  <div className={styles.container}>
    <div className={styles.header}>
      <h2 className={styles.title}>Riepilogo Spese</h2>
      <select
        className={styles.select}
        value={selectedMonth}
        onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
      >
        {MONTHS.map((m, i) => (
          <option key={i} value={i}>
            {m}
          </option>
        ))}
      </select>
    </div>

    <div className={styles.content}>
      <div className={styles.chart}>
        <Pie data={data} options={options} />
        <div className={styles.total}>
          <p>Total</p>
          <strong>€{total.toFixed(2)}</strong>
        </div>
      </div>

      <div className={styles.legendGrid}>
        {topCategories.map((cat, i) => (
          <div key={i} className={styles.legendItem}>
            <span className={styles.dot} style={{ backgroundColor: COLORS[i] }} />
            <div className={styles.legendText}>
              <div className={styles.categoryName}>{cat.name}</div>
              <div className={styles.categoryAmount}>€{cat.amount.toFixed(2)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

};

export default ExpenseSummary;