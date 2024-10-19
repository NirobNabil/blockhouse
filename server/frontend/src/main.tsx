import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ProfileForm from "./routes/backtest";
import Forecast from "./routes/forecast"
import PerformanceReport from "./routes/performance_report"

const router = createBrowserRouter([
  {
    path: "/backtest",
    element: <ProfileForm />,
  },
  {
    path: "/forecast",
    element: <Forecast />,
  },
  {
    path: "/performance_report",
    element: <PerformanceReport />,
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
