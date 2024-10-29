// app.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const config = require('./config');
const routes = require('./routes');
const ipFilter = require('./middleware/ipFilter');
const os = require('os');

class App {
    constructor() {
        this.app = express();
        this.server = http.createServer(this.app);
        this.io = new Server(this.server, {
            cors: {
                origin: true,
                credentials: true
            }
        });
        this.setupMiddleware();
        this.setupRoutes();
        this.setupSocketHandlers();
    }

    setupMiddleware() {
        this.app.use(express.static(path.join(__dirname, 'public')));
        this.app.use(express.json({ limit: config.imageProcessing.maxFileSize }));
        this.app.use(ipFilter);
    }

    setupRoutes() {
        this.app.use('/', routes(this.io));
    }

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log('Client connected:', socket.handshake.address);
            
            socket.on('disconnect', () => {
                console.log('Client disconnected:', socket.handshake.address);
            });
        });
    }

    getLocalIPs() {
        const interfaces = os.networkInterfaces();
        const addresses = [];
        
        for (const interfaceName in interfaces) {
            const networkInterface = interfaces[interfaceName];
            for (const addr of networkInterface) {
                if (addr.family === 'IPv4' && !addr.internal) {
                    addresses.push(addr.address);
                }
            }
        }
        
        return addresses;
    }

    start() {
        this.server.listen(config.port, config.host, () => {
            console.log(`Server running on port ${config.port}`);
            console.log('Available on:');
            this.getLocalIPs().forEach(ip => {
                console.log(`  http://${ip}:${config.port}`);
            });
        });
    }
}

module.exports = App;