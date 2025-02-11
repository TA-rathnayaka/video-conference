import { useEffect, useRef } from "react";
import { useWebRTC } from "../hooks/useWebRTC";

export const VideoCall = ({ roomId }) => {
  const localVideoRef = useRef();
  const remoteVideoRef = useRef();
  const { localStream, remoteStream } = useWebRTC(roomId);

  useEffect(() => {
    if (localStream) {
      localVideoRef.current.srcObject = localStream;
    }
  }, [localStream]);

  useEffect(() => {
    if (remoteStream) {
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
