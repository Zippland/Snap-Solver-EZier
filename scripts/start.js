// scripts/start.js
const App = require('../app');
const { spawn } = require('child_process');
const path = require('path');

function startScreenshotService() {
    const pythonPath = process.platform === 'win32' ? 'pythonw.exe' : 'python';
    const snapPath = path.join(__dirname, '..', 'snap.py');
    
    const pythonProcess = spawn(pythonPath, [snapPath], {
        detached: false,
        stdio: 'ignore'
    });

    pythonProcess.on('error', (err) => {
        console.error('Screenshot service error:', err);
    });

    process.on('exit', () => {
        pythonProcess.kill();
    });
}

// 启动 Python 截图服务
startScreenshotService();

// 启动主服务
const app = new App();
app.start();