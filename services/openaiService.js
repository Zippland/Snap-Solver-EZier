const axios = require('axios');
const config = require('../config');
const tunnel = require('tunnel');

class OpenAIService {
    static createAxiosInstance() {
        const axiosConfig = {
            headers: {
                'Authorization': `Bearer ${config.openai.apiKey}`,
                'Content-Type': 'application/json'
            }
        };

        if (config.proxy.enabled) {
            const tunnelConfig = {
                proxy: {
                    host: config.proxy.host,
                    port: config.proxy.port
                }
            };

            // 创建代理agent
            if (config.proxy.protocol === 'https') {
                axiosConfig.httpsAgent = tunnel.httpsOverHttps(tunnelConfig);
            } else {
                axiosConfig.httpsAgent = tunnel.httpsOverHttp(tunnelConfig);
            }

            console.log('Proxy configuration:', {
                protocol: config.proxy.protocol,
                host: config.proxy.host,
                port: config.proxy.port
            });
        }

        return axios.create(axiosConfig);
    }

    static async extractText(base64Image) {
        try {
            const client = this.createAxiosInstance();
            
            const response = await client.post('https://api.openai.com/v1/chat/completions', {
                model: config.openai.extractionModel,
                messages: [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'image_url',
                                image_url: {
                                    url: `data:image/png;base64,${base64Image}`
                                }
                            },
                            {
                                type: 'text',
                                text: '请按格式提取这张图片中的所有内容，一字不落。'
                            }
                        ]
                    }
                ],
                max_tokens: config.openai.maxTokens
            });

            if (!response.data?.choices?.[0]?.message?.content) {
                throw new Error('Invalid response from OpenAI API');
            }

            return response.data.choices[0].message.content.trim();
        } catch (error) {
            console.error('Text Extraction Error:', {
                message: error.message,
                response: error.response?.data,
                status: error.response?.status
            });
            throw new Error('Failed to extract text from image');
        }
    }

    static async solveProblem(content, isImage = false) {
        try {
            const client = this.createAxiosInstance();
            
            const requestBody = {
                model: config.openai.solvingModel,
                messages: isImage ? [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'image_url',
                                image_url: {
                                    url: `data:image/png;base64,${content}`
                                }
                            },
                            {
                                type: 'text',
                                text: '请解答图中的题目。如果是选择题，请先仔细分析题目中的每一个选项，然后给我正确答案。'
                            }
                        ]
                    }
                ] : [
                    {
                        role: 'user',
                        content: `请解答以下题目。如果是选择题，请先仔细分析题目中的每一个选项，然后给我正确答案。\n\n${content}`
                    }
                ],
                max_tokens: config.openai.maxTokens
            };

            const response = await client.post(
                'https://api.openai.com/v1/chat/completions',
                requestBody
            );

            if (!response.data?.choices?.[0]?.message?.content) {
                throw new Error('Invalid response from OpenAI API');
            }

            return response.data.choices[0].message.content.trim();
        } catch (error) {
            console.error('Problem Solving Error:', {
                message: error.message,
                response: error.response?.data,
                status: error.response?.status
            });
            throw new Error('Failed to solve the problem');
        }
    }
}

module.exports = OpenAIService;