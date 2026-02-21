require('dotenv').config();
const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT,
  waitForConnections: true,
  connectionLimit: 10,
});

// GET alertes actives
app.get('/api/alerts', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT a.id, a.type, a.value, a.level, a.timestamp, a.status,
             m.room, m.floor,
             p.first_name, p.last_name
      FROM alerts a
      JOIN monitors m ON a.monitor_id = m.id
      JOIN patients p ON a.patient_id = p.id
      WHERE a.status = 'alert'
      ORDER BY a.timestamp DESC
    `);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erreur base de données' });
  }
});

// PUT résoudre une alerte
app.put('/api/alerts/:id/resolve', async (req, res) => {
  try {
    await pool.query(`UPDATE alerts SET status = 'resolved' WHERE id = ?`, [req.params.id]);
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erreur base de données' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Serveur lancé sur http://localhost:${PORT}`));
