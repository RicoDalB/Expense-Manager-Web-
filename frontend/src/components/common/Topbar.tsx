import React from "react";
import { useLocation } from "react-router-dom";
import styles from "./Topbar.module.css";

const Topbar = () => {

    const location = useLocation();
    console.log("percorso attuale", location.pathname);
    //mappiamo url delle pagine
    const pageTitles: { [key: string]: string}={
        "/": "Dashboard",
        "/expenses": "Spese",
        "/categories": "Categorie",
        "/statistics": "Statistiche",
        "/settings": "Impostazini",
    };

    // Se la pagina non è nella mappa di default mettiamo "pagina"
    const currentPageTitle = pageTitles[location.pathname] || "Pagina";

    return(
        <div className={styles.topbar}>
            {/*sezione sinistra con titolo e bottone*/}
            <div className={styles.leftSection}>
                <h2 className={styles.pageTitle}>{currentPageTitle}</h2>
            </div>
            {/*sezione aggiungi spesa*/}
            <div className={styles.centerSection}>
                <button className={styles.addExpenseButton}>Aggiungi Spesa</button>
            </div>
            {/*sezione con bottone utente*/}
            <div className={styles.rightSection}>
                <button className={styles.profileButton}>👤</button>
            </div>

        </div>
    );
};
export default Topbar;