import { useEffect, useRef, useState } from 'react'
import sodium from 'libsodium-wrappers'

export const useWebRTC = (roomId) => {
  const [peers, setPeers] = useState(new Map())
  const localStreamRef = useRef(null)
  const socketRef = useRef(null)
  const encryptionKeyRef = useRef(null)

  const setupEncryption = async () => {
    await sodium.ready
    encryptionKeyRef.current = sodium.crypto_secretstream_keygen()
  }

  const createPeerConnection = async (userId) => {
    const peer = new RTCPeerConnection({
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        // Add TURN server config here
      ]
    })

    // Add encryption to data channels
    const createEncryptedDataChannel = (label, config) => {
      const channel = peer.createDataChannel(label, config)
      
      channel.addEventListener('message', async (event) => {
        const decrypted = sodium.crypto_secretbox_open_easy(
          new Uint8Array(event.data),
          sodium.from_hex(peer.nonce),
          encryptionKeyRef.current
        )
        // Handle decrypted message
      })

      return new Proxy(channel, {
        get(target, prop) {
          if (prop === 'send') {
            return async (data) => {
              const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES)
              const encrypted = sodium.crypto_secretbox_easy(
                sodium.from_string(data),
                nonce,
                encryptionKeyRef.current
              )
              target.send(encrypted)
              peer.nonce = sodium.to_hex(nonce)
            }
          }
          return target[prop]
        }
      })
    }

    return peer
  }

  useEffect(() => {
    (async () => {
      await setupEncryption()
      // WebSocket and media setup
    })()
  }, [roomId])

  return { peers, localStream: localStreamRef.current }
}