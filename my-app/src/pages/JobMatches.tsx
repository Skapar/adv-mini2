import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getJobMatches } from '../services/api'
import toast from 'react-hot-toast'
import { useEffect } from 'react'
import PageContainer from '../components/PageContainer'

interface Match {
  resume_id: string
  user: string
  compatibility_score: number
  matched_skills: string
  resume_skills: string
  resume_experience: string
}

interface MatchesResponse {
  data: Match[]
}

export default function JobMatches() {
  const { jobId } = useParams()
  const { data: matches, isLoading, error } = useQuery<MatchesResponse>({
    queryKey: ['jobMatches', jobId],
    queryFn: () => getJobMatches(jobId!),
    enabled: !!jobId
  })

  useEffect(() => {
    if (error) {
      console.error('Error fetching job matches:', error)
      toast.error(
        error.message || 
        'Failed to fetch matching resumes. Please try again.'
      )
    }
  }, [error])

  if (isLoading) return <div className="text-center">Loading...</div>

  if (error) {
    return (
      <div className="text-center text-red-600">
        Error loading matches: {error.message}
      </div>
    )
  }

  if (!matches?.data || matches.data.length === 0) {
    return (
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Resume Matches</h1>
        <p>No matching resumes found for this job.</p>
      </div>
    )
  }

  return (
    <PageContainer title={`Resume Matches for Job #${jobId}`}>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {matches.data.map((match) => (
          <div
            key={match.resume_id}
            className="group relative border border-gray-200 rounded-xl p-6 transition-all hover:border-teal-100 hover:shadow-lg"
          >
            <div className="absolute inset-0 bg-gradient-to-b from-teal-50/50 to-white opacity-0 group-hover:opacity-100 transition-opacity rounded-xl" />
            
            <div className="relative">
              <div className="flex items-center justify-between mb-4">
                <span className="inline-block bg-teal-100 text-teal-800 px-3 py-1 rounded-full text-sm font-medium">
                  Score: {match.compatibility_score.toFixed(1)}%
                </span>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {match.user || 'Anonymous'}
                  </h3>
                  <p className="text-sm text-gray-500">
                    ID: {match.resume_id}
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center">
                    <span className="mr-2">🎯</span>
                    <span className="text-sm">
                      {match.matched_skills || 'No skills matched'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </PageContainer>
  )
}