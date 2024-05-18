const express = require('express');
const linkRoutes = require('./linkRoutes');

const router = express.Router();

router.use('/link', linkRoutes);

module.exports = router;