import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <nav className="bg-green-200 p-4 text-gray-800">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">Resume Analyzer</Link>
        <div className="space-x-6">
          {token ? (
            <>
              <Link 
                to="/resume/upload" 
                className="hover:underline px-3 py-1 rounded bg-teal-500 text-white hover:bg-teal-600 transition-colors"
              >
                Upload Resume
              </Link>
              <Link 
                to="/resume/replace" 
                className="hover:underline px-3 py-1 rounded bg-teal-500 text-white hover:bg-teal-600 transition-colors"
              >
                Replace Resume
              </Link>
              <Link 
                to="/jobs/create" 
                className="hover:underline px-3 py-1 rounded bg-teal-500 text-white hover:bg-teal-600 transition-colors"
              >
                Create Job
              </Link>
              <Link 
                to="/jobs" 
                className="hover:underline px-3 py-1 rounded bg-teal-500 text-white hover:bg-teal-600 transition-colors"
              >
                Job Listings
              </Link>
              <button 
                onClick={handleLogout} 
                className="hover:underline px-3 py-1 rounded bg-orange-400 text-white hover:bg-orange-500 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link 
                to="/login" 
                className="hover:underline px-3 py-1 rounded bg-orange-400 text-white hover:bg-orange-500 transition-colors"
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className="hover:underline px-3 py-1 rounded bg-orange-400 text-white hover:bg-orange-500 transition-colors"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}