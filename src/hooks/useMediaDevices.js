import { useState, useCallback } from "react";

export const useMediaDevices = () => {
  const [mediaStream, setMediaStream] = useState(null);

  const getMedia = useCallback(async (constraints) => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      setMediaStream(stream);
      return stream;
    } catch (err) {
      console.error("Error accessing media devices:", err);
    }
  }, []);

  const stopMedia = useCallback(() => {
    mediaStream?.getTracks().forEach((track) => track.stop());
    setMediaStream(null);
  }, [mediaStream]);

  return { getMedia, stopMedia, mediaStream };
};
