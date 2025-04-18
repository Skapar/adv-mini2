import { Link, NavLink, Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      <Outlet /> 
    </div>
  )
}

function Navigation() {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center">
            <span className="text-2xl font-bold text-teal-600">CareerMatch</span>
          </Link>
          <div className="flex space-x-8">
            <NavLink 
              to="/jobs" 
              className={({ isActive }) => `hover:text-teal-600 transition-colors ${isActive ? 'text-teal-600' : 'text-gray-600'}`}
            >
              Jobs
            </NavLink>
            <NavLink
              to="/resume/upload"
              className={({ isActive }) => `hover:text-teal-600 transition-colors ${isActive ? 'text-teal-600' : 'text-gray-600'}`}
            >
              Resume
            </NavLink>
          </div>
        </div>
      </div>
    </nav>
  )
}