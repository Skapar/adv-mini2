import { Link } from 'react-router-dom'

export default function Home() {
  const token = localStorage.getItem('token')
  const isLoggedIn = !!token

  return (
    <div className="min-h-screen bg-gray-100">
      <section className="w-full bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-800">
            Welcome to Resume Analyzer
          </h1>
          <p className="text-lg md:text-xl text-gray-600 mb-8">
            Get started by uploading your resume or creating a job posting!
          </p>
          <div className="flex justify-center gap-6">
            {isLoggedIn ? (
              <>
                <Link 
                  to="/resume/upload" 
                  className="bg-teal-500 text-white px-8 py-3 rounded-lg hover:bg-teal-600 transition-colors"
                >
                  Upload Resume
                </Link>
                <Link 
                  to="/jobs/create" 
                  className="bg-teal-500 text-white px-8 py-3 rounded-lg hover:bg-teal-600 transition-colors"
                >
                  Create Job
                </Link>
                <Link 
                  to="/jobs" 
                  className="bg-teal-500 text-white px-8 py-3 rounded-lg hover:bg-teal-600 transition-colors"
                >
                  View Jobs
                </Link>
              </>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="bg-orange-400 text-white px-8 py-3 rounded-lg hover:bg-orange-500 transition-colors"
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="bg-orange-400 text-white px-8 py-3 rounded-lg hover:bg-orange-500 transition-colors"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="w-full py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-2xl md:text-3xl font-semibold mb-8 text-center text-gray-800">
            Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 border rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-bold text-gray-800 mb-2">Resume Analysis</h3>
              <p className="text-gray-600">
                Get detailed feedback on your resume
              </p>
            </div>
            <div className="p-6 border rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-bold text-gray-800 mb-2">Job Matching</h3>
              <p className="text-gray-600">
                Find the best candidates for your jobs
              </p>
            </div>
            <div className="p-6 border rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-bold text-gray-800 mb-2">Skill Insights</h3>
              <p className="text-gray-600">
                Identify skill gaps and improvements
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}