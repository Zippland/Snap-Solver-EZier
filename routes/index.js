const express = require('express');
const multer = require('multer');
const ImageController = require('../controllers/imageController');
const ProblemController = require('../controllers/problemController');

const router = express.Router();
const storage = multer.memoryStorage();
const upload = multer({ storage });

module.exports = (io) => {
    // 创建控制器实例
    const imageController = new ImageController(io);
    const problemController = new ProblemController();

    // 定义路由
    router.post('/upload', upload.single('file'), imageController.handleImageUpload);
    router.post('/save-crop-settings-and-process', imageController.processCropAndExtract);
    router.post('/solve-problem-with-image', imageController.solveWithImage);
    router.post('/solve-problem', problemController.solveProblem);
    
    return router;
};