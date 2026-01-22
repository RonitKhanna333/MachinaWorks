'use client'

import { motion } from 'framer-motion'

export default function Stats() {
  const stats = [
    { value: '20+', label: 'Active Consultations', suffix: '' },
    { value: '₹2-50L', label: 'Typical Client Savings Range', suffix: '' },
    { value: '6-12', label: 'Months Typical Implementation', suffix: '' },
    { value: '₹60L-200L', label: 'Typical Project Budget', suffix: '' },
  ]

  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-800">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="text-center"
            >
              <div className="text-4xl md:text-5xl font-bold text-primary-700 dark:text-primary-300 mb-2">
                {stat.value}{stat.suffix}
              </div>
              <div className="text-slate-600 dark:text-slate-400 font-medium">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
