const BASE_URL ="http://127.0.0.1:8000"; // Modificare se il backend è ospitato altrove

// 🔹 API per la gestione delle spese
export const fetchExpenses = async () => {
  const res = await fetch(`${BASE_URL}/expenses/`);
  if (!res.ok) throw new Error("Errore nel recupero delle spese");
  return res.json();
};

export const fetchExpenseById = async (id: number) => {
  const res = await fetch(`${BASE_URL}/expense/${id}`);
  if (!res.ok) throw new Error("Errore nel recupero della spesa");
  return res.json();
};

export const addExpense = async (expenseData: object) => {
  const res = await fetch(`${BASE_URL}/expenses/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expenseData),
  });
  if (!res.ok) throw new Error("Errore nell'aggiunta della spesa");
  return res.json();
};

export const updateExpense = async (id: number, expenseData: object) => {
  const res = await fetch(`${BASE_URL}/expenses/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expenseData),
  });
  if (!res.ok) throw new Error("Errore nella modifica della spesa");
  return res.json();
};

export const deleteExpense = async (id: number) => {
  const res = await fetch(`${BASE_URL}/expense/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Errore nell'eliminazione della spesa");
};

// 🔹 API per statistiche sulle spese
export const fetchSummaryStats = async (startDate?: string, endDate?: string) => {
  let url = `${BASE_URL}/expenses/stats/summary`;
  if (startDate && endDate) {
    url += `?start_date=${startDate}&end_date=${endDate}`;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error("Errore nel recupero delle statistiche");
  return res.json();
};;

export const fetchTrends = async (startDate: string, endDate: string) => {
  const url = `${BASE_URL}/expenses/stats/trends?start_date=${startDate}&end_date=${endDate}`;
  console.log("🔍 Chiamata API:", url);

  const response = await fetch(url);
  if (!response.ok) {
    console.error("❌ Errore API:", response.status, response.statusText);
    throw new Error("Errore nel recupero delle tendenze di spesa");
  }

  const result = await response.json();
  console.log("📩 Dati ricevuti dall'API:", result);

  // ✅ Estrarre `trend_data` se presente
  if (result && result.trend_data && Array.isArray(result.trend_data)) {
    console.log("✅ Il backend ha restituito `trend_data` con", result.trend_data.length, "elementi");
    return result.trend_data;
  }

  console.error("❌ ERRORE: `trend_data` non è un array valido", result);
  return [];
};





/* const fetchTrends = async (startDate: string, endDate: string) => {
  const response = await fetch(`${BASE_URL}/expenses/stats/trends?start_date=${startDate}&end_date=${endDate}`);
  if (!response.ok) throw new Error("Errore nel recupero delle tendenze di spesa");
  return response.json();
};*/

export const fetchExpensesByCategory = async () => {
  const res = await fetch(`${BASE_URL}/expenses/stats/by-category`);
  if (!res.ok) throw new Error("Errore nel recupero delle categorie più usate");
  return res.json();
};

export const fetchTopExpenses = async (startDate: string, endDate: string, limit: number = 5) => {
  const url = `${BASE_URL}/expenses/stats/top-expenses?start_date=${startDate}&end_date=${endDate}&limit=${limit}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Errore nel recupero delle spese più alte");
  return res.json();
};

export const fetchExpenseAverage = async () => {
  const res = await fetch(`${BASE_URL}/expenses/stats/average`);
  if (!res.ok) throw new Error("Errore nel recupero della spesa media giornaliera");
  return res.json();
};

// 🔹 API per la gestione delle categorie
export const fetchCategories = async () => {
  const res = await fetch(`${BASE_URL}/categories/`);
  if (!res.ok) throw new Error("Errore nel recupero delle categorie");
  return res.json();
};

export const addCategory = async (name: string) => {
  const res = await fetch(`${BASE_URL}/categories/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error("Errore nella creazione della categoria");
  return res.json();
};

export const updateCategory = async (id: number, name: string) => {
  const res = await fetch(`${BASE_URL}/categories/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error("Errore nella modifica della categoria");
  return res.json();
};

export const deleteCategory = async (id: number) => {
  const res = await fetch(`${BASE_URL}/categories/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Errore nell'eliminazione della categoria");
};

// 🔹 API avanzate
export const predictMonthlyExpense = async () => {
  const res = await fetch(`${BASE_URL}/expenses/predict-monthly`);
  if (!res.ok) throw new Error("Errore nella previsione della spesa mensile");
  return res.json();
};

export const addRecurringExpense = async (expenseData: object) => {
  const res = await fetch(`${BASE_URL}/expenses/recurring`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expenseData),
  });
  if (!res.ok) throw new Error("Errore nell'aggiunta della spesa ricorrente");
  return res.json();
};

export const exportExpensesCSV = async () => {
  const res = await fetch(`${BASE_URL}/expenses/export/csv`);
  if (!res.ok) throw new Error("Errore nell'esportazione CSV");
  return res.blob();
};

export const exportExpensesPDF = async () => {
  const res = await fetch(`${BASE_URL}/expenses/export/pdf`);
  if (!res.ok) throw new Error("Errore nell'esportazione PDF");
  return res.blob();
};

export const backupExpenses = async () => {
  const res = await fetch(`${BASE_URL}/expenses/backup`);
  if (!res.ok) throw new Error("Errore nel backup delle spese");
  return res.json();
};
