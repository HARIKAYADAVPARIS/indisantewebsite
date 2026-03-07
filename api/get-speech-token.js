export default async function handler(req, res) {
    // These match the names you will set in Vercel Environment Variables
    const speechKey = process.env.AZURE_SPEECH_KEY;
    const speechRegion = process.env.AZURE_SPEECH_REGION; 

    const tokenUrl = `https://${speechRegion}.api.cognitive.microsoft.com/sts/v1.0/issueToken`;

    try {
        const response = await fetch(tokenUrl, {
            method: 'POST',
            headers: {
                'Ocp-Apim-Subscription-Key': speechKey,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch token from Azure');
        }

        const token = await response.text();
        
        // This sends the temporary token back to your frontend securely
        res.status(200).json({ 
            token: token, 
            region: speechRegion 
        });
    } catch (error) {
        console.error('Azure Auth Error:', error);
        res.status(500).json({ error: 'Authentication failed' });
    }
}
