import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getJobDetail } from '../services/api'

export default function JobDetail() {
  const { jobId } = useParams()
  const { data: job, isLoading } = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => getJobDetail(jobId!),
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <h1 className="text-吹 font-bold mb-4">Job Details</h1>
      <div className="border p-4 rounded">
        <p className="mb-2">{job?.data.description}</p>
        <p><strong>Required Skills:</strong> {job?.data.required_skills}</p>
        <p><strong>Required Experience:</strong> {job?.data.required_experience} years</p>
        <p><strong>Created:</strong> {new Date(job?.data.created_at).toLocaleDateString()}</p>
      </div>
    </div>
  )
}