import React, { useState } from "react";
import AddExpenseModal from "../Modal/AddExpenseModal";
import { useLocation } from "react-router-dom";
import styles from "./Topbar.module.css";
import { fetchExpenses } from "../../services/api";


const Topbar = () => {
  const location = useLocation();
  const [showModal, setShowModal] = useState(false);
  const [expenses, setExpenses] = useState<any[]>([]);

  // Mappiamo gli URL delle pagine per il titolo della pagina
  const pageTitles: { [key: string]: string } = {
    "/": "Dashboard",
    "/expenses": "Spese",
    "/categories": "Categorie",
    "/statistics": "Statistiche",
    "/settings": "Impostazioni",
  };

  // Se la pagina non è nella mappa di default, mettiamo "pagina"
  const currentPageTitle = pageTitles[location.pathname] || "Pagina";

  // Funzione per aprire il modal
  const handleOpenModal = () => setShowModal(true);

  // Funzione per chiudere il modal
  const handleCloseModal = () => setShowModal(false);

  const refreshData = async () => {
    try {
      const data = await fetchExpenses();
      setExpenses(data);
    }catch (error) {
      console.error("errore nel aggiornamento spese", error);
    }
    };
  

  return (
    <>
      <div className={styles.topbar}>
        <div className={styles.leftSection}>
          <h2 className={styles.pageTitle}>{currentPageTitle}</h2>
        </div>
        <div className={styles.centerSection}>
          <button
            className={styles.addExpenseButton}
            onClick={handleOpenModal}
          >
            Aggiungi Spesa
          </button>
        </div>
        <div className={styles.rightSection}>
          <button className={styles.profileButton}>👤</button>
        </div>
      </div>

      {/* Passiamo le funzioni di apertura e chiusura al modal */}
      <AddExpenseModal isOpen={showModal} onClose={handleCloseModal} onUpdateData={refreshData} />
    </>
  );
};

export default Topbar;
