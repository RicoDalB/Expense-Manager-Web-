import React, {useEffect, useState } from "react";
import * as Recharts from "recharts";
const { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } = Recharts;
import { fetchTrends } from "../../services/api";
import styles from "./Chart.module.css";

interface TrendData {
  period: string;
  total: number;
  color?: string;
}

const timeframeTitles = {
  week: "Settimana",
  month: "Questo Mese",
  sixMonths: "Ultimi 6 Mesi",
  year: "Anno",
} as const;



const Chart = () => {
  
  const [chartData, setChartData] = useState<{ name: string; total: number; color: string }[]>([]);
  const [timeframe, setTimeframe] = useState<keyof typeof timeframeTitles>("month");
  const [title, setTitle] = useState<string>(timeframeTitles["month"]);

  
  const aggregateDataByTimeframe = (data: any[], timeframe: string) => {
    const groupedData: Record<string, { name: string; total: number; color: string }> = {};
    const today = new Date();

    switch (timeframe) {
      case "week":
        const daysOfWeek = ["Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab"];
        for (let i = 6; i >= 0; i--) {
          const date = new Date();
          date.setDate(today.getDate() - i);
          const key: string = date.toISOString().split("T")[0] || "unknown"; // ✅ Sempre una stringa valida
          if (key !== "unknown") {
            groupedData[key] = { name: daysOfWeek[date.getDay()] ?? "?", total: 0, color: "#8884d8" };
          } 
        }
        break;

      case "month":
        const weekRanges = ["1-7", "8-14", "15-21", "22-28"];
        if (today.getMonth() !== 1) weekRanges.push("29-31"); // Se il mese ha più di 28 giorni

        weekRanges.forEach(range => {
          groupedData[range] = { name: range, total: 0, color: "#8884d8" };
        });
        break;

      case "sixMonths":
        for (let i = 5; i >= 0; i--) {
          const date = new Date();
          date.setMonth(today.getMonth() - i);
          const monthName = date.toLocaleString("it-IT", { month: "short" });
          groupedData[monthName] = { name: monthName, total: 0, color: "#8884d8" };
        }
        break;

      case "year":
        for (let i = 0; i <= today.getMonth(); i++) {
          const date = new Date(today.getFullYear(), i, 1);
          const monthName = date.toLocaleString("it-IT", { month: "short" });
          groupedData[monthName] = { name: monthName, total: 0, color: "#8884d8" };
        }
        break;
    }

    // 🔹 Somma gli importi in base alla categoria temporale selezionata
    data.forEach(item => {
      const itemDate = new Date(item.date);
      const key = (() => {
        switch (timeframe) {
          case "week":
            return itemDate.toISOString().split("T")[0] || "";
          case "month":
            const day = itemDate.getDate();
            if (day <= 7) return "1-7";
            if (day <= 14) return "8-14";
            if (day <= 21) return "15-21";
            if (day <= 28) return "22-28";
            return "29-31";
          case "sixMonths":
            return itemDate.toLocaleString("it-IT", { month: "short" }) || "";
          case "year":
            return itemDate.toLocaleString("it-IT", { month: "short" }) || "";
          default:
            return "";
        }
      })();

      if (key !== "" && groupedData.hasOwnProperty(key)) {
        groupedData[key] = groupedData[key] || { name: key, total: 0, color: "#8884d8" };
        groupedData[key].total += item.total_spent;
      }


    });

    return Object.values(groupedData);
  };

  /*useEffect(() => {
    const loadChartData = async () => {
      try{
        const today = new Date();
        let startDate, endDate;

        switch(timeFrame){
          case "week":
            startDate = new Date(today.setDate(today.getDate() - 7)).toISOString().split("T")[0];

            break;
          case "month":
            startDate = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split("T")[0];
            break;
          case "sixMonth":
            startDate = new Date(today.setMonth(today.getMonth() - 6)).toISOString().split("T")[0];

            break;
          case "year":
            startDate = new Date(today.getFullYear(), 0, 1).toISOString().split("T")[0];
            break;
          default:
            startDate = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split("T")[0];
        }
        endDate = today.toISOString().split("T")[0];
        console.log(`📅 Fetching data from: ${startDate} to ${endDate}`);

        startDate = startDate.toISOString().split("T")[0];
        
        const safeStartDate = startDate ?? "";
        const safeEndDate = endDate ?? "";

        //recupero dati backend
        const data = await fetchTrends(safeStartDate, safeEndDate);
        console.log("📊 Dati ricevuti dal backend:", data);
        console.log("📂 Tipo di dati ricevuti:", typeof data, Array.isArray(data) ? "Array" : "Non è un array");

         if (!Array.isArray(data)) {
          console.error("❌ ERRORE: Il backend ha restituito un oggetto invece di un array", data);
          return;
        }

        //mappatura dati per Rechrt
        const formattedData = data.map((item: any) => ({
          name: item.period ?? "unknown",
          total: item.total ?? 0,
          color: item.color ?? "#8884d8",
        }));
        console.log("📊 Dati formattati per il grafico:", formattedData);

        setChartData(formattedData);
        setTitle(timeframeTitles[timeFrame as keyof typeof timeframeTitles]);
    }catch (error){
        console.error("Errore nel recupero dei dati", error);
      }
  };
  loadChartData();
}, [timeFrame]);*//*
    useEffect(() => {
    const loadChartData = async () => {
      try {
        const today = new Date();
        let startDate: string = "";
        let endDate: string = new Date().toISOString().split("T")[0] || ""; // Data di oggi

        switch (timeframe) {
          case "week":
            startDate = new Date(today.setDate(today.getDate() - 7)).toISOString().split("T")[0] || "";
            break;
          case "month":
            startDate = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split("T")[0] || "";
            break;
          case "sixMonths":
            startDate = new Date(today.setMonth(today.getMonth() - 6)).toISOString().split("T")[0] || "";
            break;
          case "year":
            startDate = new Date(today.getFullYear(), 0, 1).toISOString().split("T")[0] || "";
            break;
          default:
            startDate = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split("T")[0] || "";
        }

        console.log(`📅 Fetching data from: ${startDate} to ${endDate}`);

        const data = await fetchTrends(startDate, endDate);

        console.log("📊 Dati ricevuti dal backend:", data);

        if (!Array.isArray(data)) {
          console.error("❌ ERRORE: Il backend ha restituito un oggetto invece di un array", data);
          return;
        }

        const formattedData = data.map((item) => ({
          name: item.date ? new Date(item.date).toLocaleDateString("it-IT", { month: "short", day: "2-digit" }) : "Sconosciuto", // 📅 Formatta la data
          total: item.total_spent ?? 0, 
          color: item.color ?? "#8884d8",
        }));

        console.log("✅ Dati FINALMENTE corretti per il grafico:", formattedData);


        setChartData(formattedData);
        setTitle(timeframeTitles[timeframe as keyof typeof timeframeTitles]);
      } catch (error) {
        console.error("❌ Errore nel recupero dei dati del grafico:", error);
      }
    };

    loadChartData();
  }, [timeframe]);




  return(
    <div className={styles.chartContainer}>
      <div className={styles.header}>
        <h2>{title}</h2>
        <select
          className={styles.dropdown}
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
        >
          <option value="week">Settimana</option>
          <option value="month">Mese</option>
          <option value="sixMonths">Ultimi 6 mesi</option>
          <option value="year">Anno</option>
        </select>
      </div>

      {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 10 }}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip cursor={{ fillOpacity: 0.1, stroke: "rgba(0,0,0,0.1)", strokeWidth: 1 }} />
              <Bar dataKey="total" fill="#8884d8" barSize={50} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>⚠️ Nessun dato disponibile per il periodo selezionato</p>
        )}
    </div>

  );

};
export default Chart; */
useEffect(() => {
    const loadChartData = async () => {
      try {
        const today = new Date();
        let startDate: string = "";
        let endDate: string = new Date().toISOString().split("T")[0]|| "";

        switch (timeframe) {
          case "week":
            startDate = new Date(today.setDate(today.getDate() - 7)).toISOString().split("T")[0]|| "";
            break;
          case "month":
            startDate = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split("T")[0]|| "";
            break;
          case "sixMonths":
            startDate = new Date(today.setMonth(today.getMonth() - 6)).toISOString().split("T")[0]|| "";
            break;
          case "year":
            startDate = new Date(today.getFullYear(), 0, 1).toISOString().split("T")[0]|| "";
            break;
        }

        console.log(`📅 Fetching data from: ${startDate} to ${endDate}`);
        const data = await fetchTrends(startDate, endDate);

        console.log("📊 Dati ricevuti dal backend:", data);

        if (!Array.isArray(data)) {
          console.error("❌ ERRORE: Il backend ha restituito un oggetto invece di un array", data);
          return;
        }

        const formattedData = aggregateDataByTimeframe(data, timeframe);
        console.log("✅ Dati formattati per il grafico:", formattedData);

        setChartData(formattedData);
        setTitle(timeframeTitles[timeframe as keyof typeof timeframeTitles]);
      } catch (error) {
        console.error("❌ Errore nel recupero dei dati del grafico:", error);
      }
    };

    loadChartData();
  }, [timeframe]);

    const maxValue = Math.max(...chartData.map((item) => item.total), 0);
  const roundedMaxY = Math.ceil(maxValue * 1.1 / 10) * 10; // ✅ Arrotonda al multiplo di 10 più vicino
  const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        backgroundColor: "black", // ✅ Sfondo nero come esempio
        color: "white",
        padding: "6px 10px",
        borderRadius: "5px",
        fontSize: "14px",
        fontWeight: "bold"
      }}>
         {payload[0].value}€
      </div>
    );
  }
  return null;
};
const pastelColors = ["#A78BFA", "#FBBF24", "#60A5FA", "#34D399", "#F472B6", "#93C5FD", "#FCD34D"];

