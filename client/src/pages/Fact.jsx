import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const EMPTY = { fact_code: '', fact_name: '', remark: '' };

export default function Fact() {
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
    const res = await api.get('/fact');
    setRecords(res.data);
  };

  const openAdd = () => { setForm(EMPTY); setIsEdit(false); setError(''); setModal(true); };
  const openEdit = r => { setForm({ ...r }); setIsEdit(true); setError(''); setModal(true); };

  const save = async () => {
    setError('');
    if (!form.fact_code.trim() || !form.fact_name.trim()) { setError('代碼與名稱為必填'); return; }
    try {
      if (isEdit) await api.put(`/fact/${form.fact_code}`, form);
      else         await api.post('/fact', form);
      setModal(false);
      load();
    } catch (e) {
      setError(e.response?.data?.error || '儲存失敗');
    }
  };

  const del = async (code) => {
    if (!window.confirm(`確定刪除 ${code}？`)) return;
    await api.delete(`/fact/${code}`);
    load();
  };

  return (
    <div className="container">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate('/main')}>← 返回</button>
        <h2>廠商資料維護</h2>
        <button className="add-btn" onClick={openAdd}>＋ 新增</button>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>廠商代碼</th><th>廠商名稱</th><th>備註</th><th>操作</th></tr>
          </thead>
          <tbody>
            {records.length === 0
              ? <tr className="empty-row"><td colSpan={4}>尚無資料</td></tr>
              : records.map(r => (
                <tr key={r.fact_code}>
                  <td>{r.fact_code}</td>
                  <td>{r.fact_name}</td>
                  <td>{r.remark}</td>
                  <td className="action-cell">
                    <button className="edit-btn" onClick={() => openEdit(r)}>修改</button>
                    <button className="del-btn"  onClick={() => del(r.fact_code)}>刪除</button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {modal && (
        <div className="modal-overlay" onClick={e => e.target === e.currentTarget && setModal(false)}>
          <div className="modal-card">
            <div className="modal-title">{isEdit ? '修改廠商' : '新增廠商'}</div>
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group">
              <label>廠商代碼</label>
              <input value={form.fact_code} readOnly={isEdit}
                onChange={e => setForm({ ...form, fact_code: e.target.value })} placeholder="廠商代碼" />
            </div>
            <div className="form-group">
              <label>廠商名稱</label>
              <input value={form.fact_name}
                onChange={e => setForm({ ...form, fact_name: e.target.value })} placeholder="廠商名稱" />
            </div>
            <div className="form-group">
              <label>備註說明</label>
              <input value={form.remark}
                onChange={e => setForm({ ...form, remark: e.target.value })} placeholder="備註說明" />
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
