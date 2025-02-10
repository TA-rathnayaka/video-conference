import express from 'express'
import { WebSocketServer } from 'ws'
import { createServer } from 'http'

const app = express()
const server = createServer(app)
const wss = new WebSocketServer({ server })

const rooms = new Map()

wss.on('connection', (ws, req) => {
  const roomId = new URL(req.url, `ws://${req.headers.host}`).searchParams.get('room')
  
  if (!rooms.has(roomId)) {
    rooms.set(roomId, new Set())
  }
  
  const room = rooms.get(roomId)
  room.add(ws)
  
  ws.on('message', (message) => {
    room.forEach(client => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(message)
      }
    })
  })

  ws.on('close', () => {
    room.delete(ws)
    if (room.size === 0) rooms.delete(roomId)
  })
})

server.listen(3001, () => {
  console.log('Signaling server running on ws://localhost:3001')
})