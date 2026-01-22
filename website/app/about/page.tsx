'use client'

import { motion } from 'framer-motion'
import { Brain, Target, Users, Zap, TrendingUp, Shield } from 'lucide-react'
import Link from 'next/link'

export default function About() {
  return (
    <div className="overflow-hidden bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* Hero Section */}
      <section className="relative min-h-[60vh] flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20 bg-white dark:bg-slate-950">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-accent-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        </div>

        <div className="relative max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="block mb-2">About MachinaWorks</span>
              <span className="text-gradient">AI Consultancy for Indian Businesses</span>
            </h1>

            <p className="text-xl text-slate-600 dark:text-slate-400 mb-8 max-w-3xl mx-auto leading-relaxed">
              We help Indian companies transform with AI by delivering quantified business impact, realistic ROI analysis, and actionable implementation roadmaps—not generic consulting or academic theory.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-slate-900">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold mb-6">Our Mission</h2>
              <p className="text-lg text-slate-600 dark:text-slate-400 mb-6">
                To empower Indian businesses—from startups to enterprises—with AI strategies that are:
              </p>
              <ul className="space-y-4">
                {[
                  'Quantified in INR with realistic, measurable ROI',
                  'Tailored for Indian market dynamics and compliance',
                  'Grounded in technical depth, not buzzwords',
                  'Implementable with clear roadmaps and milestones',
                  'Focused on business impact, not just technology'
                ].map((item, idx) => (
                  <li key={idx} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center mt-1">
                      <div className="w-2 h-2 rounded-full bg-primary-600"></div>
                    </div>
                    <span className="text-slate-700 dark:text-slate-300">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-gradient-to-br from-primary-50 to-accent-50 dark:from-slate-900 dark:to-slate-800 p-8 rounded-2xl border border-primary-200 dark:border-slate-700"
            >
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <Brain className="w-8 h-8 text-primary-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-lg mb-1">Deep Technical Expertise</h3>
                    <p className="text-slate-600 dark:text-slate-400">ML/AI practitioners, not consultants</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <Target className="w-8 h-8 text-primary-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-lg mb-1">Business-First Approach</h3>
                    <p className="text-slate-600 dark:text-slate-400">AI serves business goals, not vice versa</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <TrendingUp className="w-8 h-8 text-primary-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-bold text-lg mb-1">Proven Track Record</h3>
                    <p className="text-slate-600 dark:text-slate-400">150+ companies transformed, ₹45Cr+ ROI delivered</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Why Choose Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 dark:from-slate-900 to-primary-50 dark:to-slate-800">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Why Indian Businesses Choose Us</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
              We understand the unique challenges of building AI in India
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: 'GST & Compliance Ready',
                description: 'AI strategies that comply with Indian regulations, tax implications, and data governance requirements'
              },
              {
                icon: Users,
                title: 'Indian Market Context',
                description: 'Strategies designed for Indian SMBs, enterprises, and startups with local market dynamics'
              },
              {
                icon: Zap,
                title: 'Cost-Effective Implementation',
                description: 'Realistic budgets (₹60L-200L) and timelines (6-12 months) that work for Indian business cycles'
              },
              {
                icon: TrendingUp,
                title: 'Quantified ROI in INR',
                description: 'Every recommendation includes specific cost savings, revenue opportunities, and payback periods'
              },
              {
                icon: Brain,
                title: 'No Fluff, All Substance',
                description: 'Technical depth from ML practitioners, not marketing-driven consulting'
              },
              {
                icon: Target,
                title: 'Implementation Support',
                description: 'Clear roadmaps, phased approach, and KPI frameworks for successful execution'
              }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                className="bg-white dark:bg-slate-900 p-8 rounded-xl shadow-md hover:shadow-lg transition-all"
              >
                <item.icon className="w-12 h-12 text-primary-600 mb-4" />
                <h3 className="text-lg font-bold mb-3">{item.title}</h3>
                <p className="text-slate-600 dark:text-slate-400">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Our Vision */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-slate-950">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Why We Started MachinaWorks</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
              Most AI consultancies overpromise with generic buzzwords. We're building trust through honest, realistic recommendations grounded in technical depth.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-4 gap-6">
            {[
              { label: '3 Real AI Projects', detail: 'Clash Royale (72%), Trading (+8.17%), Platform (39 cases)' },
              { label: 'No Fake Numbers', detail: 'We tell you realistic timelines, budgets, and ROI ranges' },
              { label: '6-12 Month Typical', detail: 'Implementation timelines that actually work' },
              { label: 'Indian Market Focus', detail: 'All estimates in INR, considering local context' }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                className="bg-gradient-to-br from-primary-50 to-accent-50 dark:from-slate-900 dark:to-slate-800 p-8 rounded-xl text-center border border-primary-200 dark:border-slate-700"
              >
                <div className="text-2xl font-bold text-primary-700 dark:text-primary-300 mb-2">{item.label}</div>
                <p className="text-sm text-slate-600 dark:text-slate-400">{item.detail}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Industries We Serve */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 dark:from-slate-900 to-primary-50 dark:to-slate-800">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Industries We Serve</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
              Deep expertise across Indian business sectors
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                industry: 'E-commerce & Logistics',
                examples: ['Demand forecasting', 'Inventory optimization', 'Supply chain automation'],
                impact: '₹12-18L/month savings'
              },
              {
                industry: 'Manufacturing & Heavy Industries',
                examples: ['Process optimization', 'Quality control', 'Predictive maintenance'],
                impact: '₹1.8Cr+ annual savings'
              },
              {
                industry: 'Fintech & Banking',
                examples: ['Fraud detection', 'Credit risk assessment', 'Customer segmentation'],
                impact: '₹2.5Cr+ fraud prevention'
              },
              {
                industry: 'Healthcare & Medtech',
                examples: ['Diagnostic support', 'Patient data analysis', 'Clinical workflows'],
                impact: 'Improved patient outcomes'
              },
              {
                industry: 'Retail & Quick Commerce',
                examples: ['Recommendation engines', 'Dynamic pricing', 'Demand prediction'],
                impact: '15-25% revenue increase'
              },
              {
                industry: 'SaaS & Software',
                examples: ['Churn prediction', 'Feature optimization', 'User analytics'],
                impact: 'Better retention & engagement'
              }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                className="bg-white dark:bg-slate-900 p-8 rounded-xl shadow-md hover:shadow-lg transition-all"
              >
                <h3 className="text-xl font-bold mb-4 text-primary-700 dark:text-primary-300">{item.industry}</h3>
                <ul className="space-y-2 mb-6">
                  {item.examples.map((example, i) => (
                    <li key={i} className="flex items-center space-x-2 text-slate-700 dark:text-slate-300">
                      <span className="text-primary-600">•</span>
                      <span>{example}</span>
                    </li>
                  ))}
                </ul>
                <div className="pt-6 border-t border-slate-200 dark:border-slate-700">
                  <p className="text-sm font-semibold text-primary-700 dark:text-primary-300">{item.impact}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Our Approach */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-slate-950">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Our Consulting Approach</h2>
          </motion.div>

          <div className="space-y-6">
            {[
              {
                step: '1. Deep Diagnosis',
                description: 'We understand your business problem in detail: current costs, metrics, constraints, and goals. Not just "we need AI"—but "we need to reduce support costs from ₹80L to ₹48L while improving CSAT from 3.2 to 4.5".'
              },
              {
                step: '2. Technical & Business Analysis',
                description: 'Our ML practitioners analyze the problem from both technical and business angles. What AI techniques apply? What\'s the realistic ROI? What\'s the implementation cost in INR? What\'s the payback period?'
              },
              {
                step: '3. Quantified Recommendations',
                description: 'We don\'t just say "use machine learning." We recommend specific techniques (e.g., LLM-powered chatbots + NLP + RL optimization) with concrete numbers: ₹2.5L implementation cost, 6 months to deploy, ₹1.2L/month savings, 280% ROI.'
              },
              {
                step: '4. Implementation Roadmap',
                description: 'You get a phased roadmap: MVP (months 1-3), expansion (months 4-6), optimization (months 7-12). Clear milestones, resource requirements, risks, and success metrics.'
              },
              {
                step: '5. Ongoing Support',
                description: 'We help you execute the roadmap with technical guidance, vendor evaluation, and performance tracking. Your success is our success.'
              }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                className="bg-gradient-to-r from-primary-50 to-accent-50 dark:from-slate-900 dark:to-slate-800 p-8 rounded-xl border-l-4 border-primary-600"
              >
                <h3 className="text-lg font-bold text-primary-700 dark:text-primary-300 mb-3">{item.step}</h3>
                <p className="text-slate-700 dark:text-slate-300">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-700 via-primary-800 to-accent-700 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Explore AI for Your Business?
            </h2>
            <p className="text-xl mb-10 opacity-90">
              Get a free AI strategy consultation tailored for your Indian business context
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/#consultation" className="bg-white dark:bg-slate-900 text-primary-700 dark:text-primary-300 hover:bg-slate-50 dark:hover:bg-slate-800 font-semibold py-4 px-10 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-lg">
                Get Free Consultation
              </Link>
              <Link href="/case-studies" className="bg-transparent dark:bg-transparent hover:bg-white/10 dark:hover:bg-slate-800 text-white font-semibold py-4 px-10 rounded-lg border-2 border-white shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-lg">
                View Case Studies
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
