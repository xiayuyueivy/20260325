const express = require('express');
const session = require('express-session');
const cors = require('cors');
require('dotenv').config();

const authRouter = require('./routes/auth');
const custRouter = require('./routes/cust');
const factRouter = require('./routes/fact');
const itemRouter = require('./routes/item');
const userRouter = require('./routes/user');

const app = express();

app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));

app.use(express.json());

app.use(session({
  secret: process.env.SESSION_SECRET || 'trisys',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: false, maxAge: 8 * 60 * 60 * 1000 }
}));

function requireAuth(req, res, next) {
  if (!req.session.user) return res.status(401).json({ error: '請先登入' });
  next();
}

app.use('/api/auth', authRouter);
app.use('/api/cust', requireAuth, custRouter);
app.use('/api/fact', requireAuth, factRouter);
app.use('/api/item', requireAuth, itemRouter);
app.use('/api/user', requireAuth, userRouter);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
