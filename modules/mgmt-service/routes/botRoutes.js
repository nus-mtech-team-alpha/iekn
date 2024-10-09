const express = require('express');
const botController = require('../controllers/botController');
const router = express.Router();

router.post('/', botController.createBot);
router.get('/', botController.getBots);
router.get('/:id', botController.getBot);
router.put('/:id', botController.updateBot);
router.delete('/:id', botController.deleteBot);

module.exports = router;