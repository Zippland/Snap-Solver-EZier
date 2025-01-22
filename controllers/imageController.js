// controllers\imageController.js
const ImageService = require('../services/imageService');
const AIServiceFactory = require('../services/aiServiceFactory');

class ImageController {
    constructor(io) {
        this.io = io;
    }

    handleImageUpload = async (req, res) => {
        if (!req.file) {
            return res.status(400).send('No file uploaded.');
        }

        try {
            const base64Image = req.file.buffer.toString('base64');
            this.io.emit('new_image_uploaded', { image: base64Image });
            res.send('Initial image uploaded. Waiting for crop settings.');
        } catch (error) {
            console.error('Upload Error:', error);
            res.status(500).send('An error occurred while uploading the image.');
        }
    }

    processCropAndExtract = async (req, res) => {
        const { cropSettings, image } = req.body;
        
        try {
            const buffer = Buffer.from(image.replace(/^data:image\/\w+;base64,/, ''), 'base64');
            const base64CroppedImage = await ImageService.processImage(buffer, cropSettings);
            
            const ExtractionService = AIServiceFactory.getExtractionService();
            const extractedText = await ExtractionService.extractText(base64CroppedImage);
            
            res.json({ extractedText });
        } catch (error) {
            console.error('Processing Error:', error);
            res.status(500).send('An error occurred while processing the image.');
        }
    }

    solveWithImage = async (req, res) => {
        const { cropSettings, image } = req.body;
        
        try {
            const buffer = Buffer.from(image.replace(/^data:image\/\w+;base64,/, ''), 'base64');
            const base64CroppedImage = await ImageService.processImage(buffer, cropSettings);
            
            const SolvingService = AIServiceFactory.getSolvingService();
            const answer = await SolvingService.solveProblem(base64CroppedImage, true);
            
            res.json({ answer });
        } catch (error) {
            console.error('Solving Error:', error);
            res.status(500).send('An error occurred while solving with image.');
        }
    }
}

module.exports = ImageController;