import Link from 'next/link'
import { Brain } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-slate-900 dark:bg-slate-950 text-white border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col md:flex-row justify-between items-center">
          {/* Brand */}
          <Link href="/" className="flex items-center space-x-2 mb-6 md:mb-0">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-accent-600 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="font-semibold">MachinaWorks</span>
          </Link>

          {/* Main Links */}
          <div className="flex flex-wrap gap-6 justify-center md:justify-end text-sm">
            <Link href="/#how-it-works" className="text-slate-400 hover:text-white transition-colors">
              How It Works
            </Link>
            <Link href="/case-studies" className="text-slate-400 hover:text-white transition-colors">
              Case Studies
            </Link>
            <Link href="/about" className="text-slate-400 hover:text-white transition-colors">
              About
            </Link>
          </div>
        </div>

        <div className="border-t border-slate-800 mt-8 pt-8 text-center text-slate-400 text-sm">
          <p>© {new Date().getFullYear()} MachinaWorks. Building AI solutions for Indian businesses.</p>
        </div>
      </div>
    </footer>
  )
}
