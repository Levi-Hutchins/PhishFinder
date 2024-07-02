const express = require('express');
const healthController = require('../api/controllers/healthController');
const limiter = require('../api/utils/ratelimiter');

const router = express.Router();

router.get('/generalHealth', limiter, healthController.generalHealth);

module.exports = router;