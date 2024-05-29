const express = require('express');
const linkRoutes = require('./linkRoutes');
const emailRoutes = require('./emailRoutes');
const healthRoutes = require('./healthRoutes');

const router = express.Router();

router.use('/link', linkRoutes);
router.use('/mail', emailRoutes);
router.use('/health', healthRoutes);

module.exports = router;