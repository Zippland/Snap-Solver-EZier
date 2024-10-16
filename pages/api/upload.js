import formidable from 'formidable';
import openai from 'openai';
import fs from 'fs';

export const config = {
  api: {
    bodyParser: false,  // 禁用 bodyParser 以处理文件上传
  },
};

const handler = async (req, res) => {
  if (req.method === 'POST') {
    const form = formidable({ multiples: true });  // 使用新版 formidable

    form.parse(req, async (err, fields, files) => {
      if (err) {
        console.error('文件上传失败:', err);  // 添加错误日志
        return res.status(500).json({ error: 'File upload failed' });
      }

      // 检查 files 对象是否存在，并获取文件路径
      const uploadedFile = files.file;
      if (!uploadedFile) {
        return res.status(400).json({ error: 'No file uploaded' });
      }

      const filePath = uploadedFile.filepath || uploadedFile.path;  // 兼容不同版本的 formidable

      if (!filePath) {
        return res.status(500).json({ error: 'Failed to retrieve file path' });
      }

      // 调用 OpenAI GPT-4 进行图片分析
      const apiKey = process.env.OPENAI_API_KEY;
      openai.apiKey = apiKey;

      const imageStream = fs.createReadStream(filePath);  // 创建文件读取流

      try {
        const response = await openai.createImage({
          model: "gpt-4o-2024-08-06",
          file: imageStream,
          prompt: "请分析并解决这张图片中的问题，用中文回答。",
        });

        const gptAnswer = response.data;  // GPT 的中文解答

        // 将 GPT 的解答发送回前端
        res.status(200).json({ answer: gptAnswer });
      } catch (error) {
        console.error('Error with GPT-4:', error);
        res.status(500).json({ error: 'Error with GPT-4 processing' });
      }
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
};

export default handler;
