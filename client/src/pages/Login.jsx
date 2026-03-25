import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ userid: '', pwd: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const login = async (e) => {
    e.preventDefault();
    setError('');
    if (!form.userid || !form.pwd) { setError('請輸入帳號與密碼'); return; }
    setLoading(true);
    try {
      const res = await api.post('/auth/login', form);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/main');
    } catch (err) {
      setError(err.response?.data?.error || '登入失敗');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="login-logo">TriSys</div>
        <div className="login-sub">資料維護系統</div>
        <form onSubmit={login}>
          {error && <div className="alert alert-error">{error}</div>}
          <div className="form-group">
            <label>帳號</label>
            <input
              type="text"
              placeholder="請輸入帳號"
              value={form.userid}
              onChange={e => setForm({ ...form, userid: e.target.value })}
              autoComplete="username"
            />
          </div>
          <div className="form-group">
            <label>密碼</label>
            <input
              type="password"
              placeholder="請輸入密碼"
              value={form.pwd}
              onChange={e => setForm({ ...form, pwd: e.target.value })}
              autoComplete="current-password"
            />
          </div>
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? '登入中...' : '登入'}
          </button>
        </form>
      </div>
    </div>
  );
}
