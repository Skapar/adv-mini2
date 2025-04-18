import { useState } from 'react' 
import { useNavigate } from 'react-router-dom'
import { createJob } from '../services/api'
import toast from 'react-hot-toast'

export default function JobCreate() {
  const [description, setDescription] = useState('')
  const navigate = useNavigate()
  const userRole = localStorage.getItem('userRole') 

  if (userRole !== 'admin') {
    navigate('/jobs')
  }


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await createJob({ description })
      toast.success('Job successfully created!')
      navigate('/jobs')
    } catch (error) {
      console.error(error)
    }
  }


  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-gray-800">Create Job Posting</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Job Description"
            className="w-full p-2 border rounded h-32"
          />
          <button 
            type="submit" 
            className="w-full bg-teal-500 text-white p-2 rounded hover:bg-teal-600 transition-colors"
          >
            Create Job
          </button>
        </form>
      </div>
    </div>
  )
}