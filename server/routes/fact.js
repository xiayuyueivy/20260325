const express = require('express');
const router = express.Router();
const { getPool, sql } = require('../config/db');

router.get('/', async (req, res) => {
  try {
    const pool = await getPool();
    const result = await pool.request().query('SELECT * FROM fact ORDER BY fact_code');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/', async (req, res) => {
  const { fact_code, fact_name, remark } = req.body;
  try {
    const pool = await getPool();
    await pool.request()
      .input('fact_code', sql.VarChar(20), fact_code)
      .input('fact_name', sql.NVarChar(100), fact_name)
      .input('remark', sql.NVarChar(200), remark)
      .query('INSERT INTO fact (fact_code,fact_name,remark) VALUES (@fact_code,@fact_name,@remark)');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.put('/:code', async (req, res) => {
  const { fact_name, remark } = req.body;
  try {
    const pool = await getPool();
    await pool.request()
      .input('fact_code', sql.VarChar(20), req.params.code)
      .input('fact_name', sql.NVarChar(100), fact_name)
      .input('remark', sql.NVarChar(200), remark)
      .query('UPDATE fact SET fact_name=@fact_name,remark=@remark WHERE fact_code=@fact_code');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.delete('/:code', async (req, res) => {
  try {
    const pool = await getPool();
    await pool.request()
      .input('fact_code', sql.VarChar(20), req.params.code)
      .query('DELETE FROM fact WHERE fact_code=@fact_code');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
