import { useEffect, useState } from "react";
import { db } from "../services/firebase"; // Ensure you export your Firestore db instance correctly
import { collection, doc, onSnapshot, addDoc } from "firebase/firestore";

export const useWebRTC = (roomId) => {
  const [localStream, setLocalStream] = useState(null);
  const [remoteStream, setRemoteStream] = useState(null);
  const [pc, setPc] = useState(null);

  useEffect(() => {
    if (!roomId) return;

    const rtcPeerConnection = new RTCPeerConnection({
      iceServers: [
        { urls: "stun:stun.l.google.com:19302" },
        { urls: "stun:stun.l.google.com:5349" },
      ],
      iceCandidatePoolSize: 10,
    });
    setPc(rtcPeerConnection);

    // Create a MediaStream for remote tracks and store it in state
    const remoteMediaStream = new MediaStream();
    setRemoteStream(remoteMediaStream);

    // When a remote track arrives, add it to the remoteMediaStream.
    rtcPeerConnection.ontrack = (event) => {
      event.streams[0].getTracks().forEach((track) => {
        remoteMediaStream.addTrack(track);
      });
    };

    // Get a reference to the Firestore room document and its signals subcollection.
    const roomRef = doc(db, "rooms", roomId);
    const signalsRef = collection(roomRef, "signals");

    // When ICE candidates are generated locally, send them to Firestore.
    rtcPeerConnection.onicecandidate = async (event) => {
      if (event.candidate) {
        console.log("New local ICE candidate:", event.candidate);
        try {
          await addDoc(signalsRef, {
            type: "candidate",
            candidate: event.candidate.toJSON(),
          });
        } catch (error) {
          console.error("Error sending ICE candidate:", error);
        }
      }
    };

    // Capture the local media stream (video and audio) and add its tracks to the RTCPeerConnection.
    const getLocalStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true,
        });
        setLocalStream(stream);
        stream.getTracks().forEach((track) => {
          rtcPeerConnection.addTrack(track, stream);
        });
      } catch (error) {
        console.error("Error accessing local media:", error);
      }
    };
    getLocalStream();

    // Listen for signals from Firestore and handle them accordingly.
    const unsubscribe = onSnapshot(signalsRef, async (snapshot) => {
      // Iterate over document changes
      for (const change of snapshot.docChanges()) {
        if (change.type === "added") {
          const data = change.doc.data();
          console.log("Received signal:", data);

          if (data.type === "offer") {
            // When an offer is received: set it as remote description, create an answer, and send the answer.
            if (!rtcPeerConnection.currentRemoteDescription) {
              try {
                await rtcPeerConnection.setRemoteDescription(
                  new RTCSessionDescription(data.sdp)
                );
                const answer = await rtcPeerConnection.createAnswer();
                await rtcPeerConnection.setLocalDescription(answer);
                await addDoc(signalsRef, {
                  type: "answer",
                  sdp: rtcPeerConnection.localDescription.toJSON(),
                });
              } catch (error) {
                console.error("Error handling received offer:", error);
              }
            }
          } else if (data.type === "answer") {
            // When an answer is received, set it as the remote description.
            if (!rtcPeerConnection.currentRemoteDescription) {
              try {
                await rtcPeerConnection.setRemoteDescription(
                  new RTCSessionDescription(data.sdp)
                );
              } catch (error) {
                console.error("Error handling received answer:", error);
              }
            }
          } else if (data.type === "candidate") {
            // When a remote ICE candidate is received, add it to the connection.
            try {
              await rtcPeerConnection.addIceCandidate(
                new RTCIceCandidate(data.candidate)
              );
            } catch (error) {
              console.error("Error adding remote ICE candidate:", error);
            }
          }
        }
      }
    });

    // Cleanup: close the peer connection and unsubscribe from Firestore signals.
    return () => {
      rtcPeerConnection.close();
      unsubscribe();
    };
  }, [roomId]);

  return { localStream, remoteStream, pc };
};
