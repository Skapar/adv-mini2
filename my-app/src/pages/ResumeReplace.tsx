import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { replaceResume } from '../services/api'
import toast from 'react-hot-toast'

export default function ResumeReplace() {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file to replace')
      return
    }

    const token = localStorage.getItem('token')
    if (!token) {
      setError('You must be logged in to replace a resume')
      navigate('/login')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await replaceResume(formData)
      console.log('Replace response:', response.data) 
      setAnalysis(response.data) 
      toast.success('Resume successfully updated!')

    } catch (error: any) {
      console.error('Replace error:', error.response?.data || error.message)
      setError(
        error.response?.data?.error || 
        error.message || 
        'Failed to replace resume. Please try again.'
      )
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-2xl w-full p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-gray-800">Replace Resume</h1>
        
        {/* Replace Form */}
        {!analysis ? (
          <>
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {error}
              </div>
            )}
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="w-full p-2 border rounded"
              />
              <button 
                type="submit" 
                className="w-full bg-teal-500 text-white p-2 rounded hover:bg-teal-600 transition-colors"
              >
                Replace
              </button>
            </form>
          </>
        ) : (
          /* Feedback Section */
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-800">Resume Analysis</h2>
            
            {/* Basic Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-gray-600">
                  <strong>Skills:</strong> {analysis.skills || 'N/A'}
                </p>
                <p className="text-gray-600">
                  <strong>Experience:</strong> {analysis.experience || 'Not specified'}
                </p>
              </div>
              <div>
                <p className="text-gray-600">
                  <strong>Education:</strong> {analysis.education || 'Not specified'}
                </p>
                <p className="text-gray-600">
                  <strong>Rating:</strong> {analysis.rating?.toFixed(2) || 'N/A'}
                </p>
              </div>
            </div>

            {/* Detailed Feedback */}
            <div className="border-t pt-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Feedback</h3>
              
              {/* Skill Gaps */}
              {analysis.analysis?.feedback?.skill_gaps?.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-md font-medium text-gray-700">Skill Gaps</h4>
                  <ul className="list-disc list-inside text-gray-600">
                    {analysis.analysis.feedback.skill_gaps.map((gap: string, index: number) => (
                      <li key={index}>{gap}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Formatting Suggestions */}
              {analysis.analysis?.feedback?.formatting?.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-md font-medium text-gray-700">Formatting Suggestions</h4>
                  <ul className="list-disc list-inside text-gray-600">
                    {analysis.analysis.feedback.formatting.map((suggestion: string, index: number) => (
                      <li key={index}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* ATS Keywords */}
              {analysis.analysis?.feedback?.ats_keywords?.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-md font-medium text-gray-700">ATS Keywords to Add</h4>
                  <ul className="list-disc list-inside text-gray-600">
                    {analysis.analysis.feedback.ats_keywords.map((keyword: string, index: number) => (
                      <li key={index}>{keyword}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Back to Home Button */}
            <button
              onClick={() => navigate('/')}
              className="w-full bg-teal-500 text-white p-2 rounded hover:bg-teal-600 transition-colors"
            >
              Back to Home
            </button>
          </div>
        )}
      </div>
    </div>
  )
}