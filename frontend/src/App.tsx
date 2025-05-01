import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);
  const [feedbackText, setFeedbackText] = useState<string | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [drawing, setDrawing] = useState(false);
  const [startPoint, setStartPoint] = useState<any>(null);
  const [box, setBox] = useState<{ x: number; y: number; w: number; h: number } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setVideoFile(file);
      setBox(null);
      setProcessedVideoUrl("");
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>) => {
    if (!drawing || !canvasRef.current || !startPoint) return;
  
    const rect = canvasRef.current.getBoundingClientRect();
    const ctx = canvasRef.current.getContext("2d");
    if (!ctx) return;
  
    const currentX = e.clientX - rect.left;
    const currentY = e.clientY - rect.top;
  
    // Redraw original frame
    if (videoRef.current) {
      ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  
    // Draw dynamic rectangle
    ctx.strokeStyle = "red";
    ctx.lineWidth = 2;
    ctx.strokeRect(
      startPoint.x,
      startPoint.y,
      currentX - startPoint.x,
      currentY - startPoint.y
    );
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>) => {
    if (!canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
  
    setStartPoint({ x, y });
    setDrawing(true);
  };
  
  const handleMouseUp = (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>) => {
    if (!drawing || !canvasRef.current || !startPoint) return;
  
    const rect = canvasRef.current.getBoundingClientRect();
    const endX = e.clientX - rect.left;
    const endY = e.clientY - rect.top;
  
    const x = Math.min(startPoint.x, endX);
    const y = Math.min(startPoint.y, endY);
    const w = Math.abs(endX - startPoint.x);
    const h = Math.abs(endY - startPoint.y);
  
    setBox({ x, y, w, h });
    setDrawing(false);
  
    // Final draw box
    const ctx = canvasRef.current.getContext("2d");
    if (ctx && videoRef.current) {
      ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
      ctx.strokeStyle = "red";
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y, w, h);
    }
  };

  const handleUpload = async () => {
    if (!videoFile || !box) return;

    const formData = new FormData();
    formData.append('file', videoFile);
    formData.append('bbox', JSON.stringify(box));

    const uploadRes = await axios.post('http://localhost:8000/upload/', formData, {
      responseType: 'blob',
    });

    const contentDisposition = uploadRes.headers['content-disposition'];
    let filename = 'default_filename';

    if (contentDisposition) {
      const matches = contentDisposition.match(/filename="(.+)"/);
      if (matches) {
        filename = matches[1];
      }
    }
    const videoBlob = new Blob([uploadRes.data], { type: 'video/mp4' });
    setProcessedVideoUrl(URL.createObjectURL(videoBlob));

    const feedbackRes = await axios.get('http://localhost:8000/feedback/', {
      params: { filename },
    });
    setFeedbackText(feedbackRes.data.feedback);
  };

  useEffect(() => {
    if (videoFile && videoRef.current) {
      const videoUrl = URL.createObjectURL(videoFile);
      const video = videoRef.current;
      video.src = videoUrl;
      video.load();
  
      video.onloadeddata = () => {
        // Ensure metadata is ready and seek to first frame
        video.currentTime = 0;
      };
  
      video.onseeked = () => {
        // Once seek is done, draw the first frame
        if (canvasRef.current && videoRef.current) {
          const canvas = canvasRef.current;
          const ctx = canvas.getContext("2d");
          if (ctx) {
            // Match canvas size to video size
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
  
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          }
        }
      };
    }
  }, [videoFile]);
  

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Upload Video</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <br />
      <video ref={videoRef} controls width={500} style={{ marginTop: '1rem' }} />
      <canvas
        ref={canvasRef}
        style={{ border: '1px solid black', marginTop: '1rem' }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      />
      <br />
      <button onClick={handleUpload} disabled={!videoFile || !box}>
        Upload & Process
      </button>

      {processedVideoUrl && (
        <div>
          <h3>Processed Video</h3>
          <video src={processedVideoUrl} controls width={500} />
        </div>
      )}

      {feedbackText && (
        <div>
          <h3>Feedback</h3>
          <pre>{feedbackText}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
