const config = require('../config');

const ipFilter = (req, res, next) => {
    const clientIP = req.ip || req.connection.remoteAddress;
    
    // 如果没有配置 allowedIPs，允许所有局域网 IP
    if (!config.allowedIPs.length) {
        // 检查是否是局域网 IP
        if (
            clientIP === '127.0.0.1' || 
            clientIP === '::1' ||
            clientIP.startsWith('192.168.') || 
            clientIP.startsWith('10.') || 
            clientIP.startsWith('172.16.') ||
            clientIP.startsWith('172.17.') ||
            clientIP.startsWith('172.18.') ||
            clientIP.startsWith('172.19.') ||
            clientIP.startsWith('172.20.') ||
            clientIP.startsWith('172.21.') ||
            clientIP.startsWith('172.22.') ||
            clientIP.startsWith('172.23.') ||
            clientIP.startsWith('172.24.') ||
            clientIP.startsWith('172.25.') ||
            clientIP.startsWith('172.26.') ||
            clientIP.startsWith('172.27.') ||
            clientIP.startsWith('172.28.') ||
            clientIP.startsWith('172.29.') ||
            clientIP.startsWith('172.30.') ||
            clientIP.startsWith('172.31.')
        ) {
            return next();
        }
    } else if (config.allowedIPs.includes(clientIP)) {
        return next();
    }
    
    res.status(403).send('Access denied. Your IP is not allowed.');
};

module.exports = ipFilter;