import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const EMPTY = { item_code: '', item_name: '', fact_code: '' };

export default function Item() {
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);
  const [facts, setFacts] = useState([]);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(EMPTY);
  const [isEdit, setIsEdit] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!localStorage.getItem('user')) { navigate('/'); return; }
    load();
    api.get('/fact').then(r => setFacts(r.data));
  }, []);

  const load = async () => {
    const res = await api.get('/item');
    setRecords(res.data);
  };

  const openAdd = () => {
    setForm({ ...EMPTY, fact_code: facts[0]?.fact_code || '' });
    setIsEdit(false); setError(''); setModal(true);
  };
  const openEdit = r => { setForm({ item_code: r.item_code, item_name: r.item_name, fact_code: r.fact_code }); setIsEdit(true); setError(''); setModal(true); };

  const save = async () => {
    setError('');
    if (!form.item_code.trim() || !form.item_name.trim()) { setError('代碼與名稱為必填'); return; }
    try {
      if (isEdit) await api.put(`/item/${form.item_code}`, form);
      else         await api.post('/item', form);
      setModal(false);
      load();
    } catch (e) {
      setError(e.response?.data?.error || '儲存失敗');
    }
  };

  const del = async (code) => {
    if (!window.confirm(`確定刪除 ${code}？`)) return;
    await api.delete(`/item/${code}`);
    load();
  };

  return (
    <div className="container">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate('/main')}>← 返回</button>
        <h2>商品資料維護</h2>
        <button className="add-btn" onClick={openAdd}>＋ 新增</button>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>商品代碼</th><th>商品名稱</th><th>主供應商</th><th>操作</th></tr>
          </thead>
          <tbody>
            {records.length === 0
              ? <tr className="empty-row"><td colSpan={4}>尚無資料</td></tr>
              : records.map(r => (
                <tr key={r.item_code}>
                  <td>{r.item_code}</td>
                  <td>{r.item_name}</td>
                  <td>{r.fact_name || r.fact_code}</td>
                  <td className="action-cell">
                    <button className="edit-btn" onClick={() => openEdit(r)}>修改</button>
                    <button className="del-btn"  onClick={() => del(r.item_code)}>刪除</button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {modal && (
        <div className="modal-overlay" onClick={e => e.target === e.currentTarget && setModal(false)}>
          <div className="modal-card">
            <div className="modal-title">{isEdit ? '修改商品' : '新增商品'}</div>
            {error && <div className="alert alert-error">{error}</div>}
            <div className="form-group">
              <label>商品代碼</label>
              <input value={form.item_code} readOnly={isEdit}
                onChange={e => setForm({ ...form, item_code: e.target.value })} placeholder="商品代碼" />
            </div>
            <div className="form-group">
              <label>商品名稱</label>
              <input value={form.item_name}
                onChange={e => setForm({ ...form, item_name: e.target.value })} placeholder="商品名稱" />
            </div>
            <div className="form-group">
              <label>主供應商</label>
              <select value={form.fact_code} onChange={e => setForm({ ...form, fact_code: e.target.value })}>
                <option value="">-- 請選擇 --</option>
                {facts.map(f => (
                  <option key={f.fact_code} value={f.fact_code}>{f.fact_code} - {f.fact_name}</option>
                ))}
              </select>
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