const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);


  return (
    <div className={styles.chartContainer}>
      <div className={styles.header}>
        <h2>{title}</h2>
        <select
          className={styles.dropdown}
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value as keyof typeof timeframeTitles)}
        >
          <option value="week">Settimana</option>
          <option value="month">Mese</option>
          <option value="sixMonths">Ultimi 6 mesi</option>
          <option value="year">Anno</option>
        </select>
      </div>

      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
<BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 10 }}>
  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" /> {/* ✅ Linee tratteggiate attivate */}
  <XAxis dataKey="name" stroke="#A0AEC0" tick={{ fill: "#1A202C", fontSize: 14, fontWeight: "bold" }} axisLine={false} tickLine={false} />
  <YAxis domain={[0, roundedMaxY]} stroke="#E5E7EB" tick={{ fill: "#A0AEC0", fontSize: 12 }} axisLine={false} tickLine={false} />
  <Tooltip content={<CustomTooltip />} cursor={false} />
  <Bar dataKey="total" barSize={50} radius={[8, 8, 0, 0]}>
    {chartData.map((entry, index) => (
      <Cell key={`cell-${index}`} fill={pastelColors[index % pastelColors.length]} opacity={hoveredIndex === null || hoveredIndex === index ? 1 : 0.3} onMouseEnter={() => setHoveredIndex(index)} onMouseLeave={() => setHoveredIndex(null)} />
    ))}
  </Bar>
</BarChart>

        </ResponsiveContainer>
      ) : (
        <p>⚠️ Nessun dato disponibile da visualizzare</p>
      )}
    </div>
  );
};

export default Chart;
