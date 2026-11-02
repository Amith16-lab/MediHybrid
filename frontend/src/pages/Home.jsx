import React from 'react';
import { Link } from 'react-router-dom';
import {
  Activity,
  Heart,
  Eye,
  Bot,
  History,
  FlaskConical,
  Dna,
  Cpu,
  Layers,
  ArrowRight,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';

export default function Home({ onOpenBot }) {
  return (
    <div className="space-y-16 pb-16 animate-fade-in">
      
      {/* Hero Section with Medical Background Visual */}
      <section className="relative overflow-hidden bg-gradient-to-br from-navy-950 via-navy-900 to-slate-900 text-white rounded-3xl p-8 sm:p-14 border border-navy-700/80 shadow-2xl">
        {/* Subtle Decorative Grid & Glow Background */}
        <div className="absolute inset-0 bg-[radial-gradient(#14b8a6_1px,transparent_1px)] [background-size:24px_24px] opacity-10 pointer-events-none"></div>
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-1/3 -mb-20 w-80 h-80 bg-cyan-600/20 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-teal-500/15 border border-teal-500/30 text-teal-300 text-xs font-semibold uppercase tracking-wider shadow-sm">
            <Cpu className="w-3.5 h-3.5 text-teal-400" />
            Intelligent Hybrid Clinical Platform
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            Medi<span className="text-teal-400">Hybrid</span>: Precision Healthcare Intelligence
          </h1>

          <p className="text-slate-300 text-base sm:text-lg leading-relaxed font-light">
            An advanced clinical decision support system bridging probabilistic deep learning with transparent rule-based symbolic reasoning: 
            <strong className="text-white font-medium"> Genetic Algorithm</strong> for biomarker selection, 
            <strong className="text-white font-medium"> Artificial Neural Network (ANN)</strong> for risk patterns, 
            <strong className="text-white font-medium"> Mamdani Fuzzy Inference</strong> for clinical vagueness, and 
            <strong className="text-white font-medium"> CNN with Grad-CAM</strong> for diabetic retinopathy fundus evaluation.
          </p>

          <div className="flex flex-wrap gap-3.5 pt-2">
            <Link
              to="/diabetes"
              className="px-5 py-3 rounded-xl bg-teal-500 hover:bg-teal-400 text-navy-950 font-bold text-sm flex items-center gap-2 shadow-lg hover:shadow-teal-500/25 transition-all transform hover:-translate-y-0.5"
            >
              <Activity className="w-4 h-4" />
              <span>Diabetes Assessment</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              to="/heart"
              className="px-5 py-3 rounded-xl bg-navy-800/90 hover:bg-navy-800 text-white border border-navy-600/80 font-semibold text-sm flex items-center gap-2 transition-all transform hover:-translate-y-0.5 hover:border-rose-400/50"
            >
              <Heart className="w-4 h-4 text-rose-400" />
              <span>Heart Disease Assessment</span>
            </Link>

            <Link
              to="/retina"
              className="px-5 py-3 rounded-xl bg-navy-800/90 hover:bg-navy-800 text-white border border-navy-600/80 font-semibold text-sm flex items-center gap-2 transition-all transform hover:-translate-y-0.5 hover:border-teal-400/50"
            >
              <Eye className="w-4 h-4 text-teal-400" />
              <span>RetinaScan CNN</span>
            </Link>
          </div>

          <div className="pt-4 flex flex-wrap items-center gap-6 text-xs text-slate-400 border-t border-navy-800/80">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-teal-400" /> Real Test Set Inferences
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-teal-400" /> Explainable AI (XAI)
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-teal-400" /> Authenticated Eye Fundus Vision
            </span>
          </div>
        </div>
      </section>

      {/* 3 Core Intelligent Modules Grid */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-navy-900 tracking-tight">
            Three Core Intelligent Modules
          </h2>
          <p className="text-slate-600 text-sm">
            Combining multi-objective feature optimization, neural pattern classification, fuzzy logic, and ophthalmic computer vision.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Module 1: GA + ANN + Fuzzy */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-600">
                <Dna className="w-6 h-6" />
              </div>
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-teal-600">Module 1</span>
                <h3 className="text-lg font-bold text-navy-900">Hybrid Tabular Prediction</h3>
              </div>
              <p className="text-slate-600 text-xs leading-relaxed">
                Dual pipeline for Diabetes and Heart Disease. Uses <strong>DEAP Genetic Algorithm</strong> for biomarker selection, an <strong>MLP Neural Network</strong> for pattern classification, and a <strong>Mamdani Fuzzy System</strong> for clinical ambiguity.
              </p>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs text-slate-700 font-mono">
                Hybrid Score = 0.70·ANN + 0.30·Fuzzy
              </div>
            </div>
            <div className="pt-6 flex gap-2">
              <Link to="/diabetes" className="text-xs font-semibold text-teal-600 hover:text-teal-700 flex items-center gap-1">
                Diabetes Lab →
              </Link>
              <span className="text-slate-300">•</span>
              <Link to="/heart" className="text-xs font-semibold text-teal-600 hover:text-teal-700 flex items-center gap-1">
                Heart Lab →
              </Link>
            </div>
          </div>

          {/* Module 2: CNN RetinaScan */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-cyan-50 border border-cyan-100 flex items-center justify-center text-cyan-600">
                <Eye className="w-6 h-6" />
              </div>
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-cyan-600">Module 2</span>
                <h3 className="text-lg font-bold text-navy-900">Diabetic Retinopathy CNN</h3>
              </div>
              <p className="text-slate-600 text-xs leading-relaxed">
                Trained on the <strong>APTOS 2019 Blindness Detection</strong> dataset with biometric fundus verification. Analyzes retinal imagery across 5 severity classes (No DR to Proliferative DR) with <strong>Grad-CAM</strong> visual attention heatmaps.
              </p>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs text-slate-700 space-y-1">
                <div className="flex justify-between">
                  <span>Quadratic Kappa (QWK):</span>
                  <span className="font-bold text-navy-900">0.9335</span>
                </div>
                <div className="flex justify-between">
                  <span>Test Accuracy:</span>
                  <span className="font-bold text-navy-900">84.15%</span>
                </div>
              </div>
            </div>
            <div className="pt-6">
              <Link to="/retina" className="text-xs font-semibold text-cyan-600 hover:text-cyan-700 flex items-center gap-1">
                Launch RetinaScan CNN →
              </Link>
            </div>
          </div>

          {/* Module 3: MediBot AI Assistant */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600">
                <Bot className="w-6 h-6" />
              </div>
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-purple-600">Module 3</span>
                <h3 className="text-lg font-bold text-navy-900">MediBot AI Assistant</h3>
              </div>
              <p className="text-slate-600 text-xs leading-relaxed">
                A context-aware intelligent clinical assistant that answers healthcare questions, interprets personal model predictions, explains biometric terms, and breaks down soft-computing algorithms.
              </p>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs text-slate-700">
                Interactive queries: <em>"Explain my risk factors"</em> or <em>"How does the fuzzy system work?"</em>
              </div>
            </div>
            <div className="pt-6">
              <button
                onClick={onOpenBot}
                className="text-xs font-semibold text-purple-600 hover:text-purple-700 flex items-center gap-1"
              >
                Chat with MediBot →
              </button>
            </div>
          </div>

        </div>
      </section>

      {/* Quick Tool Cards: Algorithm Lab & Assessment History */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-navy-950 to-navy-900 text-white rounded-2xl p-7 border border-navy-800 shadow-md flex items-start gap-4">
          <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 flex items-center justify-center shrink-0">
            <FlaskConical className="w-5 h-5" />
          </div>
          <div className="space-y-2">
            <h3 className="font-bold text-base">Interactive Algorithm Laboratory</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Inspect live GA chromosome masks, ANN loss curves, 5-class confusion matrices, and interactive Mamdani fuzzy membership function graphs.
            </p>
            <Link to="/laboratory" className="inline-block text-xs font-semibold text-teal-300 hover:text-teal-200 pt-1">
              Explore Algorithm Lab →
            </Link>
          </div>
        </div>

        <div className="bg-gradient-to-br from-navy-950 to-navy-900 text-white rounded-2xl p-7 border border-navy-800 shadow-md flex items-start gap-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center shrink-0">
            <History className="w-5 h-5" />
          </div>
          <div className="space-y-2">
            <h3 className="font-bold text-base">Patient Assessment History</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Review all previously evaluated risk assessments, compare neural network vs fuzzy risk progression, and export comprehensive clinical PDF reports.
            </p>
            <Link to="/history" className="inline-block text-xs font-semibold text-cyan-300 hover:text-cyan-200 pt-1">
              View Assessment Records →
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}
