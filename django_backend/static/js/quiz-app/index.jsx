import React from 'react';
import ReactDOM from 'react-dom/client';
import "./styles/global.css"
import { Button } from './components/ui/button';
import { Card } from './components/ui/card';

const App = () => (
  <div>
    <h1>Hello, React!</h1>
    <Button>Button</Button>
  </div>
);

const root = ReactDOM.createRoot(document.getElementById('quiz-app-root'))
root.render(<App />)
