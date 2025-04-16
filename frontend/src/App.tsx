import React, { useState } from 'react';
import axios from './api';

const App = () => {
  const [video, setVideo] = useState<File | null>(null);
  const [resultUrl, setResultUrl] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!video) return;

    const formData = new FormData();
    formData.append('file', video);

    const response = await axios.post('/upload/', formData, {
      responseType: 'blob'
    });

    const url = URL.createObjectURL(response.data);
    setResultUrl(url);
  };

  return (
    <div style={{ padding: 24 }}>
      <h1>Upload Your Volleyball Video</h1>
      <input type="file" accept="video/*" onChange={e => setVideo(e.target.files?.[0] || null)} />
      <button onClick={handleUpload}>Upload & Get Feedback</button>

      {resultUrl && (
        <video controls style={{ marginTop: 20 }} width="600" src={resultUrl}></video>
      )}
    </div>
  );
};

export default App;
