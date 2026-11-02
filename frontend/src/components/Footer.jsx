import React from 'react';
import { Activity, ShieldAlert, Cpu } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-navy-900 border-t border-navy-800 text-slate-400 text-xs py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center border-b border-navy-800 pb-6 mb-6">
          
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-teal-500/20 border border-teal-500/30 flex items-center justify-center text-teal-400">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <p className="font-bold text-white text-sm">MediHybrid — Clinical Decision Support Engine</p>
              <p className="text-slate-400">Integrated Soft Computing & Deep Vision Architecture</p>
            </div>
          </div>

          <div className="flex items-center space-x-2 text-slate-300">
            <Cpu className="w-4 h-4 text-teal-400 shrink-0" />
            <span>GA (DEAP) • ANN (ReLU/Adam) • Mamdani Fuzzy • CNN (APTOS 2019)</span>
          </div>

          <div className="flex md:justify-end items-center text-amber-300/80 gap-2">
            <ShieldAlert className="w-4 h-4 shrink-0" />
            <span>Educational Research Prototype — Not for Clinical Diagnosis</span>
          </div>

        </div>

        <div className="flex flex-col sm:flex-row justify-between items-center text-slate-500 gap-2">
          <p>© {new Date().getFullYear()} MediHybrid Research Group. All rights reserved.</p>
          <p>Integrated Soft Computing Architecture: Genetic Algorithm + Neural Network + Fuzzy Logic + Vision CNN</p>
        </div>
      </div>
    </footer>
  );
}
