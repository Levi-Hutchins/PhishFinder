const express = require('express');
const emailController = require('../api/controllers/emailController');
const {boy, validate} = require('express-validation');

const router = express.Router();

router.get('/get_email_data', emailController.getEmailData)

router.post('/insert_email_data', emailController.insertEmailData);

module.exports = router;