// src/services/users.js
import { db, auth } from "./firebase";
import { doc, setDoc, getDoc } from "firebase/firestore";

export const createUser = async (user) => {
  const userRef = doc(db, "users", user.uid);
  await setDoc(
    userRef,
    {
      displayName: user.displayName,
      email: user.email,
      photoURL: user.photoURL,
    },
    { merge: true }
  );
};

export const getUser = async (uid) => {
  const userRef = doc(db, "users", uid);
  const userSnap = await getDoc(userRef);
  return userSnap.exists() ? userSnap.data() : null;
};
