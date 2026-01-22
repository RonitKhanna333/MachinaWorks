'use client'

import { motion } from 'framer-motion'
import { TrendingUp, Users, Zap } from 'lucide-react'

export default function ImpactShowcase() {
  const examples = [
    {
      industry: 'E-commerce & Logistics',
      problem: 'Customer Support Automation',
      icon: Users,
      metrics: [
        { label: 'Potential Monthly Savings', value: '₹12-18L/month', change: '↓ 25-30%' },
        { label: 'Potential Response Time', value: '< 1 hour', change: '↓ 85%' },
        { label: 'Potential Satisfaction', value: '4.6/5.0', change: '↑ 35%' },
        { label: 'Projected ROI', value: '180-220%', change: 'Annual' },
      ],
      timeline: '4-6 months',
      budget: '₹75-110L',
    },
    {
      industry: 'Manufacturing & Heavy Industries',
      problem: 'Predictive Maintenance AI',
      icon: Zap,
      metrics: [
        { label: 'Potential Downtime Reduction', value: '65-72%', change: '↓ 2000 hrs/year' },
        { label: 'Potential Maintenance Savings', value: '₹1.8Cr+', change: '↓ 38%' },
        { label: 'Potential Equipment Lifespan', value: '+32%', change: 'Extended' },
        { label: 'Projected ROI', value: '280%', change: '15 months' },
      ],
      timeline: '5-7 months',
      budget: '₹150-200L',
    },
    {
      industry: 'Fintech & Banking',
      problem: 'Fraud Detection & Prevention',
      icon: TrendingUp,
      metrics: [
        { label: 'Potential Fraud Prevention', value: '↓ 82%', change: '₹2.5Cr saved' },
        { label: 'Potential False Positives', value: '↓ 58%', change: 'Better UX' },
        { label: 'Potential Detection Speed', value: '< 50ms', change: 'Real-time' },
        { label: 'Projected ROI', value: '320%', change: '11 months' },
      ],
      timeline: '3-5 months',
      budget: '₹60-90L',
    },
  ]

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-900 to-primary-900 text-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">Real Business Impact</h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            See how AI delivers measurable results across different industries
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {examples.map((example, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all"
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <div>
                  <span className="text-primary-300 text-sm font-semibold">{example.industry}</span>
                  <h3 className="text-xl font-bold mt-1">{example.problem}</h3>
                </div>
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                  <example.icon className="w-6 h-6" />
                </div>
              </div>

              {/* Metrics */}
              <div className="space-y-4 mb-6">
                {example.metrics.map((metric, idx) => (
                  <div key={idx} className="bg-white/5 rounded-lg p-3">
                    <div className="text-sm text-slate-300 mb-1">{metric.label}</div>
                    <div className="flex items-baseline justify-between">
                      <span className="text-2xl font-bold">{metric.value}</span>
                      <span className="text-sm text-green-400">{metric.change}</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Footer */}
              <div className="flex items-center justify-between text-sm border-t border-white/20 pt-4">
                <div>
                  <span className="text-slate-400">Timeline</span>
                  <div className="font-semibold">{example.timeline}</div>
                </div>
                <div className="text-right">
                  <span className="text-slate-400">Budget</span>
                  <div className="font-semibold">{example.budget}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
