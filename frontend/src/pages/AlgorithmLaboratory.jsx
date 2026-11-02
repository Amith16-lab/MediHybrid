import React, { useState, useEffect } from 'react';
import {
  Dna,
  Cpu,
  Layers,
  Eye,
  Sliders,
  TrendingUp,
  Award,
  Activity,
  CheckCircle2
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';
import {
  getGALabData,
  getANNLabData,
  getFuzzyLabData,
  getCNNLabData
} from '../services/api';

export default function AlgorithmLaboratory() {
  const [activeTab, setActiveTab] = useState('ga'); // 'ga', 'ann', 'fuzzy', 'cnn'
  const [gaData, setGaData] = useState(null);
  const [annData, setAnnData] = useState(null);
  const [fuzzyData, setFuzzyData] = useState(null);
  const [cnnData, setCnnData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Sub-selection for disease in GA / ANN / Fuzzy
  const [diseaseTab, setDiseaseTab] = useState('diabetes'); // 'diabetes' or 'heart'

  // Interactive fuzzy playground
  const [fuzzyInputs, setFuzzyInputs] = useState({ glucose: 135, bmi: 28 });

  useEffect(() => {
    Promise.all([getGALabData(), getANNLabData(), getFuzzyLabData(), getCNNLabData()])
      .then(([gaRes, annRes, fuzRes, cnnRes]) => {
        setGaData(gaRes.data);
        setAnnData(annRes.data);
        setFuzzyData(fuzRes.data);
        setCnnData(cnnRes.data);
      })
      .catch((err) => console.error("Error fetching lab data:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="py-20 text-center space-y-3">
        <div className="w-8 h-8 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-sm text-slate-500">Initializing Soft Computing Laboratory...</p>
      </div>
    );
  }

  const currentGA = diseaseTab === 'diabetes' ? gaData?.diabetes : gaData?.heart;
  const currentANN = diseaseTab === 'diabetes' ? annData?.diabetes : annData?.heart;

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      
      {/* Title */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold">
          <Cpu className="w-3.5 h-3.5 text-teal-600" />
          Soft Computing Laboratory & Diagnostics
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-navy-900">
          Algorithm Laboratory
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          Interactive evaluation workbench for Genetic Algorithm feature selection, Artificial Neural Network convergence, 
          Mamdani Fuzzy rule evaluation, and Retinal CNN classification.
        </p>
      </div>

      {/* Main Tabs Navigation */}
      <div className="flex border-b border-slate-200 bg-white p-1 rounded-2xl shadow-sm overflow-x-auto gap-1">
        <button
          onClick={() => setActiveTab('ga')}
          className={`flex-1 min-w-[130px] py-2.5 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
            activeTab === 'ga'
              ? 'bg-navy-900 text-white shadow-sm'
              : 'text-slate-600 hover:text-navy-900 hover:bg-slate-50'
          }`}
        >
          <Dna className="w-4 h-4 text-teal-400" />
          <span>Genetic Algorithm (GA)</span>
        </button>

        <button
          onClick={() => setActiveTab('ann')}
          className={`flex-1 min-w-[130px] py-2.5 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
            activeTab === 'ann'
              ? 'bg-navy-900 text-white shadow-sm'
              : 'text-slate-600 hover:text-navy-900 hover:bg-slate-50'
          }`}
        >
          <Cpu className="w-4 h-4 text-teal-400" />
          <span>Neural Network (ANN)</span>
        </button>

        <button
          onClick={() => setActiveTab('fuzzy')}
          className={`flex-1 min-w-[130px] py-2.5 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
            activeTab === 'fuzzy'
              ? 'bg-navy-900 text-white shadow-sm'
              : 'text-slate-600 hover:text-navy-900 hover:bg-slate-50'
          }`}
        >
          <Layers className="w-4 h-4 text-teal-400" />
          <span>Fuzzy Logic (Mamdani)</span>
        </button>

        <button
          onClick={() => setActiveTab('cnn')}
          className={`flex-1 min-w-[130px] py-2.5 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
            activeTab === 'cnn'
              ? 'bg-navy-900 text-white shadow-sm'
              : 'text-slate-600 hover:text-navy-900 hover:bg-slate-50'
          }`}
        >
          <Eye className="w-4 h-4 text-teal-400" />
          <span>Retinal CNN (APTOS)</span>
        </button>
      </div>

      {/* Disease Sub-Selector (For GA, ANN, Fuzzy) */}
      {activeTab !== 'cnn' && (
        <div className="flex justify-between items-center bg-slate-100 p-1.5 rounded-xl max-w-sm">
          <button
            onClick={() => setDiseaseTab('diabetes')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              diseaseTab === 'diabetes' ? 'bg-white text-navy-900 shadow-sm' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Diabetes Pipeline (8 Features)
          </button>
          <button
            onClick={() => setDiseaseTab('heart')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              diseaseTab === 'heart' ? 'bg-white text-navy-900 shadow-sm' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Heart Disease Pipeline (13 Features)
          </button>
        </div>
      )}

      {/* TAB 1: GENETIC ALGORITHM */}
      {activeTab === 'ga' && currentGA && (
        <div className="space-y-6">
          
          {/* Chromosome & Hyperparameters Card */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-navy-900 uppercase tracking-wider flex items-center gap-2">
              <Dna className="w-4 h-4 text-teal-600" />
              DEAP Binary Chromosome Encoding
            </h3>

            {/* Binary Bit Array Display */}
            <div className="bg-slate-900 p-4 rounded-2xl space-y-2">
              <span className="text-[11px] text-slate-400 font-mono block">Optimal Individual Chromosome (Bitstring):</span>
              <div className="flex flex-wrap gap-2">
                {currentGA.all_features?.map((feat, idx) => {
                  const isActive = currentGA.chromosome[idx] === 1;
                  return (
                    <div
                      key={idx}
                      className={`px-3 py-2 rounded-xl text-center font-mono border ${
                        isActive
                          ? 'bg-teal-500/20 border-teal-400 text-teal-300'
                          : 'bg-slate-800/60 border-slate-700 text-slate-500'
                      }`}
                    >
                      <div className="text-lg font-bold">{currentGA.chromosome[idx]}</div>
                      <div className="text-[10px] mt-0.5 truncate max-w-[90px]">{feat}</div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* GA Parameters */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-xs">
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <span className="text-slate-400 block text-[10px]">Population Size</span>
                <span className="font-bold text-navy-900 text-sm">20 Individuals</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <span className="text-slate-400 block text-[10px]">Generations</span>
                <span className="font-bold text-navy-900 text-sm">10 Generations</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <span className="text-slate-400 block text-[10px]">2-Point Crossover</span>
                <span className="font-bold text-navy-900 text-sm">P_c = 0.60</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <span className="text-slate-400 block text-[10px]">Bit-Flip Mutation</span>
                <span className="font-bold text-navy-900 text-sm">P_m = 0.20</span>
              </div>
            </div>
          </div>

          {/* Fitness Evolution Chart */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div>
              <h3 className="font-bold text-sm text-navy-900">GA Fitness Evolution Across Generations</h3>
              <p className="text-[11px] text-slate-500">Evaluates 5-fold cross-validated ROC-AUC on training partition</p>
            </div>

            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={currentGA.evolution_history}
                  margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis
                    dataKey="generation"
                    label={{ value: 'Generation', position: 'insideBottom', offset: -4, fontSize: 11 }}
                    tick={{ fontSize: 11 }}
                  />
                  <YAxis domain={['auto', 'auto']} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(val) => [val, 'Best Fitness (CV AUC)']} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="best_fitness"
                    name="Best Generation Fitness"
                    stroke="#0d9488"
                    strokeWidth={2.5}
                    dot={{ r: 4, fill: '#0d9488' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="text-xs text-slate-600 bg-teal-50/60 p-3.5 rounded-xl border border-teal-100 flex items-center justify-between">
              <span>Selected Feature Subset: <strong>{currentGA.selected_count} / {currentGA.total_features} active</strong></span>
              <span className="font-bold text-teal-800">Pruning Rate: {Math.round((1 - currentGA.selected_count / currentGA.total_features) * 100)}%</span>
            </div>
          </div>

        </div>
      )}

      {/* TAB 2: ARTIFICIAL NEURAL NETWORK */}
      {activeTab === 'ann' && currentANN && (
        <div className="space-y-6">
          
          {/* Architecture & Evaluation Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div className="md:col-span-1 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="text-xs font-bold text-navy-900 uppercase tracking-wider">ANN Architecture</h3>
              
              <div className="space-y-2 text-xs">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <span className="text-slate-400 block text-[10px]">Input Layer</span>
                  <span className="font-bold text-navy-900 font-mono">{currentANN.architecture.input_dim} Nodes (GA Features)</span>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <span className="text-slate-400 block text-[10px]">Hidden Layers</span>
                  <span className="font-bold text-navy-900 font-mono">Layer 1: 32 (ReLU) • Layer 2: 16 (ReLU)</span>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <span className="text-slate-400 block text-[10px]">Output Layer</span>
                  <span className="font-bold text-navy-900 font-mono">1 Node (Sigmoid Probability)</span>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <span className="text-slate-400 block text-[10px]">Optimizer & Iterations</span>
                  <span className="font-bold text-navy-900 font-mono">{currentANN.architecture.optimizer} ({currentANN.architecture.iterations_completed} epochs)</span>
                </div>
              </div>
            </div>

            {/* Test Metrics & Confusion Matrix */}
            <div className="md:col-span-2 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="text-xs font-bold text-navy-900 uppercase tracking-wider">Holdout Set Evaluation</h3>

              <div className="grid grid-cols-3 sm:grid-cols-5 gap-2 text-center text-xs">
                <div className="p-3 bg-teal-50 rounded-xl border border-teal-100">
                  <span className="text-slate-500 block text-[10px]">Accuracy</span>
                  <span className="font-black text-teal-800 text-sm">{(currentANN.test_metrics.accuracy * 100).toFixed(1)}%</span>
                </div>
                <div className="p-3 bg-teal-50 rounded-xl border border-teal-100">
                  <span className="text-slate-500 block text-[10px]">ROC-AUC</span>
                  <span className="font-black text-teal-800 text-sm">{currentANN.test_metrics.roc_auc}</span>
                </div>
                <div className="p-3 bg-teal-50 rounded-xl border border-teal-100">
                  <span className="text-slate-500 block text-[10px]">Precision</span>
                  <span className="font-black text-teal-800 text-sm">{(currentANN.test_metrics.precision * 100).toFixed(1)}%</span>
                </div>
                <div className="p-3 bg-teal-50 rounded-xl border border-teal-100">
                  <span className="text-slate-500 block text-[10px]">Recall</span>
                  <span className="font-black text-teal-800 text-sm">{(currentANN.test_metrics.recall * 100).toFixed(1)}%</span>
                </div>
                <div className="p-3 bg-teal-50 rounded-xl border border-teal-100">
                  <span className="text-slate-500 block text-[10px]">F1-Score</span>
                  <span className="font-black text-teal-800 text-sm">{currentANN.test_metrics.f1_score}</span>
                </div>
              </div>

              {/* Confusion Matrix Table */}
              <div className="pt-2">
                <span className="text-xs font-bold text-navy-900 block mb-2">Confusion Matrix (Holdout Test Set):</span>
                <div className="grid grid-cols-2 gap-2 text-center text-xs max-w-sm mx-auto">
                  <div className="bg-emerald-50 border border-emerald-200 p-3 rounded-xl">
                    <span className="text-[10px] text-emerald-800 block">True Negatives (TN)</span>
                    <span className="text-lg font-black text-emerald-900">{currentANN.confusion_matrix.true_negatives}</span>
                  </div>
                  <div className="bg-amber-50 border border-amber-200 p-3 rounded-xl">
                    <span className="text-[10px] text-amber-800 block">False Positives (FP)</span>
                    <span className="text-lg font-black text-amber-900">{currentANN.confusion_matrix.false_positives}</span>
                  </div>
                  <div className="bg-amber-50 border border-amber-200 p-3 rounded-xl">
                    <span className="text-[10px] text-amber-800 block">False Negatives (FN)</span>
                    <span className="text-lg font-black text-amber-900">{currentANN.confusion_matrix.false_negatives}</span>
                  </div>
                  <div className="bg-emerald-50 border border-emerald-200 p-3 rounded-xl">
                    <span className="text-[10px] text-emerald-800 block">True Positives (TP)</span>
                    <span className="text-lg font-black text-emerald-900">{currentANN.confusion_matrix.true_positives}</span>
                  </div>
                </div>
              </div>

            </div>

          </div>

          {/* Loss Curve */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div>
              <h3 className="font-bold text-sm text-navy-900">Training Loss Curve (Binary Cross-Entropy)</h3>
              <p className="text-[11px] text-slate-500">Monitored convergence with Adam optimizer</p>
            </div>

            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={currentANN.training_curves.loss.map((loss, i) => ({ iteration: i + 1, loss }))}
                  margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="iteration" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="loss" name="Log Loss" stroke="#3b82f6" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      )}

      {/* TAB 3: FUZZY LOGIC */}
      {activeTab === 'fuzzy' && fuzzyData && (
        <div className="space-y-6">
          
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div>
              <h3 className="font-bold text-sm text-navy-900">Mamdani Membership Functions (Triangular & Trapezoidal)</h3>
              <p className="text-[11px] text-slate-500">Continuous fuzzification ranges modeled via scikit-fuzzy</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-2">
                <span className="font-bold text-navy-900 block">Fasting Glucose Linguistic Sets:</span>
                <p>• <strong>Normal</strong>: Trapezoidal [40, 40, 90, 110] mg/dL</p>
                <p>• <strong>Moderate / Borderline</strong>: Triangular [100, 125, 150] mg/dL</p>
                <p>• <strong>High</strong>: Trapezoidal [140, 170, 260, 260] mg/dL</p>
              </div>

              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-2">
                <span className="font-bold text-navy-900 block">Body Mass Index (BMI) Linguistic Sets:</span>
                <p>• <strong>Normal</strong>: Trapezoidal [12, 12, 20, 25] kg/m²</p>
                <p>• <strong>Overweight</strong>: Triangular [24, 27.5, 31] kg/m²</p>
                <p>• <strong>Obese</strong>: Trapezoidal [29, 35, 60, 60] kg/m²</p>
              </div>

              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-2">
                <span className="font-bold text-navy-900 block">Output Risk Defuzzification:</span>
                <p>• <strong>Low Risk</strong>: Trapezoidal [0, 0, 20, 35]%</p>
                <p>• <strong>Moderate Risk</strong>: Triangular [25, 50, 75]%</p>
                <p>• <strong>High Risk</strong>: Trapezoidal [65, 80, 100, 100]%</p>
              </div>

              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-2">
                <span className="font-bold text-navy-900 block">Defuzzification Technique:</span>
                <p>• <strong>Centroid Method (Center of Gravity)</strong></p>
                <p className="font-mono text-[10px] text-teal-700">y* = ∫ y · μ(y) dy / ∫ μ(y) dy</p>
                <p className="text-[10px] text-slate-400">Guarantees mathematically continuous risk transitions.</p>
              </div>

            </div>
          </div>

        </div>
      )}

      {/* TAB 4: CONVOLUTIONAL NEURAL NETWORK */}
      {activeTab === 'cnn' && cnnData && (
        <div className="space-y-6">
          
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-sm text-navy-900">{cnnData.model_name}</h3>
                <p className="text-[11px] text-slate-500">Fine-tuned on {cnnData.dataset}</p>
              </div>
              <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-800 text-xs font-bold border border-blue-200">
                5-Class Ophthalmic CNN
              </span>
            </div>

            {/* Overall CNN Metrics */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs">
              <div className="p-3 bg-blue-50 rounded-xl border border-blue-100">
                <span className="text-slate-500 block text-[10px]">Test Accuracy</span>
                <span className="font-black text-blue-900 text-lg">{(cnnData.overall_metrics.accuracy * 100).toFixed(1)}%</span>
              </div>
              <div className="p-3 bg-teal-50 rounded-xl border border-teal-100">
                <span className="text-slate-500 block text-[10px]">Quadratic Kappa (QWK)</span>
                <span className="font-black text-teal-900 text-lg">{cnnData.overall_metrics.quadratic_weighted_kappa}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-slate-500 block text-[10px]">Macro F1-Score</span>
                <span className="font-black text-navy-900 text-lg">{cnnData.overall_metrics.macro_f1_score}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-slate-500 block text-[10px]">Input Resolution</span>
                <span className="font-black text-navy-900 text-lg">{cnnData.input_resolution}</span>
              </div>
            </div>

            {/* Preprocessing Steps */}
            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-1.5 text-xs">
              <span className="font-bold text-navy-900 block">Automated Ophthalmic Preprocessing Pipeline:</span>
              {cnnData.preprocessing_pipeline?.map((step, idx) => (
                <p key={idx} className="text-slate-600 font-mono text-[11px]">{step}</p>
              ))}
            </div>

            {/* 5x5 Confusion Matrix */}
            <div className="space-y-2 pt-2">
              <span className="text-xs font-bold text-navy-900 block">APTOS 2019 5x5 Confusion Matrix:</span>
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-center border-collapse">
                  <thead>
                    <tr className="bg-slate-100 text-slate-700 text-[10px]">
                      <th className="p-2 border">Actual \ Pred</th>
                      <th className="p-2 border">Class 0</th>
                      <th className="p-2 border">Class 1</th>
                      <th className="p-2 border">Class 2</th>
                      <th className="p-2 border">Class 3</th>
                      <th className="p-2 border">Class 4</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cnnData.confusion_matrix?.map((row, rIdx) => (
                      <tr key={rIdx}>
                        <td className="p-2 border font-bold text-slate-700 bg-slate-50 text-[10px]">Class {rIdx}</td>
                        {row.map((cell, cIdx) => (
                          <td
                            key={cIdx}
                            className={`p-2 border font-mono ${
                              rIdx === cIdx ? 'bg-emerald-100 font-bold text-emerald-900' : 'text-slate-600'
                            }`}
                          >
                            {cell}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}
