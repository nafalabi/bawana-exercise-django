import React from 'react';
import ReactDOM from 'react-dom/client';
import "./styles/global.css"
import { RouterProvider } from 'react-router-dom';
import { router } from './routes';

const App = () => (
  <RouterProvider router={router} />
);

const root = ReactDOM.createRoot(document.getElementById('quiz-app-root'))
root.render(<App />)
