// services\imageService.js
const sharp = require('sharp');

class ImageService {
    static async processImage(imageBuffer, cropSettings) {
        try {
            let img = sharp(imageBuffer);
            const metadata = await img.metadata();
            
            const { x, y, width, height } = this.validateCropSettings(
                cropSettings,
                metadata.width,
                metadata.height
            );

            img = img.extract({ left: x, top: y, width, height });
            const processedBuffer = await img.png().toBuffer();
            return processedBuffer.toString('base64');
        } catch (error) {
            console.error('Image Processing Error:', error);
            throw new Error('Failed to process image');
        }
    }

    static validateCropSettings(settings, imgWidth, imgHeight) {
        try {
            const x = Math.max(0, Math.min(Math.round(settings.x), imgWidth));
            const y = Math.max(0, Math.min(Math.round(settings.y), imgHeight));
            const width = Math.max(1, Math.min(Math.round(settings.width), imgWidth - x));
            const height = Math.max(1, Math.min(Math.round(settings.height), imgHeight - y));

            return { x, y, width, height };
        } catch (error) {
            console.error('Validation Error:', error);
            throw new Error('Invalid crop settings');
        }
    }
}

module.exports = ImageService;