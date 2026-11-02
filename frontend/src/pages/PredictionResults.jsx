import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import {
  Activity,
  Heart,
  FileDown,
  Bot,
  RotateCcw,
  CheckCircle,
  AlertTriangle,
  Sliders,
  Dna,
  Cpu,
  Layers,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';

export default function PredictionResults({ onOpenBotWithContext }) {
  const location = useLocation();
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="max-w-2xl mx-auto py-20 text-center space-y-4">
        <Activity className="w-12 h-12 text-slate-300 mx-auto" />
        <h2 className="text-xl font-bold text-navy-900">No Assessment Loaded</h2>
        <p className="text-xs text-slate-500">
          Run an evaluation from the Diabetes Lab or Heart Disease Lab to review predictions.
        </p>
        <div className="pt-2 flex justify-center gap-3">
          <Link to="/diabetes" className="px-4 py-2 rounded-xl bg-teal-600 text-navy-900 text-xs font-bold">
            Diabetes Lab
          </Link>
          <Link to="/heart" className="px-4 py-2 rounded-xl bg-navy-800 text-white text-xs font-semibold">
            Heart Lab
          </Link>
        </div>
      </div>
    );
  }

  const hybrid = result.hybrid || {};
  const ann = result.ann || {};
  const fuzzy = result.fuzzy || {};
  const explain = result.explainability || [];
  const score = hybrid.score || 0;
  const category = hybrid.category || "Evaluated";

  // Score styling
  const getScoreTheme = (s) => {
    if (s < 35.0) return { text: 'text-emerald-700', bg: 'bg-emerald-50 border-emerald-200', tag: 'bg-emerald-100 text-emerald-800' };
    if (s < 65.0) return { text: 'text-amber-700', bg: 'bg-amber-50 border-amber-200', tag: 'bg-amber-100 text-amber-800' };
    return { text: 'text-rose-700', bg: 'bg-rose-50 border-rose-200', tag: 'bg-rose-100 text-rose-800' };
  };

  const theme = getScoreTheme(score);

  const handleDownloadPDF = () => {
    if (result.record_id) {
      window.open(`/api/reports/download/${result.record_id}`, '_blank');
    }
  };

  const handleAskMediBot = () => {
    onOpenBotWithContext(result);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-16 animate-fade-in">
      
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-teal-600 flex items-center gap-1.5">
            <CheckCircle className="w-3.5 h-3.5" /> Soft Computing Inference Complete
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-navy-900 mt-1">
            {result.disease || "Clinical Risk Assessment Results"}
          </h1>
        </div>

        <div className="flex gap-2.5">
          {result.record_id && (
            <button
              onClick={handleDownloadPDF}
              className="px-3.5 py-2 rounded-xl bg-navy-900 hover:bg-navy-800 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm transition-all"
            >
              <FileDown className="w-4 h-4 text-teal-400" />
              <span>Download PDF Report</span>
            </button>
          )}

          <button
            onClick={handleAskMediBot}
            className="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-navy-900 text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all"
          >
            <Bot className="w-4 h-4" />
            <span>Ask MediBot About Results</span>
          </button>
        </div>
      </div>

      {/* Primary Score Hero Card */}
      <div className={`p-6 sm:p-8 rounded-3xl border ${theme.bg} shadow-sm space-y-6`}>
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
          
          <div className="space-y-2">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-500">
              Integrated Hybrid Risk Score
            </span>
            <div className={`text-5xl sm:text-6xl font-black ${theme.text} tracking-tight font-mono`}>
              {score}%
            </div>
            <div className="flex items-center gap-2 justify-center sm:justify-start">
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${theme.tag}`}>
                {category}
              </span>
              <span className="text-xs text-slate-500 font-mono">
                Record #{result.record_id || 'AUTO'}
              </span>
            </div>
          </div>

          {/* Fusion Breakdown Pills */}
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl border border-slate-200/80 space-y-3 min-w-[260px]">
            <div className="text-xs font-bold text-navy-900 uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-100 pb-2">
              <Sliders className="w-3.5 h-3.5 text-teal-600" /> Component Formula Breakdown
            </div>
            
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-600">Neural Network (ANN):</span>
              <span className="font-mono font-bold text-navy-900">{ann.score}% (70%)</span>
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-600">Mamdani Fuzzy Logic:</span>
              <span className="font-mono font-bold text-navy-900">{fuzzy.fuzzy_score}% (30%)</span>
            </div>

            <div className="pt-1 text-[10px] text-slate-400 border-t border-slate-100 font-mono">
              Hybrid = (0.70 × {ann.score}) + (0.30 × {fuzzy.fuzzy_score}) = {score}%
            </div>
          </div>

        </div>

        {/* Clinical Recommendation Text */}
        <div className="bg-white/90 p-4 rounded-2xl border border-slate-200/80 text-xs text-slate-700 leading-relaxed">
          <strong className="text-navy-900 block font-semibold mb-1">Clinical Interpretation:</strong>
          {hybrid.recommendation}
        </div>
      </div>

      {/* GA Selected Features and Active Fuzzy Rules */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* GA Selected Feature Subset */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
              <Dna className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-xs uppercase tracking-wider text-navy-900">
                Genetic Algorithm Selected Features
              </h3>
              <p className="text-[11px] text-slate-400">Features selected by DEAP evolution</p>
            </div>
          </div>

          <div className="flex flex-wrap gap-1.5 pt-1">
            {result.ga_selected_features?.map((feat, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-lg bg-teal-50 border border-teal-200 text-teal-800 font-semibold text-xs flex items-center gap-1"
              >
                ✓ {feat}
              </span>
            ))}
          </div>
          <p className="text-[11px] text-slate-500 pt-1">
            The neural network classifier strictly takes these optimized inputs to prevent noise and overfitting.
          </p>
        </div>

        {/* Active Fuzzy Linguistic Rules */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Layers className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-xs uppercase tracking-wider text-navy-900">
                Active Mamdani Fuzzy Rules
              </h3>
              <p className="text-[11px] text-slate-400">Rule firings contributing to defuzzified score</p>
            </div>
          </div>

          <div className="space-y-1.5 pt-1">
            {fuzzy.active_rules?.map((rule, idx) => (
              <div key={idx} className="p-2 rounded-xl bg-slate-50 border border-slate-100 text-[11px] text-slate-700 leading-snug">
                {rule}
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Explainable AI (XAI) Biomarker Impacts Table */}
      {explain.length > 0 && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div>
            <h3 className="font-bold text-sm text-navy-900">
              Explainable AI (XAI) Biomarker Attribution
            </h3>
            <p className="text-[11px] text-slate-500">
              Evaluates how each patient parameter deviates from clinical healthy baselines.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3 font-semibold">Biomarker</th>
                  <th className="py-2.5 px-3 font-semibold">Value</th>
                  <th className="py-2.5 px-3 font-semibold">GA Active</th>
                  <th className="py-2.5 px-3 font-semibold">Baseline Ref</th>
                  <th className="py-2.5 px-3 font-semibold">Attribution Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {explain.map((f, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/60">
                    <td className="py-2.5 px-3 font-medium text-navy-900">{f.label}</td>
                    <td className="py-2.5 px-3 font-mono font-bold text-slate-800">
                      {f.value} {f.unit}
                    </td>
                    <td className="py-2.5 px-3">
                      {f.ga_selected ? (
                        <span className="text-[10px] font-bold text-teal-700 bg-teal-50 px-1.5 py-0.5 rounded border border-teal-200">
                          Selected
                        </span>
                      ) : (
                        <span className="text-[10px] text-slate-400">Pruned</span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-slate-500 font-mono">{f.reference} {f.unit}</td>
                    <td className="py-2.5 px-3">
                      {f.is_risk_factor ? (
                        <span className="text-rose-600 font-semibold flex items-center gap-1 text-[11px]">
                          ↑ Risk Factor
                        </span>
                      ) : f.is_protective ? (
                        <span className="text-emerald-600 font-semibold flex items-center gap-1 text-[11px]">
                          ↓ Protective
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px]">Neutral</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Action Footer */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-2">
        <Link
          to="/"
          className="text-xs font-semibold text-slate-600 hover:text-navy-900 flex items-center gap-1"
        >
          ← Return to Dashboard
        </Link>

        <div className="flex gap-2">
          <Link
            to="/diabetes"
            className="px-4 py-2 rounded-xl border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-slate-50"
          >
            New Diabetes Test
          </Link>
          <Link
            to="/heart"
            className="px-4 py-2 rounded-xl border border-slate-300 text-xs font-semibold text-slate-700 hover:bg-slate-50"
          >
            New Heart Disease Test
          </Link>
        </div>
      </div>

    </div>
  );
}
