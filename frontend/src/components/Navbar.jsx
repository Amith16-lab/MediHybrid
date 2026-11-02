import React, { useState, useEffect } from 'react';
import { NavLink, Link } from 'react-router-dom';
import {
  Activity,
  Heart,
  Eye,
  FileText,
  FlaskConical,
  History,
  Bot,
  LayoutDashboard,
  Menu,
  X
} from 'lucide-react';
import { healthCheck } from '../services/api';

export default function Navbar({ onOpenBot }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isHealthy, setIsHealthy] = useState(true);

  useEffect(() => {
    healthCheck()
      .then(() => setIsHealthy(true))
      .catch(() => setIsHealthy(false));
  }, []);

  const navLinks = [
    { to: '/', label: 'Home', icon: null },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/diabetes', label: 'Diabetes', icon: Activity },
    { to: '/heart', label: 'Heart Disease', icon: Heart },
    { to: '/retina', label: 'RetinaScan', icon: Eye },
    { to: '/laboratory', label: 'Algorithm Lab', icon: FlaskConical },
    { to: '/history', label: 'History', icon: History },
  ];

  return (
    <header className="sticky top-0 z-40 bg-navy-900/95 backdrop-blur-md border-b border-navy-700 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo / Brand */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-teal-400 flex items-center justify-center text-navy-900 shadow-md group-hover:scale-105 transition-transform">
              <Activity className="w-6 h-6 stroke-[2.5]" />
            </div>
            <div>
              <div className="font-extrabold text-xl tracking-tight text-white flex items-center gap-1.5">
                Medi<span className="text-teal-400">Hybrid</span>
              </div>
              <p className="text-[10px] text-teal-200/80 -mt-0.5 tracking-wider uppercase font-medium">
                Intelligent Healthcare System
              </p>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <nav className="hidden lg:flex items-center space-x-1">
            {navLinks.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                    isActive
                      ? 'bg-teal-500/20 text-teal-300 border border-teal-500/30'
                      : 'text-slate-300 hover:text-white hover:bg-navy-800'
                  }`
                }
              >
                {item.icon && <item.icon className="w-4 h-4 opacity-75" />}
                {item.label}
              </NavLink>
            ))}
          </nav>

          {/* Right Action Buttons */}
          <div className="hidden sm:flex items-center space-x-3">
            {/* System Status Pill */}
            <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-navy-800 border border-navy-700 text-xs">
              <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`}></span>
              <span className="text-slate-300">{isHealthy ? 'Models Active' : 'Offline'}</span>
            </div>

            {/* MediBot Drawer Toggle Button */}
            <button
              onClick={onOpenBot}
              className="px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-navy-900 font-semibold text-sm flex items-center gap-1.5 transition-all shadow-sm hover:shadow"
              title="Open MediBot AI Health Assistant"
            >
              <Bot className="w-4 h-4 text-navy-900" />
              <span>MediBot AI</span>
            </button>
          </div>

          {/* Mobile Menu Toggle Button */}
          <div className="flex lg:hidden items-center gap-2">
            <button
              onClick={onOpenBot}
              className="p-2 rounded-lg bg-teal-600 text-navy-900 font-bold"
              title="Open MediBot"
            >
              <Bot className="w-5 h-5" />
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-300 hover:text-white hover:bg-navy-800"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Nav Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-navy-700 bg-navy-900 px-4 pt-2 pb-4 space-y-1">
          {navLinks.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setMobileMenuOpen(false)}
              className={({ isActive }) =>
                `block px-3 py-2 rounded-md text-base font-medium ${
                  isActive ? 'bg-teal-500/20 text-teal-300' : 'text-slate-300 hover:bg-navy-800 hover:text-white'
                }`
              }
            >
              <div className="flex items-center gap-2">
                {item.icon && <item.icon className="w-5 h-5" />}
                {item.label}
              </div>
            </NavLink>
          ))}
        </div>
      )}
    </header>
  );
}
