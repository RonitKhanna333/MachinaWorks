'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, TrendingUp, Gamepad2, Brain } from 'lucide-react'

const caseStudies = [
  {
    id: 1,
    title: 'Clash Royale AI Simulator',
    description: 'Superhuman game strategy using RL agents',
    metric: '72% win rate',
    icon: Gamepad2,
  },
  {
    id: 2,
    title: 'Ensemble RL Trading System',
    description: 'Beat NIFTY 50 with 36% annual returns',
    metric: '+8.17% outperformance',
    icon: TrendingUp,
  },
  {
    id: 3,
    title: 'AI Consultancy Platform',
    description: 'This system - personalized AI recommendations',
    metric: '39 use cases',
    icon: Brain,
  }
]

export default function CaseStudiesPreview() {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-slate-900">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="section-title">Real Projects. Real Impact.</h2>
          <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
            See how we've built AI systems that deliver measurable results
          </p>
        </motion.div>

        {/* Case Studies Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {caseStudies.map((study, index) => {
            const Icon = study.icon
            return (
              <motion.div
                key={study.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card group hover:shadow-xl transition-all duration-300"
              >
                {/* Icon */}
                <div className="feature-icon mb-4">
                  <Icon className="w-8 h-8" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                  {study.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-300 mb-4">
                  {study.description}
                </p>

                {/* Metric */}
                <div className="bg-slate-100 dark:bg-slate-800 rounded-lg px-4 py-3 mb-6 border border-slate-200 dark:border-slate-700">
                  <p className="text-sm text-slate-600 dark:text-slate-400 font-medium">Key Result</p>
                  <p className="text-lg font-bold text-primary-700 dark:text-primary-300">{study.metric}</p>
                </div>

                {/* Link */}
                <Link 
                  href="/case-studies"
                  className="inline-flex items-center space-x-2 text-primary-700 dark:text-primary-300 font-semibold hover:text-primary-800 dark:hover:text-primary-200 group/link"
                >
                  <span>View Details</span>
                  <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                </Link>
              </motion.div>
            )
          })}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center"
        >
          <Link 
            href="/case-studies"
            className="inline-flex items-center space-x-2 bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
          >
            <span>Explore All Case Studies</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </motion.div>
      </div>
    </section>
  )
}
