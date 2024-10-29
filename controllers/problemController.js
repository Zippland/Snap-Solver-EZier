const OpenAIService = require('../services/openaiService');

class ProblemController {
    solveProblem = async (req, res) => {
        const { extractedText } = req.body;
        
        try {
            const answer = await OpenAIService.solveProblem(extractedText);
            res.json({ answer });
        } catch (error) {
            console.error('Solving Error:', error);
            res.status(500).send('An error occurred while solving the problem.');
        }
    }
}

module.exports = ProblemController;