import React from 'react'

interface PageContainerProps {
  children: React.ReactNode
  title: string
}

export default function PageContainer({ children, title }: PageContainerProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 animate-fade-in-down">
          {title}
        </h1>
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
          {children}
        </div>
      </div>
    </div>
  )
} 