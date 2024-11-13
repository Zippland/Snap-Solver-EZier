const axios = require('axios');
const config = require('../config');
const tunnel = require('tunnel');

class ClaudeService {
    static createAxiosInstance() {
        const axiosConfig = {
            headers: {
                'x-api-key': config.claude.apiKey,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
        };

        if (config.proxy.enabled) {
            const tunnelConfig = {
                proxy: {
                    host: config.proxy.host,
                    port: config.proxy.port
                }
            };

            if (config.proxy.protocol === 'https') {
                axiosConfig.httpsAgent = tunnel.httpsOverHttps(tunnelConfig);
            } else {
                axiosConfig.httpsAgent = tunnel.httpsOverHttp(tunnelConfig);
            }
        }

        return axios.create(axiosConfig);
    }

    static async extractText(base64Image) {
        try {
            const client = this.createAxiosInstance();
            
            const response = await client.post('https://api.anthropic.com/v1/messages', {
                model: config.claude.model,
                messages: [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'image',
                                source: {
                                    type: 'base64',
                                    media_type: 'image/png',
                                    data: base64Image
                                }
                            },
                            {
                                type: 'text',
                                text: '请按格式提取这张图片中的所有内容，一字不落。'
                            }
                        ]
                    }
                ],
                max_tokens: config.claude.maxTokens
            });

            if (!response.data?.content?.[0]?.text) {
                throw new Error('Invalid response from Claude API');
            }

            return response.data.content[0].text.trim();
        } catch (error) {
            console.error('Claude Text Extraction Error:', {
                message: error.message,
                response: error.response?.data,
                status: error.response?.status
            });
            throw new Error('Failed to extract text using Claude');
        }
    }

    static async solveProblem(content, isImage = false) {
        try {
            const client = this.createAxiosInstance();
            const prompt = config.solving.defaultPrompt;
            
            const messages = isImage ? [
                {
                    role: 'user',
                    content: [
                        {
                            type: 'image',
                            source: {
                                type: 'base64',
                                media_type: 'image/png',
                                data: content
                            }
                        },
                        {
                            type: 'text',
                            text: `${prompt}\n\n请解答图中的题目。`
                        }
                    ]
                }
            ] : [
                {
                    role: 'user',
                    content: `${prompt}\n\n请解答以下题目：\n\n${content}`
                }
            ];
    
            const response = await client.post('https://api.anthropic.com/v1/messages', {
                model: config.claude.model,
                messages: messages,
                max_tokens: config.claude.maxTokens
            });

            if (!response.data?.content?.[0]?.text) {
                throw new Error('Invalid response from Claude API');
            }

            return response.data.content[0].text.trim();
        } catch (error) {
            console.error('Claude Problem Solving Error:', {
                message: error.message,
                response: error.response?.data,
                status: error.response?.status
            });
            throw new Error('Failed to solve problem using Claude');
        }
    }
}

module.exports = ClaudeService;