require('dotenv').config();

const config = {
    host: process.env.HOST || '0.0.0.0',
    port: process.env.PORT || 3000,
    allowedIPs: process.env.ALLOWED_IPS ? process.env.ALLOWED_IPS.split(',') : [],
    
    // OpenAI Configuration
    openai: {
        apiKey: process.env.OPENAI_API_KEY,
        model: 'gpt-4o-2024-08-06',
        maxTokens: 1000
    },
    
    // Claude Configuration
    claude: {
        apiKey: process.env.CLAUDE_API_KEY,
        model: 'claude-3-5-sonnet-20241022',
        maxTokens: 1000
    },
    
    // AI Service Selection
    aiSelection: {
        extraction: process.env.EXTRACTION_AI || 'openai',
        solving: process.env.SOLVING_AI || 'claude'
    },
    
    // Proxy Configuration
    proxy: {
        enabled: process.env.USE_PROXY === 'true',
        host: process.env.PROXY_HOST || '127.0.0.1',
        port: parseInt(process.env.PROXY_PORT) || 4780,
        protocol: (process.env.PROXY_PROTOCOL || 'http').toLowerCase().trim()
    },

    // 添加解题提示配置
    solving: {
        defaultPrompt: process.env.SOLVING_PROMPT || '请详细分析这道题目并给出完整的解答思路和步骤。如果是选择题，请分析每个选项并说明选择的理由。'
    },
    
    imageProcessing: {
        maxFileSize: '100mb'
    }
};

// Helper function to get model based on service
config.getModel = function(service) {
    return service === 'openai' ? this.openai.model : this.claude.model;
};

if (config.proxy.enabled) {
    console.log('Proxy configuration:', {
        protocol: config.proxy.protocol,
        host: config.proxy.host,
        port: config.proxy.port
    });
}

module.exports = config;