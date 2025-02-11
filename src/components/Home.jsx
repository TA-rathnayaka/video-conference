import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export const Home = () => {
  const [roomId, setRoomId] = useState("");
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleJoin = (e) => {
    e.preventDefault();
    navigate(`/call/${roomId}`);
  };

  const handleLogin = () => {
    navigate("/login");
  };

  return (
    <div className="home-container">
      <h1>Video Conference</h1>
      {user ? (
        <form onSubmit={handleJoin}>
          <input
            type="text"
            placeholder="Enter Room ID"
            value={roomId}
            onChange={(e) => setRoomId(e.target.value)}
          />
          <button type="submit">Join Call</button>
        </form>
      ) : (
        <div>
          <p>Please sign in to start a call</p>
          <button onClick={handleLogin}>Login</button>
        </div>
      )}
    </div>
  );
};
