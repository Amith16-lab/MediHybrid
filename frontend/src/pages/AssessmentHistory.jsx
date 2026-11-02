import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  History,
  FileDown,
  Trash2,
  Filter,
  Eye,
  Activity,
  Heart,
  Calendar,
  AlertCircle
} from 'lucide-react';
import { getAssessmentHistory, deleteAssessment } from '../services/api';

export default function AssessmentHistory({ onOpenBotWithContext }) {
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'diabetes', 'heart', 'high'
  const [loading, setLoading] = useState(true);

  const fetchHistory = () => {
    setLoading(true);
    getAssessmentHistory()
      .then((res) => setRecords(res.data || []))
      .catch((err) => console.error("Error loading history:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm(`Delete assessment record #${id}?`)) return;
    try {
      await deleteAssessment(id);
      setRecords((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      alert("Failed to delete record.");
    }
  };

  const handleExportCSV = () => {
    if (records.length === 0) return;
    const headers = ["ID", "Type", "ANN_Score", "Fuzzy_Score", "Hybrid_Score", "Category", "Date"];
    const rows = records.map((r) => [
      r.id,
      r.type,
      r.ann_score,
      r.fuzzy_score,
      r.hybrid_score,
      `"${r.category}"`,
      r.created_at
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `medihybrid_assessment_audit_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleView = (r) => {
    const payload = {
      record_id: r.id,
      disease: r.type === 'diabetes' ? 'Diabetes Risk Assessment' : 'Heart Disease Risk Assessment',
      hybrid: { score: r.hybrid_score, category: r.category, recommendation: "Recorded assessment from history archive." },
      ann: { score: r.ann_score },
      fuzzy: { fuzzy_score: r.fuzzy_score },
      inputs: r.input_values,
      ga_selected_features: r.selected_features || [],
      explainability: []
    };
    navigate('/results', { state: { result: payload } });
  };

  const filteredRecords = records.filter((r) => {
    if (filter === 'diabetes') return r.type === 'diabetes';
    if (filter === 'heart') return r.type === 'heart';
    if (filter === 'high') return r.hybrid_score >= 65.0;
    return true;
  });

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-navy-900">
            Assessment Audit History
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-1">
            Complete database of past patient assessments with 1-click re-evaluation and CSV export.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          disabled={records.length === 0}
          className="px-3.5 py-2 rounded-xl bg-navy-900 hover:bg-navy-800 disabled:opacity-50 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm transition-all"
        >
          <FileDown className="w-4 h-4 text-teal-400" />
          <span>Export Audit CSV</span>
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 text-xs">
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1.5 rounded-lg font-semibold transition-colors ${
            filter === 'all' ? 'bg-navy-900 text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          All Records ({records.length})
        </button>
        <button
          onClick={() => setFilter('diabetes')}
          className={`px-3 py-1.5 rounded-lg font-semibold transition-colors ${
            filter === 'diabetes' ? 'bg-navy-900 text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          Diabetes Only
        </button>
        <button
          onClick={() => setFilter('heart')}
          className={`px-3 py-1.5 rounded-lg font-semibold transition-colors ${
            filter === 'heart' ? 'bg-navy-900 text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          Heart Disease Only
        </button>
        <button
          onClick={() => setFilter('high')}
          className={`px-3 py-1.5 rounded-lg font-semibold transition-colors ${
            filter === 'high' ? 'bg-navy-900 text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          }`}
        >
          Elevated Risk Only
        </button>
      </div>

      {/* Records Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="py-20 text-center space-y-2">
            <div className="w-8 h-8 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="text-xs text-slate-500">Querying database records...</p>
          </div>
        ) : filteredRecords.length === 0 ? (
          <div className="py-20 text-center text-slate-400 text-xs">
            No assessment records match this filter. Run a clinical evaluation first!
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4 font-semibold">ID</th>
                  <th className="py-3 px-4 font-semibold">Assessment Type</th>
                  <th className="py-3 px-4 font-semibold">ANN Score</th>
                  <th className="py-3 px-4 font-semibold">Fuzzy Score</th>
                  <th className="py-3 px-4 font-semibold">Hybrid Score</th>
                  <th className="py-3 px-4 font-semibold">Risk Category</th>
                  <th className="py-3 px-4 font-semibold">Timestamp</th>
                  <th className="py-3 px-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredRecords.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-3 px-4 font-mono font-medium text-slate-800">#{r.id}</td>
                    <td className="py-3 px-4 font-bold text-navy-900 uppercase flex items-center gap-1.5">
                      {r.type === 'diabetes' ? (
                        <Activity className="w-3.5 h-3.5 text-teal-600" />
                      ) : (
                        <Heart className="w-3.5 h-3.5 text-rose-500" />
                      )}
                      <span>{r.type}</span>
                    </td>
                    <td className="py-3 px-4 font-mono">{r.ann_score}%</td>
                    <td className="py-3 px-4 font-mono">{r.fuzzy_score}%</td>
                    <td className="py-3 px-4 font-mono font-bold text-teal-700 text-sm">
                      {r.hybrid_score}%
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        r.hybrid_score < 35.0 ? 'bg-emerald-100 text-emerald-800' : (
                          r.hybrid_score < 65.0 ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800'
                        )
                      }`}>
                        {r.category}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">
                      {new Date(r.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                    </td>
                    <td className="py-3 px-4 text-right space-x-1">
                      <button
                        onClick={() => handleView(r)}
                        className="p-1.5 rounded-lg text-slate-500 hover:text-navy-900 hover:bg-slate-100"
                        title="View Full Diagnosis"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => window.open(`/api/reports/download/${r.id}`, '_blank')}
                        className="p-1.5 rounded-lg text-slate-500 hover:text-teal-700 hover:bg-slate-100"
                        title="Download PDF"
                      >
                        <FileDown className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(r.id)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50"
                        title="Delete Record"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
}
