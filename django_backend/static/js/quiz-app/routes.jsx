import React from "react";
import { createHashRouter, Outlet } from "react-router-dom";
import { Card } from "./components/ui/card";

const BaseLayout = React.lazy(() => import("./layout/base"));
const Mainpage = React.lazy(() => import("./pages/Main"));
const QuestionsPage = React.lazy(() => import("./pages/Questions"));
const QuizPage = React.lazy(() => import("./pages/Quiz"));
const SessionPage = React.lazy(() => import("./pages/Session"));

const LazyLoad = ({ Component, fallback, props }) => {
  return (
    <React.Suspense fallback={fallback ?? <div>Loading...</div>}>
      <Component {...props} />
    </React.Suspense>
  );
};

export const router = createHashRouter([
  {
    path: "/",
    element: (
      <LazyLoad Component={BaseLayout} props={{ content: <Outlet /> }} />
    ),
    children: [
      {
        index: true,
        element: <LazyLoad Component={Mainpage} />,
      },
      {
        path: "/quiz",
        element: <LazyLoad Component={QuizPage} />,
      },
      {
        path: "/questions",
        element: <LazyLoad Component={QuestionsPage} />,
      },
      {
        path: "/sessions",
        element: <LazyLoad Component={SessionPage} />,
      },
      // {
      //   path: "/test",
      //   element: <LazyLoad Component={base} />,
      // },
    ],
  },
]);
