export default async function handler(req, res) {
  // 1. Only allow POST requests from your frontend
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { text, target_lang } = req.body;
  const authKey = process.env.DEEPL_API_KEY; 

  // 2. Check if the API key is actually loaded in Vercel
  if (!authKey) {
    return res.status(500).json({ error: 'DeepL API key not configured in Vercel settings' });
  }

  try {
    const response = await fetch('https://api-free.deepl.com/v2/translate', {
      method: 'POST',
      headers: {
        'Authorization': `DeepL-Auth-Key ${authKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: [text],
        target_lang: target_lang || 'EN',
      }),
    });

    const data = await response.json();

    if (data.translations && data.translations.length > 0) {
      res.status(200).json({ translation: data.translations[0].text });
    } else {
      console.error('DeepL Error Response:', data);
      res.status(500).json({ error: 'DeepL returned an empty response' });
    }
  } catch (error) {
    console.error('Server Error:', error);
    res.status(500).json({ error: 'Internal Server Error during translation' });
  }
}
