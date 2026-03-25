import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Main() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  useEffect(() => {
    if (!user) navigate('/');
  }, []);

  const logout = async () => {
    await api.post('/auth/logout');
    localStorage.removeItem('user');
    navigate('/');
  };

  const menus = [
    { label: '客戶資料', icon: '🏢', path: '/cust' },
    { label: '廠商資料', icon: '🏭', path: '/fact' },
    { label: '商品資料', icon: '📦', path: '/item' },
    { label: '用戶資料', icon: '👤', path: '/user' },
  ];

  return (
    <div className="container">
      <div className="main-header">
        <span className="main-title">TriSys</span>
        <button className="logout-btn" onClick={logout}>登出</button>
      </div>
      <div className="welcome-text">歡迎，{user?.username || user?.userid}</div>
      <div className="menu-grid">
        {menus.map(m => (
          <button key={m.path} className="menu-card" onClick={() => navigate(m.path)}>
            <div className="menu-icon">{m.icon}</div>
            <div className="menu-label">{m.label}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
