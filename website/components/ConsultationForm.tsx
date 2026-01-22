'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, Loader2, CheckCircle } from 'lucide-react'

export default function ConsultationForm() {
  const [formData, setFormData] = useState({
    problem: '',
    industry: '',
    companySize: '',
    email: '',
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const industries = [
    'E-commerce', 'Fintech', 'SaaS', 'Healthcare', 'Manufacturing',
    'Retail', 'AgriTech', 'Logistics', 'Media', 'Other'
  ]

  const companySizes = ['startup', 'SMB', 'enterprise']

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      // Send consultation to backend
      const response = await fetch('/api/consult', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error('Failed to get consultation')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Failed to process consultation. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <form onSubmit={handleSubmit} className="card space-y-6">
        {/* Problem Description */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            Describe Your Business Problem *
          </label>
          <textarea
            value={formData.problem}
            onChange={(e) => setFormData({ ...formData, problem: e.target.value })}
            placeholder="E.g., 'Our customer support costs ₹80L/month, handling 10,000 tickets/month. Response time: 24 hours, CSAT: 3.2/5. We need to reduce operational costs by 40% while improving customer satisfaction.'"
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
            rows={5}
            required
          />
          <p className="text-sm text-slate-500 mt-1">
            Include metrics in INR: monthly spend, volume, current outcomes, and specific goals
          </p>
        </div>

        {/* Industry */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            Industry *
          </label>
          <select
            value={formData.industry}
            onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            required
          >
            <option value="">Select your industry</option>
            {industries.map((industry) => (
              <option key={industry} value={industry}>
                {industry}
              </option>
            ))}
          </select>
        </div>

        {/* Company Size */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            Company Size *
          </label>
          <div className="grid grid-cols-3 gap-4">
            {companySizes.map((size) => (
              <button
                key={size}
                type="button"
                onClick={() => setFormData({ ...formData, companySize: size })}
                className={`py-3 px-4 rounded-lg border-2 font-semibold transition-all ${
                  formData.companySize === size
                    ? 'border-primary-600 bg-primary-50 text-primary-700'
                    : 'border-slate-300 hover:border-primary-300'
                }`}
              >
                {size.charAt(0).toUpperCase() + size.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Email */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            Email Address *
          </label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            placeholder="your@email.com"
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            required
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Get AI Consultation</span>
            </>
          )}
        </button>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
      </form>

      {/* Results */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Success Message */}
          <div className="card-gradient flex items-center space-x-3 text-green-700">
            <CheckCircle className="w-8 h-8" />
            <div>
              <h3 className="text-xl font-bold">Analysis Complete!</h3>
              <p className="text-sm text-slate-600">Your personalized AI consultation is ready</p>
            </div>
          </div>

          {/* AI Recommendations */}
          <div className="card">
            <h3 className="text-2xl font-bold mb-4 text-gradient">AI Solution Recommendations</h3>
            <div className="prose max-w-none">
              <p className="text-slate-700 whitespace-pre-wrap">{result.recommendations}</p>
            </div>
          </div>

          {/* Business Impact */}
          {result.businessImpact && (
            <div className="card bg-gradient-to-br from-primary-50 to-accent-50">
              <h3 className="text-2xl font-bold mb-6 text-gradient">Business Impact Analysis</h3>
              
              <div className="space-y-6">
                {/* Cost Savings */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-green-700 dark:text-green-400">
                    💰 Cost Savings
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.cost_savings}
                  </div>
                </div>

                {/* Revenue Potential */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-blue-700 dark:text-blue-400">
                    📈 Revenue Potential
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.revenue_potential}
                  </div>
                </div>

                {/* Time Savings */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-purple-700 dark:text-purple-400">
                    ⏱️ Time Savings
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.time_savings}
                  </div>
                </div>

                {/* ROI Estimate */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-orange-700 dark:text-orange-400">
                    💵 ROI Estimate
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.roi_estimate}
                  </div>
                </div>

                {/* Risk Reduction */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-red-700 dark:text-red-400">
                    🛡️ Risk Reduction
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.risk_reduction}
                  </div>
                </div>

                {/* Competitive Advantage */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-indigo-700 dark:text-indigo-400">
                    🚀 Competitive Advantage
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.competitive_advantage}
                  </div>
                </div>

                {/* Timeline */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-cyan-700 dark:text-cyan-400">
                    📅 Implementation Timeline
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.implementation_timeline}
                  </div>
                </div>

                {/* Resource Requirements */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-3 flex items-center text-teal-700 dark:text-teal-400">
                    👥 Resource Requirements
                  </h4>
                  <div className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {result.businessImpact.resource_requirements}
                  </div>
                </div>

                {/* Key Metrics */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-4 flex items-center text-pink-700 dark:text-pink-400">
                    📊 Key Success Metrics
                  </h4>
                  <ul className="space-y-2">
                    {result.businessImpact.key_metrics.map((metric: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-700 dark:text-slate-300">{metric}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Success Factors */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-4 flex items-center text-emerald-700 dark:text-emerald-400">
                    ✅ Success Factors
                  </h4>
                  <ul className="space-y-2">
                    {result.businessImpact.success_factors.map((factor: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-500 mr-3 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-700 dark:text-slate-300">{factor}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Potential Challenges */}
                <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-4 flex items-center text-amber-700 dark:text-amber-400">
                    ⚠️ Potential Challenges
                  </h4>
                  <ul className="space-y-2">
                    {result.businessImpact.potential_challenges.map((challenge: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <span className="text-amber-600 dark:text-amber-500 mr-3 flex-shrink-0 font-bold">⚠</span>
                        <span className="text-slate-700 dark:text-slate-300">{challenge}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* CTA */}
          <div className="card text-center bg-gradient-to-r from-primary-600 to-accent-600 text-white">
            <h3 className="text-2xl font-bold mb-4">Ready to Implement?</h3>
            <p className="mb-6">Let's discuss your project in detail and create a customized implementation plan.</p>
            <button className="bg-white text-primary-700 hover:bg-slate-50 font-semibold py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all">
              Schedule a Call
            </button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
