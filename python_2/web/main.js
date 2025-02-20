const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

const signalingServerUrl = 'ws://localhost:8765';
const signalingSocket = new WebSocket(signalingServerUrl);

let localStream;
let peerConnection;
const servers = {
    iceServers: [
        {
            urls: 'stun:stun.l.google.com:19302'
        }
    ]
};

// Get access to the user's webcam
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        localVideo.srcObject = stream;
        localStream = stream;
        initializePeerConnection();
    })
    .catch(error => {
        console.error('Error accessing media devices.', error);
    });

function initializePeerConnection() {
    peerConnection = new RTCPeerConnection(servers);
    
    // Add local stream to peer connection
    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    });

    // Handle remote stream
    peerConnection.ontrack = event => {
        remoteVideo.srcObject = event.streams[0];
    };

    // Handle ICE candidates
    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            signalingSocket.send(JSON.stringify({ type: 'candidate', candidate: event.candidate }));
        }
    };

    // Create an offer
    peerConnection.createOffer()
        .then(offer => peerConnection.setLocalDescription(offer))
        .then(() => {
            signalingSocket.send(JSON.stringify({ type: 'offer', offer: peerConnection.localDescription }));
        })
        .catch(error => {
            console.error('Error creating offer.', error);
        });
}

// Handle incoming messages from the signaling server
signalingSocket.onmessage = event => {
    const data = JSON.parse(event.data);

    switch (data.type) {
        case 'offer':
            peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer))
                .then(() => peerConnection.createAnswer())
                .then(answer => peerConnection.setLocalDescription(answer))
                .then(() => {
                    signalingSocket.send(JSON.stringify({ type: 'answer', answer: peerConnection.localDescription }));
                })
                .catch(error => {
                    console.error('Error handling offer.', error);
                });
            break;
        case 'answer':
            peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer))
                .catch(error => {
                    console.error('Error setting remote description.', error);
                });
            break;
        case 'candidate':
            peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate))
                .catch(error => {
                    console.error('Error adding received ICE candidate.', error);
                });
            break;
        default:
            console.error('Unknown message type:', data.type);
            break;
    }
};