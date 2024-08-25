import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/global.css";
import { RouterProvider } from "react-router-dom";
import { router } from "./routes";
import { QueryClient, QueryClientProvider } from "react-query";
import AuthChecker from "./layout/auth-checker";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <RouterProvider router={router} />
    <AuthChecker />
  </QueryClientProvider>
);

const root = ReactDOM.createRoot(document.getElementById("quiz-app-root"));
root.render(<App />);
