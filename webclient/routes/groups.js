const express = require('express');
const router = express.Router();

const groups_controller = require('../controllers/groups')

router.get('/', groups_controller.index);

module.exports = router