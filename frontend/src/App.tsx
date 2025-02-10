import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { VideoConference } from './components/VideoConference';
import './App.css';

function App() {
  const [roomId, setRoomId] = useState('');

  const handleJoinRoom = () => {
    if (roomId.trim()) {
      window.location.href = `/room/${roomId}`;
    }
  };

  return (
    <Router>
      <div className="app-container">
        <h1>Secure Video Conferencing</h1>
        <Routes>
          <Route
            path="/"
            element={
              <div className="join-room-container">
                <input
                  type="text"
                  placeholder="Enter Room ID"
                  value={roomId}
                  onChange={(e) => setRoomId(e.target.value)}
                />
                <button onClick={handleJoinRoom}>Join Room</button>
              </div>
            }
          />
          <Route
            path="/room/:roomId"
            element={<VideoConference roomId={roomId} />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;