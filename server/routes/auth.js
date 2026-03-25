const express = require('express');
const router = express.Router();
const { getPool, sql } = require('../config/db');

router.post('/login', async (req, res) => {
  const { userid, pwd } = req.body;
  try {
    const pool = await getPool();
    const result = await pool.request()
      .input('userid', sql.VarChar(20), userid)
      .input('pwd', sql.VarChar(50), pwd)
      .query('SELECT userid, username FROM [user] WHERE userid=@userid AND pwd=@pwd');
    if (result.recordset.length === 0) {
      return res.status(401).json({ error: '帳號或密碼錯誤' });
    }
    req.session.user = result.recordset[0];
    res.json({ user: result.recordset[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/logout', (req, res) => {
  req.session.destroy();
  res.json({ ok: true });
});

router.get('/session', (req, res) => {
  res.json({ user: req.session.user || null });
});

module.exports = router;
