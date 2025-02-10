import { useRef, useEffect, useState } from 'react'
import { useWebRTC } from '../hooks/useWebRTC'
import { ARFilterRenderer } from './ARFilterRenderer'

interface VideoConferenceProps {
  roomId: string;
}

export const VideoConference = ({ roomId }: VideoConferenceProps) => {
  const localVideoRef = useRef<HTMLVideoElement>(null)
  const [remoteStreams, setRemoteStreams] = useState([])
  const { peers, localStream }: { peers: Map<string, any>, localStream: MediaStream } = useWebRTC(roomId)

  useEffect(() => {
    if (localStream && localVideoRef.current) {
      localVideoRef.current.srcObject = localStream
    }
  }, [localStream])

  return (
    <div className="conference-container">
      <div className="local-video">
        <video ref={localVideoRef} autoPlay muted />
        {localVideoRef.current && <ARFilterRenderer videoElement={localVideoRef.current} />}
      </div>
      
      {Array.from(peers).map(([peerId, peer]) => (
        <RemoteVideo key={peerId} peer={peer} />
      ))}
    </div>
  )
}

interface RemoteVideoProps {
  peer: any;
}

const RemoteVideo = ({ peer }: RemoteVideoProps) => {
  const videoRef = useRef<HTMLVideoElement>(null)
  
  useEffect(() => {
    const trackHandler = (event: RTCTrackEvent) => {
      if (videoRef.current && !videoRef.current.srcObject) {
        videoRef.current.srcObject = event.streams[0]
      }
    }
    
    peer.addEventListener('track', trackHandler)
    return () => peer.removeEventListener('track', trackHandler)
  }, [peer])

  return <video ref={videoRef} autoPlay />
}