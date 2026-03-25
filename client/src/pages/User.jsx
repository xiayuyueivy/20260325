import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const EMPTY = { userid: '', username: '', pwd: '' };

export default function User() {
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(EMPTY);
  const [isEdit, setIsEdit] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!localStorage.getItem('user')) { navigate('/'); return; }
    load();
  }, []);

  const load = async () => {
    const res = await api.get('/user');
    setRecords(res.data);
  };

  const openAdd = () => { setForm(EMPTY); setIsEdit(false); setError(''); setModal(true); };
  const openEdit = r => { setForm({ ...r }); setIsEdit(true); setError(''); setModal(true); };

  const save = async () => {
    setError('');
    if (!form.userid.trim() || !form.username.trim() || !form.pwd.trim()) { setError('代碼、名稱與密碼為必填'); return; }
    try {
      if (isEdit) await api.put(`/user/${form.userid}`, form);
      else         await api.post('/user', form);
      setModal(false);
      load();
    } catch (e) {
      setError(e.response?.data?.error || '儲存失敗');
    }
  };

  const del = async (id) => {
    if (!window.confirm(`確定刪除 ${id}？`)) return;
    await api.delete(`/user/${id}`);
    load();
  };

  return (
    <div className="container">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate('/main')}>← 返回</button>
        <h2>用戶資料維護</h2>
        <button className="add-btn" onClick={openAdd}>＋ 新增</button>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>用戶代碼</th><th>用戶名稱</th><th>密碼</th><th>操作</th></tr>
          </thead>
          <tbody>
            {records.length === 0
              ? <tr className="empty-row"><td colSpan={4}>尚無資料</td></tr>
              : records.map(r => (
                <tr key={r.userid}>
                  <td>{r.userid}</td>
                  <td>{r.username}</td>
                  <td>{r.pwd}</td>
                  <td className="action-cell">
                    <button className="edit-btn" onClick={() => openEdit(r)}>修改</button>
                    <button className="del-btn"  onClick={() => del(r.userid)}>刪除</button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {modal && (
        <div className="modal-overlay" onClick={e => e.target === e.currentTarget && setModal(false)}>
          <div className="modal-card">
            <div className="modal-title">{isEdit ? '修改用戶' : '新增用戶'}</div>
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group">
              <label>用戶代碼</label>
              <input value={form.userid} readOnly={isEdit}
                onChange={e => setForm({ ...form, userid: e.target.value })} placeholder="用戶代碼" />
            </div>
            <div className="form-group">
              <label>用戶名稱</label>
              <input value={form.username}
                onChange={e => setForm({ ...form, username: e.target.value })} placeholder="用戶名稱" />
            </div>
            <div className="form-group">
              <label>用戶密碼</label>
              <input value={form.pwd}
                onChange={e => setForm({ ...form, pwd: e.target.value })} placeholder="用戶密碼" />
            </div>
            <div className="modal-footer">
              <button className="btn btn-default" onClick={() => setModal(false)}>取消</button>
              <button className="btn btn-primary" onClick={save}>儲存</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
