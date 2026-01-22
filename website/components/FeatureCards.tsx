'use client'

import { motion } from 'framer-motion'
import { DollarSign, TrendingUp, Clock, Target, Shield, Rocket, Users, CheckCircle, BarChart3, Zap } from 'lucide-react'

export default function FeatureCards() {
  const features = [
    {
      icon: DollarSign,
      title: 'Quantified Cost Reduction',
      description: 'Break down labor, infrastructure, and error costs with precise INR savings and monthly/annual impact projections.',
    },
    {
      icon: TrendingUp,
      title: 'Revenue Stream Identification',
      description: 'Uncover new ₹1L-₹5L+ monthly revenue opportunities through AI-powered product launches and market expansion.',
    },
    {
      icon: Clock,
      title: 'Efficiency & Productivity',
      description: 'Measure team productivity gains from 2000-5000 hours/year, calculated with actual salary costs for ROI.',
    },
    {
      icon: Target,
      title: 'Break-Even & ROI Timelines',
      description: 'Get realistic implementation cost, 6-12 month payback periods, and 200-400% annual ROI estimates.',
    },
    {
      icon: Shield,
      title: 'Compliance & Risk Management',
      description: 'Ensure GST compliance, reduce audit risks, and quantify risk mitigation benefits for Indian regulations.',
    },
    {
      icon: Rocket,
      title: 'Competitive Positioning',
      description: 'Analyze market gap opportunities and quantify competitive advantages in your specific Indian market segment.',
    },
    {
      icon: BarChart3,
      title: 'Custom KPI Framework',
      description: 'Define measurable success metrics aligned with your business goals and quarterly performance tracking.',
    },
    {
      icon: Users,
      title: 'Team & Budget Planning',
      description: 'Detailed resource requirements: team size, skill sets, infrastructure costs, and total implementation budget.',
    },
    {
      icon: Zap,
      title: 'Phased Implementation',
      description: '6-18 month realistic project roadmap with milestones, dependencies, and resource allocation schedules.',
    },
    {
      icon: CheckCircle,
      title: 'Risk Mitigation Strategy',
      description: 'Identify adoption challenges, data quality issues, and provide concrete mitigation tactics upfront.',
    },
  ]

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      {features.map((feature, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: index * 0.05 }}
          className="card"
        >
          <div className="feature-icon mb-6">
            <feature.icon className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-slate-900 dark:text-white">{feature.title}</h3>
          <p className="text-slate-600 dark:text-slate-400">{feature.description}</p>
        </motion.div>
      ))}
    </div>
  )
}
