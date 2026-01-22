'use client'

import { motion } from 'framer-motion'
import { Brain, TrendingUp, Zap, Target, Shield, Rocket, DollarSign, Clock, Users, CheckCircle } from 'lucide-react'
import Link from 'next/link'
import ConsultationForm from '@/components/ConsultationForm'
import ImpactShowcase from '@/components/ImpactShowcase'
import FeatureCards from '@/components/FeatureCards'
import CaseStudiesPreview from '@/components/CaseStudiesPreview'
import Stats from '@/components/Stats'

export default function Home() {
  return (
    <div className="overflow-hidden bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20 bg-white dark:bg-slate-950">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-accent-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        </div>

        <div className="relative max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-flex items-center space-x-2 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm px-6 py-3 rounded-full shadow-lg mb-8">
              <Zap className="w-5 h-5 text-accent-600" />
              <span className="text-sm font-semibold text-gradient">AI-Powered Business Transformation</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="block mb-2">Transform Your Indian Business</span>
              <span className="text-gradient">With AI That Delivers Real ROI</span>
            </h1>

            <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-400 mb-12 max-w-4xl mx-auto leading-relaxed">
              Get expert AI/ML recommendations tailored for Indian markets with <span className="font-bold text-primary-700">quantified business impact in INR</span>, 
              complete ROI analysis, and implementation roadmaps. From problem to profitable solution.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Link href="#consultation" className="btn-primary text-lg">
                Get Free AI Consultation
              </Link>
              <Link href="#how-it-works" className="btn-secondary text-lg">
                See How It Works
              </Link>
            </div>

            {/* Key Value Props */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {[
                { icon: DollarSign, label: '₹2L - ₹50L Savings', color: 'text-green-600' },
                { icon: Clock, label: '6-9 Mo. Payback', color: 'text-blue-600' },
                { icon: TrendingUp, label: '20-50% Cost Cut', color: 'text-purple-600' },
                { icon: Target, label: '₹50L+ Revenue', color: 'text-orange-600' },
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 + index * 0.1 }}
                  className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-md dark:bg-slate-900/80 dark:shadow-lg"
                >
                  <item.icon className={`w-8 h-8 mx-auto mb-2 ${item.color}`} />
                  <p className="font-bold text-sm dark:text-slate-200">{item.label}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <Stats />

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-slate-900">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="section-title">Why Indian Businesses Choose MachinaWorks</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
              Expert AI solutions designed for Indian markets with local business context, GST compliance, and rupee-based ROI analysis
            </p>
          </motion.div>

          <FeatureCards />
        </div>
      </section>

      {/* Impact Showcase */}
      <ImpactShowcase />

      {/* Case Studies Preview */}
      <CaseStudiesPreview />

      {/* How It Works */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 dark:from-slate-900 to-primary-50 dark:to-slate-800">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="section-title">How MachinaWorks Works</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
              From your business challenge to actionable AI strategy with Indian market insights
            </p>
          </motion.div>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              {
                step: '01',
                title: 'Describe Your Problem',
                description: 'Tell us your business challenge, current metrics, and constraints',
                icon: Brain,
              },
              {
                step: '02',
                title: 'AI Analysis',
                description: 'Our AI analyzes your problem and recommends optimal techniques',
                icon: Zap,
              },
              {
                step: '03',
                title: 'Business Impact',
                description: 'Get quantified ROI, cost savings, timeline, and resource needs',
                icon: TrendingUp,
              },
              {
                step: '04',
                title: 'Implementation Plan',
                description: 'Receive actionable roadmap with KPIs and success factors',
                icon: Rocket,
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="relative"
              >
                <div className="card-gradient text-center h-full">
                  <div className="text-6xl font-bold text-primary-200 mb-4">{item.step}</div>
                  <item.icon className="w-12 h-12 mx-auto mb-4 text-primary-600" />
                  <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                  <p className="text-slate-600">{item.description}</p>
                </div>
                {index < 3 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                    <div className="w-8 h-0.5 bg-gradient-to-r from-primary-400 to-accent-400"></div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Consultation Form */}
      <section id="consultation" className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-slate-900">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="section-title">Get Your Free AI Strategy Report</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              Describe your business challenge and get instant AI recommendations with INR-based ROI, implementation timeline, and Indian market context
            </p>
          </motion.div>

          <ConsultationForm />
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
            <Rocket className="w-20 h-20 mx-auto mb-6" />
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Scale Your Indian Business with AI?
            </h2>
            <p className="text-xl mb-10 opacity-90">
              Join Indian companies across e-commerce, fintech, manufacturing, and more who are leveraging AI for measurable business impact
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#consultation" className="bg-white dark:bg-slate-900 text-primary-700 dark:text-primary-300 hover:bg-slate-50 dark:hover:bg-slate-800 font-semibold py-4 px-10 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-lg">
                Get Started Free
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
