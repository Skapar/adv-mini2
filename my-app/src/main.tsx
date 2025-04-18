import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import Home from './pages/Home.tsx'
import Login from './pages/Login.tsx'
import Register from './pages/Register.tsx'
import ResumeUpload from './pages/ResumeUpload.tsx'
import ResumeReplace from './pages/ResumeReplace.tsx'
import JobCreate from './pages/JobCreate.tsx'
import JobList from './pages/JobList.tsx'
import JobDetail from './pages/JobDetail.tsx'
import JobMatches from './pages/JobMatches.tsx'
import './index.css'
import { Toaster } from 'react-hot-toast' 

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/login', element: <Login /> },
      { path: '/register', element: <Register /> },
      { path: '/resume/upload', element: <ResumeUpload /> },
      { path: '/resume/replace', element: <ResumeReplace /> },
      { path: '/jobs/create', element: <JobCreate /> },
      { path: '/jobs', element: <JobList /> },
      { path: '/jobs/:jobId', element: <JobDetail /> },
      { path: '/jobs/:jobId/matches', element: <JobMatches /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <Toaster position="top-right" toastOptions={{ duration: 3000 }} /> {/* Add Toaster */}
    </QueryClientProvider>
  </React.StrictMode>,
)