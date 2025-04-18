import { useQuery } from '@tanstack/react-query'
import { getJobs } from '../services/api'
import { Link } from 'react-router-dom'

export default function JobList() {
  const { data: jobs, isLoading } = useQuery({
    queryKey: ['jobs'],
    queryFn: getJobs,
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Job Listings</h1>
      <div className="space-y-4">
        {jobs?.data.map((job: any) => (
          <div key={job.id} className="border p-4 rounded">
            <p className="truncate">{job.description}</p>
            <div className="mt-2 space-x-2">
              <Link to={`/jobs/${job.id}`} className="text-blue-600 hover:underline">Details</Link>
              <Link to={`/jobs/${job.id}/matches`} className="text-blue-600 hover:underline">Matches</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}