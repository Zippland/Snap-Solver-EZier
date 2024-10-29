require('dotenv').config();

const config = {
    // 允许配置 host，默认监听所有网卡
    host: process.env.HOST || '0.0.0.0',
    port: process.env.PORT || 3000,
    // 可以配置允许访问的 IP 范围
    allowedIPs: process.env.ALLOWED_IPS ? process.env.ALLOWED_IPS.split(',') : [],
    // GPT模型相关配置
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

module.exports = config;