require('dotenv').config();

const config = {
    host: process.env.HOST || '0.0.0.0',
    port: process.env.PORT || 3000,
    allowedIPs: process.env.ALLOWED_IPS ? process.env.ALLOWED_IPS.split(',') : [],
    proxy: {
        enabled: process.env.USE_PROXY === 'true',
        host: process.env.PROXY_HOST || '127.0.0.1',
        port: parseInt(process.env.PROXY_PORT) || 4780,
        protocol: (process.env.PROXY_PROTOCOL || 'http').toLowerCase().trim()
    },
    openai: {
        apiKey: process.env.OPENAI_API_KEY,
        extractionModel: 'gpt-4o-mini',
        solvingModel: 'gpt-4o-2024-08-06',
        maxTokens: 1000
    },
    imageProcessing: {
        maxFileSize: '100mb'
    }
};

// 在启动时打印代理配置
if (config.proxy.enabled) {
    console.log('Proxy configuration:', {
        protocol: config.proxy.protocol,
        host: config.proxy.host,
        port: config.proxy.port
    });
}

module.exports = config;