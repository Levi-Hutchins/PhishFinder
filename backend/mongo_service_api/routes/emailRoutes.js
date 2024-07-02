const express = require('express');
const emailController = require('../api/controllers/emailController');
const limiter = require('../api/utils/ratelimiter');

const router = express.Router();

router.get('/get_email_data', limiter, emailController.getEmailData)

router.post('/insert_email_data',limiter, emailController.insertEmailData);

module.exports = router;