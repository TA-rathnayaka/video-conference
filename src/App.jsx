import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { Home } from "./components/Home";
import { VideoCall } from "./components/VideoCall";
import { Auth } from "./components/Auth";
import "./index.css";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/call/:roomId" element={<VideoCall />} />
          <Route path="/login" element={<Auth />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
