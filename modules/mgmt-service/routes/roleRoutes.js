const express = require('express');
const roleController = require('../controllers/roleController');
const router = express.Router();

router.post('/', roleController.createRole);
router.get('/', roleController.getRoles);
router.get('/:id', roleController.getRole);
router.put('/:id', roleController.updateRole);
router.delete('/:id', roleController.deleteRole);

module.exports = router;