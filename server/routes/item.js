const express = require('express');
const router = express.Router();
const { getPool, sql } = require('../config/db');

router.get('/', async (req, res) => {
  try {
    const pool = await getPool();
    const result = await pool.request().query(
      `SELECT i.item_code, i.item_name, i.fact_code, f.fact_name
       FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_code
       ORDER BY i.item_code`
    );
    res.json(result.recordset);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/', async (req, res) => {
  const { item_code, item_name, fact_code } = req.body;
  try {
    const pool = await getPool();
    await pool.request()
      .input('item_code', sql.VarChar(20), item_code)
      .input('item_name', sql.NVarChar(100), item_name)
      .input('fact_code', sql.VarChar(20), fact_code)
      .query('INSERT INTO item (item_code,item_name,fact_code) VALUES (@item_code,@item_name,@fact_code)');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.put('/:code', async (req, res) => {
  const { item_name, fact_code } = req.body;
  try {
    const pool = await getPool();
    await pool.request()
      .input('item_code', sql.VarChar(20), req.params.code)
      .input('item_name', sql.NVarChar(100), item_name)
      .input('fact_code', sql.VarChar(20), fact_code)
      .query('UPDATE item SET item_name=@item_name,fact_code=@fact_code WHERE item_code=@item_code');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.delete('/:code', async (req, res) => {
  try {
    const pool = await getPool();
    await pool.request()
      .input('item_code', sql.VarChar(20), req.params.code)
      .query('DELETE FROM item WHERE item_code=@item_code');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
