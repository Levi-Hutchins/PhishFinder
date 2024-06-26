const express = require('express');
const linkController  = require('../api/controllers/linkController');
const { body, validationResult } = require("express-validator");
const limiter = require('../api/utils/ratelimiter');

const router = express.Router();

router.get('/get_link_data', linkController.getLinkData);

router.post(
    '/insert_link_data',
    [
      body('link').isURL(),
    ],
    limiter,
    linkController.insertLinkData
  );


module.exports = router;