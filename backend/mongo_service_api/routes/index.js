const express = require('express');
const linkRoutes = require('./linkRoutes');
const emailRoutes = require('./emailRoutes');
const healthRoutes = require('./healthRoutes');
const limiter = require('../api/utils/ratelimiter');
const router = express.Router();

router.use('/link', limiter, linkRoutes);
router.use('/email', limiter, emailRoutes);
router.use('/health', limiter, healthRoutes);

module.exports = router;