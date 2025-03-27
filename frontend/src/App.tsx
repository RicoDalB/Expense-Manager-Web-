import { useEffect } from "react";
import Navbar from "./components/navbar/navbar";
import Topbar from "./components/common/Topbar";
import AppRoutes from "./routes";


const App = () => {
  useEffect(() => {
    document.title = "Expense Manager";
  }, []);
  
  return (
      <div style={{ backgroundColor: "white", color: "black", minHeight: "100vh" }}>
        <Navbar /> 
        <Topbar />
        <AppRoutes />
      </div>
  );
};

export default App;