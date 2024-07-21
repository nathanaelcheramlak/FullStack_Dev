import { BrowserRouter, Routes, Route } from "react-router-dom";
import Transaction from "./pages/transaction/Transaction";
import EditTransaction from "./pages/transaction/edit-transaction/EditTransaction";
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/transaction" element={<Transaction />} />
        <Route path="/transaction/edit" element={<EditTransaction />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
