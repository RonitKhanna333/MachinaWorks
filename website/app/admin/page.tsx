'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@supabase/supabase-js'
import { Mail, User, Building2, MessageSquare, Eye, Trash2, Download } from 'lucide-react'
import Link from 'next/link'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

type SubmissionType = 'signup' | 'consultation' | 'contact'

interface Submission {
  id: string
  type: SubmissionType
  email: string
  data: any
  created_at: string
}

export default function AdminDashboard() {
  const [submissions, setSubmissions] = useState<Submission[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | SubmissionType>('all')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchSubmissions()
    const subscription = supabase
      .channel('submissions')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'form_submissions' },
        () => fetchSubmissions()
      )
      .subscribe()

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  const fetchSubmissions = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('form_submissions')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      setSubmissions(data || [])
    } catch (error) {
      console.error('Error fetching submissions:', error)
    } finally {
      setLoading(false)
    }
  }

  const deleteSubmission = async (id: string) => {
    try {
      const { error } = await supabase
        .from('form_submissions')
        .delete()
        .eq('id', id)

      if (error) throw error
      setSubmissions(submissions.filter(s => s.id !== id))
    } catch (error) {
      console.error('Error deleting submission:', error)
    }
  }

  const exportData = () => {
    const csv = [
      ['ID', 'Type', 'Email', 'Data', 'Date'],
      ...filteredSubmissions.map(s => [
        s.id,
        s.type,
        s.email,
        JSON.stringify(s.data),
        new Date(s.created_at).toLocaleString(),
      ]),
    ]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `submissions_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
  }

  const filteredSubmissions = submissions.filter(s => {
    const matchesFilter = filter === 'all' || s.type === filter
    const matchesSearch = 
      s.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      JSON.stringify(s.data).toLowerCase().includes(searchTerm.toLowerCase())
    return matchesFilter && matchesSearch
  })

  const stats = {
    total: submissions.length,
    signups: submissions.filter(s => s.type === 'signup').length,
    consultations: submissions.filter(s => s.type === 'consultation').length,
    contacts: submissions.filter(s => s.type === 'contact').length,
  }

  const getIcon = (type: SubmissionType) => {
    switch (type) {
      case 'signup':
        return <User className="w-4 h-4" />
      case 'consultation':
        return <MessageSquare className="w-4 h-4" />
      case 'contact':
        return <Mail className="w-4 h-4" />
      default:
        return null
    }
  }

  const getTypeColor = (type: SubmissionType) => {
    switch (type) {
      case 'signup':
        return 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
      case 'consultation':
        return 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
      case 'contact':
        return 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
      default:
        return 'bg-gray-100 dark:bg-gray-900'
    }
  }

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950">
      {/* Header */}
      <div className="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-2">
                Admin Dashboard
              </h1>
              <p className="text-slate-600 dark:text-slate-400">
                Track all form submissions and user registrations
              </p>
            </div>
            <Link href="/" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white">
              ← Back to Site
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">Total Submissions</p>
              <p className="text-3xl font-bold text-slate-900 dark:text-white">{stats.total}</p>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">Signups</p>
              <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{stats.signups}</p>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">Consultations</p>
              <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">{stats.consultations}</p>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">Contacts</p>
              <p className="text-3xl font-bold text-green-600 dark:text-green-400">{stats.contacts}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Controls */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <input
              type="text"
              placeholder="Search by email or content..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />

            {/* Filter */}
            <div className="flex gap-2">
              {(['all', 'signup', 'consultation', 'contact'] as const).map(f => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    filter === f
                      ? 'bg-primary-600 text-white'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </button>
              ))}
            </div>

            {/* Export */}
            <button
              onClick={exportData}
              className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 font-medium flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export
            </button>
          </div>
        </div>

        {/* Submissions Table */}
        <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 overflow-hidden">
          {loading ? (
            <div className="p-8 text-center text-slate-600 dark:text-slate-400">
              Loading submissions...
            </div>
          ) : filteredSubmissions.length === 0 ? (
            <div className="p-8 text-center text-slate-600 dark:text-slate-400">
              No submissions found
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900 dark:text-white">Type</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900 dark:text-white">Email</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900 dark:text-white">Details</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900 dark:text-white">Date</th>
                    <th className="px-6 py-3 text-right text-sm font-semibold text-slate-900 dark:text-white">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                  {filteredSubmissions.map(submission => (
                    <tr key={submission.id} className="hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                      <td className="px-6 py-4">
                        <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(submission.type)}`}>
                          {getIcon(submission.type)}
                          {submission.type.charAt(0).toUpperCase() + submission.type.slice(1)}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-slate-900 dark:text-white">
                        {submission.email}
                      </td>
                      <td className="px-6 py-4 text-slate-600 dark:text-slate-400 max-w-xs truncate">
                        {submission.type === 'signup'
                          ? `User: ${submission.data.fullName}`
                          : submission.type === 'consultation'
                          ? `Problem: ${submission.data.problem}`
                          : `Message: ${submission.data.message}`}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
                        {new Date(submission.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <button
                            onClick={() => {
                              alert(JSON.stringify(submission.data, null, 2))
                            }}
                            className="p-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
                            title="View details"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => {
                              if (confirm('Delete this submission?')) {
                                deleteSubmission(submission.id)
                              }
                            }}
                            className="p-2 text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
