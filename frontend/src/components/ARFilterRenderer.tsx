import { useRef, useEffect } from 'react'
import * as THREE from 'three'
import * as faceLandmarksDetection from '@tensorflow-models/face-landmarks-detection'

interface ARFilterRendererProps {
  videoElement: HTMLVideoElement;
}

export const ARFilterRenderer = ({ videoElement }: ARFilterRendererProps) => {
  const canvasRef = useRef(null)
  const modelRef = useRef<faceLandmarksDetection.FaceLandmarksDetector | null>(null)
  const sceneRef = useRef<THREE.Scene | null>(null)
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null)
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null)

  useEffect(() => {
    const initThreeJS = async () => {
      modelRef.current = await faceLandmarksDetection.createDetector(
        faceLandmarksDetection.SupportedModels.MediaPipeFaceMesh
      )

      // WebGL setup
      if (canvasRef.current) {
        rendererRef.current = new THREE.WebGLRenderer({
          canvas: canvasRef.current,
          alpha: true,
          antialias: true
        })
      }
      
      sceneRef.current = new THREE.Scene()
      cameraRef.current = new THREE.PerspectiveCamera(
        75,
        videoElement.videoWidth / videoElement.videoHeight,
        0.1,
        1000
      )
      
      // Add 3D objects
      const addFilterObject = () => {
        const geometry = new THREE.SphereGeometry(0.1)
        const material = new THREE.MeshBasicMaterial({ color: 0xff0000 })
        const mesh = new THREE.Mesh(geometry, material)
        if (sceneRef.current) {
          sceneRef.current.add(mesh)
        }
        return mesh
      }
      
      const filterObject = addFilterObject()
      
      const animate = async () => {
        if (modelRef.current) {
          const faces = await modelRef.current.estimateFaces(videoElement)
          faces.forEach(face => {
            const keypoints = face.keypoints;
            const nose = keypoints.find(point => point.name === 'noseTip');
            if (nose) {
              if (nose.x !== undefined && nose.y !== undefined && nose.z !== undefined) {
                filterObject.position.set(nose.x, nose.y, nose.z);
              }
            }
          })
        }
        
        if (rendererRef.current && sceneRef.current && cameraRef.current) {
          rendererRef.current.render(sceneRef.current, cameraRef.current)
        }
        requestAnimationFrame(animate)
      }
      
      animate()
    }

    videoElement.addEventListener('loadedmetadata', initThreeJS)
    return () => videoElement.removeEventListener('loadedmetadata', initThreeJS)
  }, [videoElement])

  return <canvas ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0 }} />
}