'use client'

import { motion } from 'framer-motion'
import { TrendingUp, Gamepad2, Brain, ArrowUpRight, BarChart3, Zap } from 'lucide-react'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

const caseStudies = [
  {
    id: 1,
    title: 'Clash Royale AI Simulator',
    category: 'Reinforcement Learning',
    description: 'AI-powered game strategy system using RL agents',
    challenge: 'Develop an AI that learns optimal card placement and spell timing strategies in Clash Royale through self-play',
    solution: 'Built RL agents (PPO, A2C, DQN) that learn game dynamics and strategy through millions of simulations against themselves',
    results: [
      'Achieved superhuman performance in specific matchups',
      'Discovered novel card combinations and strategies',
      'Successfully generalized across 50+ different deck archetypes',
      'Reduced training time by 60% with curriculum learning'
    ],
    metrics: {
      'Win Rate': '72% vs competitive players',
      'Training Time': '500K episodes',
      'Convergence': '2 weeks on GPU'
    },
    tech: ['PyTorch', 'Stable-Baselines3', 'OpenAI Gym', 'Python'],
    color: 'from-blue-500 to-purple-500',
    icon: Gamepad2
  },
  {
    id: 2,
    title: 'Ensemble RL Trading System',
    category: 'Deep Learning & RL',
    description: 'Outperformed NIFTY 50 with 36% annual returns using deep learning + reinforcement learning',
    challenge: 'Build a portfolio optimization system that consistently beats NIFTY 50 benchmark while minimizing risk and drawdowns in Indian stock markets',
    solution: 'Engineered 5 ensemble models combining RL agents (A2C, PPO, TD3, DDPG, SAC) with Deep Learning (LSTM/Transformer) for dynamic portfolio allocation based on market conditions',
    results: [
      '27.59% total return vs NIFTY 50 19.42%',
      'Sharpe Ratio: 3.75 vs NIFTY 1.99',
      'Minimal drawdown: -5.09% vs market volatility',
      'Consistent outperformance on 2023-2024 out-of-sample data'
    ],
    metrics: {
      'Annual Return': '36.06%',
      'Sharpe Ratio': '3.75',
      'Max Drawdown': '-5.09%',
      'Volatility': '8.9%'
    },
    tech: ['FinRL', 'PyTorch', 'LSTM/Transformer', 'Pandas', 'NumPy', 'Scikit-learn'],
    color: 'from-green-500 to-emerald-500',
    icon: TrendingUp
  },
  {
    id: 3,
    title: 'AI Consultancy Platform',
    category: 'Gen AI & RAG',
    description: 'RAG-powered consultant connecting businesses with AI solutions using vector search + LLM reasoning',
    challenge: 'Build an intelligent system that understands business problems and recommends tailored AI solutions with accurate ROI projections and implementation strategies',
    solution: 'Implemented Retrieval-Augmented Generation (RAG) with ChromaDB for semantic search, Groq LLM for fast inference, and automated business impact analysis using LLM-powered financial modeling',
    results: [
      'Personalized recommendations for 40+ business domains',
      'Accurate ROI estimates within 15% of actual implementations',
      '39 Indian market-specific use cases in vector store',
      'Real-time business impact analysis across 11 dimensions'
    ],
    metrics: {
      'Use Cases': '39 Indian-focused',
      'Response Time': '<5 seconds',
      'Embeddings': 'HuggingFace all-MiniLM',
      'LLM': 'Groq Llama 3.3 70B'
    },
    tech: ['ChromaDB', 'HuggingFace', 'Groq', 'FastAPI', 'Next.js', 'Python'],
    color: 'from-orange-500 to-red-500',
    icon: Brain
  }
]

export default function CaseStudiesPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-white dark:bg-slate-950 pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-4">
              MachinaWorks Portfolio. Proven Results.
            </h1>
            <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
              Quantitative trading, intelligent gaming AI, and business transformation — delivered by MachinaWorks
            </p>
          </motion.div>

          {/* Case Studies */}
          <div className="space-y-12">
            {caseStudies.map((study, index) => {
              const Icon = study.icon
              return (
                <motion.div
                  key={study.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="card overflow-hidden hover:shadow-xl transition-shadow"
                >
                  <div className="grid lg:grid-cols-3 gap-8">
                    {/* Left: Header & Content */}
                    <div className="lg:col-span-2 space-y-6">
                      <div>
                        <div className="flex items-center space-x-3 mb-3">
                          <div className={`p-3 rounded-lg bg-gradient-to-br ${study.color}`}>
                            <Icon className="w-6 h-6 text-white" />
                          </div>
                          <span className="px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-full text-sm font-medium">
                            {study.category}
                          </span>
                        </div>
                        <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100 mb-2">
                          {study.title}
                        </h2>
                        <p className="text-lg text-slate-600 dark:text-slate-400">{study.description}</p>
                      </div>

                      <div className="space-y-4">
                        <div>
                          <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">Challenge</h3>
                          <p className="text-slate-600 dark:text-slate-400">{study.challenge}</p>
                        </div>
                        <div>
                          <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">Solution</h3>
                          <p className="text-slate-600 dark:text-slate-400">{study.solution}</p>
                        </div>
                      </div>

                      {/* Results */}
                      <div>
                        <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-3">Results</h3>
                        <ul className="space-y-2">
                          {study.results.map((result, idx) => (
                            <li key={idx} className="flex items-start space-x-3">
                              <ArrowUpRight className="w-5 h-5 text-green-600 dark:text-green-500 mt-0.5 flex-shrink-0" />
                              <span className="text-slate-700 dark:text-slate-300">{result}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Tech Stack */}
                      <div>
                        <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-3">Tech Stack</h3>
                        <div className="flex flex-wrap gap-2">
                          {study.tech.map((tech) => (
                            <span
                              key={tech}
                              className="px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                            >
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Right: Key Metrics */}
                    <div className={`bg-gradient-to-br ${study.color} rounded-xl p-8 text-white flex flex-col justify-between`}>
                      <div>
                        <h3 className="text-lg font-bold mb-6 flex items-center space-x-2">
                          <BarChart3 className="w-5 h-5" />
                          <span>Key Metrics</span>
                        </h3>
                        <div className="space-y-4">
                          {Object.entries(study.metrics).map(([key, value]) => (
                            <div key={key}>
                              <p className="text-white/80 text-sm font-medium">{key}</p>
                              <p className="text-2xl font-bold">{value}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div className="pt-6 border-t border-white/20">
                        <p className="text-white/70 text-sm">
                          ✓ Production Ready
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>

          {/* Call to Action */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mt-16 card bg-gradient-to-r from-primary-600 to-accent-600 text-white text-center py-12"
          >
            <h2 className="text-3xl font-bold mb-4">
              Ready to Build Your Next AI Project?
            </h2>
            <p className="text-lg text-white/90 mb-6 max-w-2xl mx-auto">
              Get personalized AI consulting and implementation strategies for your business
            </p>
            <a href="/#consultation" className="inline-block bg-white text-primary-600 hover:bg-slate-100 px-8 py-3 rounded-lg font-semibold hover:shadow-lg transition-all">
              Start Consultation
            </a>
          </motion.div>
        </div>
      </main>
      <Footer />
    </>
  )
}
