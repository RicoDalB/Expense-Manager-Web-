import React from "react";
import Topbar from "../components/common/Topbar";
import Chart from "../components/dashboard/Chart";
import ExpenseSummary from "../components/dashboard/ExpenseSummary";
import RecentExpenses from "../components/dashboard/RecentExpenses";
import styles from "./dashboard.module.css";

const Dashboard = () => {
    return (
        <div className={styles.dashboardWrapper}>
            <Topbar />
        <div className={styles.dashboardContainer}>
            {/* contenuto della dashboard */}
            <div className={styles.dashboardGrid}>
                {/*sezione grafico */}
                <div className={styles.chartSection}>
                <Chart />
                </div>

                {/*Sezione riepilogo spese*/}
                <div className={styles.ExpenseSummarySection}>
                    <ExpenseSummary />
                </div>

                {/* Sezione Ultime spese */}
                <div className={styles.recentExpensesSection}>
                    <RecentExpenses />
                </div>
            </div>
        </div>
        </div>
    );
};

export default Dashboard;