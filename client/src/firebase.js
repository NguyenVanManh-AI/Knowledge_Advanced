import { initializeApp } from 'firebase/app';
import { getFirestore, collection } from 'firebase/firestore';

export const firebaseApp = initializeApp({
  apiKey: "AIzaSyA6yJWsqmCtnbJJzBWLrU12oz67XyyCbTI",
  authDomain: "webhoc-90c3d.firebaseapp.com",
  projectId: "webhoc-90c3d",
  storageBucket: "webhoc-90c3d.appspot.com",
  messagingSenderId: "342569386423",
  appId: "1:342569386423:web:865e3f41785db3b4a3e832",
  measurementId: "G-B68475R7Y2"
});

export const db = getFirestore(firebaseApp);
export const messagesRef = collection(db, 'messages');
export const notifiesRef = collection(db, 'notifies');