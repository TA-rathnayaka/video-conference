export class WebAuthnManager {
    static async register() {
      const challenge = crypto.getRandomValues(new Uint8Array(32))
      const userId = crypto.getRandomValues(new Uint8Array(16))
      
      const credential = await navigator.credentials.create({
        publicKey: {
          challenge,
          rp: { name: "SecureVideoConf" },
          user: {
            id: userId,
            name: "user@secureconf.com",
            displayName: "User"
          },
          pubKeyCredParams: [
            { type: "public-key", alg: -7 }, // ES256
            { type: "public-key", alg: -257 } // RS256
          ],
          authenticatorSelection: {
            userVerification: "preferred",
            requireResidentKey: true
          }
        }
      })
      
      localStorage.setItem('webauthn_credential', JSON.stringify({
        id: credential.id,
        rawId: Array.from(new Uint8Array(credential.rawId)),
        type: credential.type
      }))
      
      return credential
    }
  
    static async authenticate() {
      const storedCredential = JSON.parse(localStorage.getItem('webauthn_credential'))
      
      const credential = await navigator.credentials.get({
        publicKey: {
          challenge: crypto.getRandomValues(new Uint8Array(32)),
          allowCredentials: [{
            id: Uint8Array.from(storedCredential.rawId),
            type: 'public-key'
          }],
          userVerification: "preferred"
        }
      })
      
      return credential
    }
  }