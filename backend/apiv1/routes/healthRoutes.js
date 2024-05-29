const express = require('express');
const healthController = require('../api/controllers/healthController');

const router = express.Router();

router.get('/generalHealth', healthController.generalHealth);

module.exports = router;