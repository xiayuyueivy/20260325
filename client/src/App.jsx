import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Main  from './pages/Main';
import Cust  from './pages/Cust';
import Fact  from './pages/Fact';
import Item  from './pages/Item';
import User  from './pages/User';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"     element={<Login />} />
        <Route path="/main" element={<Main  />} />
        <Route path="/cust" element={<Cust  />} />
        <Route path="/fact" element={<Fact  />} />
        <Route path="/item" element={<Item  />} />
        <Route path="/user" element={<User  />} />
      </Routes>
    </BrowserRouter>
  );
}
