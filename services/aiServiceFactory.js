// services\aiServiceFactory.js
const OpenAIService = require('./openaiService');
const ClaudeService = require('./claudeService');
const config = require('../config');

class AIServiceFactory {
    static getExtractionService() {
        switch(config.aiSelection.extraction.toLowerCase()) {
            case 'claude':
                return ClaudeService;
            case 'openai':
            default:
                return OpenAIService;
        }
    }

    static getSolvingService() {
        switch(config.aiSelection.solving.toLowerCase()) {
            case 'claude':
                return ClaudeService;
            case 'openai':
            default:
                return OpenAIService;
        }
    }
}

module.exports = AIServiceFactory;