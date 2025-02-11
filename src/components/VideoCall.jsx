// src/components/VideoCall.jsx
import React, { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { useMediaDevices } from "../hooks/useMediaDevices";
import { useWebRTC } from "../hooks/useWebRTC";

export const VideoCall = () => {
  const { roomId } = useParams();
  const localVideoRef = useRef();
  const remoteVideoRef = useRef();
  const { getMedia } = useMediaDevices();
  const [localStream, setLocalStream] = useState(null);

  // Get the local media stream.
  useEffect(() => {
    (async () => {
      const stream = await getMedia({ video: true, audio: true });
      setLocalStream(stream);
      if (localVideoRef.current) {
        localVideoRef.current.srcObject = stream;
      }
    })();
  }, [getMedia]);

  // Initialize WebRTC using the local stream.
  const { remoteStream } = useWebRTC(roomId, localStream);

  useEffect(() => {
    if (remoteVideoRef.current && remoteStream) {
      remoteVideoRef.current.srcObject = remoteStream;
    }
  }, [remoteStream]);

  return (
    <div className="video-container">
      <video ref={localVideoRef} autoPlay muted className="local-video" />
      <video ref={remoteVideoRef} autoPlay className="remote-video" />
    </div>
  );
};
