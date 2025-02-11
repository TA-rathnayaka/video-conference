// src/components/Auth.jsx
import React from "react";
import { auth, provider } from "../services/firebase";
import { signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { createUser } from "../services/users";

export const Auth = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const signIn = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      await createUser(result.user);
      navigate("/");
    } catch (error) {
      console.error("Error signing in", error);
    }
  };

  return (
    <div className="auth-container">
      {user ? (
        <p>You are signed in as {user.displayName}</p>
      ) : (
        <button onClick={signIn}>Sign in with Google</button>
      )}
    </div>
  );
};
