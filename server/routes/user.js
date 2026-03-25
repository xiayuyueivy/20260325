const express = require('express');
const router = express.Router();
const { getPool, sql } = require('../config/db');

router.get('/', async (req, res) => {
  try {
    const pool = await getPool();
    const result = await pool.request().query('SELECT userid, username, pwd FROM [user] ORDER BY userid');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/', async (req, res) => {
  const { userid, username, pwd } = req.body;
  try {
    const pool = await getPool();
    await pool.request()
      .input('userid', sql.VarChar(20), userid)
      .input('username', sql.NVarChar(100), username)
      .input('pwd', sql.VarChar(50), pwd)
      .query('INSERT INTO [user] (userid,username,pwd) VALUES (@userid,@username,@pwd)');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.put('/:id', async (req, res) => {
  const { username, pwd } = req.body;
  try {
    const pool = await getPool();
    await pool.request()
      .input('userid', sql.VarChar(20), req.params.id)
      .input('username', sql.NVarChar(100), username)
      .input('pwd', sql.VarChar(50), pwd)
      .query('UPDATE [user] SET username=@username,pwd=@pwd WHERE userid=@userid');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.delete('/:id', async (req, res) => {
  try {
    const pool = await getPool();
    await pool.request()
      .input('userid', sql.VarChar(20), req.params.id)
      .query('DELETE FROM [user] WHERE userid=@userid');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
