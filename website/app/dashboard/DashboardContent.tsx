'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { User, FileText, Clock, Settings, ChevronRight } from 'lucide-react'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

interface DashboardContentProps {
  user: any
}

export default function DashboardContent({ user }: DashboardContentProps) {
  const [activeTab, setActiveTab] = useState('consultations')

  const tabs = [
    { id: 'consultations', name: 'My Consultations', icon: FileText },
    { id: 'history', name: 'History', icon: Clock },
    { id: 'settings', name: 'Settings', icon: Settings },
  ]

  // Mock consultation data - in production, fetch from Supabase
  const consultations = [
    {
      id: 1,
      problem: 'Customer churn prediction for SaaS platform',
      industry: 'SaaS',
      date: '2026-01-20',
      status: 'completed',
    },
    {
      id: 2,
      problem: 'Automated invoice processing system',
      industry: 'Finance',
      date: '2026-01-18',
      status: 'completed',
    },
  ]

  return (
    <>
      <Header />
      <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Welcome Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-gradient">
              Welcome back, {user.user_metadata?.full_name || user.email?.split('@')[0]}!
            </h1>
            <p className="text-slate-600 mt-2">
              Manage your AI consultations and view your history
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="lg:col-span-1"
            >
              <div className="card sticky top-24">
                {/* User Info */}
                <div className="flex items-center space-x-3 pb-6 border-b border-slate-200">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
                    {user.email?.[0]?.toUpperCase() || 'U'}
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900 dark:text-slate-100">
                      {user.user_metadata?.full_name || 'User'}
                    </p>
                    <p className="text-sm text-slate-500 dark:text-slate-400 truncate max-w-[150px]">
                      {user.email}
                    </p>
                  </div>
                </div>

                {/* Navigation */}
                <nav className="mt-6 space-y-2">
                  {tabs.map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                        activeTab === tab.id
                          ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                      }`}
                    >
                      <tab.icon className="w-5 h-5" />
                      <span className="font-medium">{tab.name}</span>
                    </button>
                  ))}
                </nav>
              </div>
            </motion.div>

            {/* Main Content */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="lg:col-span-3"
            >
              {activeTab === 'consultations' && (
                <div className="space-y-6">
                  <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">My Consultations</h2>
                    <a
                      href="/#consultation"
                      className="btn-primary"
                    >
                      New Consultation
                    </a>
                  </div>

                  {consultations.length > 0 ? (
                    <div className="space-y-4">
                      {consultations.map((consultation) => (
                        <div
                          key={consultation.id}
                          className="card hover:shadow-lg transition-shadow cursor-pointer"
                        >
                          <div className="flex justify-between items-start">
                            <div>
                              <h3 className="font-semibold text-slate-900 dark:text-slate-100">
                                {consultation.problem}
                              </h3>
                              <div className="flex items-center space-x-4 mt-2 text-sm text-slate-500 dark:text-slate-400">
                                <span className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">
                                  {consultation.industry}
                                </span>
                                <span>{consultation.date}</span>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <span className="text-green-600 text-sm font-medium capitalize">
                                {consultation.status}
                              </span>
                              <ChevronRight className="w-5 h-5 text-slate-400" />
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="card text-center py-12">
                      <FileText className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
                      <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-300 mb-2">
                        No consultations yet
                      </h3>
                      <p className="text-slate-500 dark:text-slate-400 mb-4">
                        Start your first AI consultation to see it here
                      </p>
                      <a href="/#consultation" className="btn-primary">
                        Get Started
                      </a>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'history' && (
                <div className="card">
                  <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-4">History</h2>
                  <p className="text-slate-600 dark:text-slate-400">
                    Your complete consultation history will appear here.
                  </p>
                </div>
              )}

              {activeTab === 'settings' && (
                <div className="card">
                  <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-6">Settings</h2>
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Email
                      </label>
                      <input
                        type="email"
                        value={user.email}
                        disabled
                        className="w-full px-4 py-3 border border-slate-300 rounded-lg bg-slate-50 text-slate-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Full Name
                      </label>
                      <input
                        type="text"
                        defaultValue={user.user_metadata?.full_name || ''}
                        placeholder="Enter your name"
                        className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                    <button className="btn-primary">Save Changes</button>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
