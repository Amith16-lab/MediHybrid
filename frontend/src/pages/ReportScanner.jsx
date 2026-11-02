import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileText,
  Upload,
  Sparkles,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  ArrowRight,
  ShieldCheck,
  Edit3
} from 'lucide-react';
import { extractMedicalReport } from '../services/api';

export default function ReportScanner() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [extractedData, setExtractedData] = useState(null);
  const [error, setError] = useState(null);

  // Editable fields state
  const [verifiedValues, setVerifiedValues] = useState({
    glucose: 136,
    cholesterol: 218,
    systolic_bp: 134,
    diastolic_bp: 82,
    bmi: 28.6,
    age: 48
  });

  const sampleReports = [
    {
      name: "Metabolic Profile Sample (PDF)",
      filename: "metabolic_lab_report.pdf",
      text: "METABOLIC LAB REPORT\nPatient Age: 52 Years | Sex: Male\nBlood Pressure (BP): 138/84 mm Hg\nFasting Glucose: 142 mg/dL\nTotal Cholesterol: 228 mg/dL\nBody Mass Index (BMI): 29.4 kg/m2\n"
    },
    {
      name: "Cardiovascular Panel Sample (Image)",
      filename: "cardiac_panel.jpg",
      text: "CARDIOLOGY DIAGNOSTIC REPORT\nAge: 58 | Sex: 1 (Male)\nResting Blood Pressure: 146/88 mm Hg\nSerum Cholesterol: 248 mg/dL\nFasting Blood Sugar: 118 mg/dL\nBMI: 31.2 kg/m2\n"
    }
  ];

  const handleFileUpload = async (uploadedFile) => {
    setFile(uploadedFile);
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const res = await extractMedicalReport(formData);
      setExtractedData(res.data);
      const fields = res.data.extracted_fields || {};
      setVerifiedValues((prev) => ({
        ...prev,
        ...fields
      }));
    } catch (err) {
      setError(err.response?.data?.detail || "Report OCR scanning failed. Please verify the report format.");
    } finally {
      setLoading(false);
    }
  };

  const handleSampleClick = (sample) => {
    const fakeFile = new File([sample.text], sample.filename, {
      type: sample.filename.endsWith('.pdf') ? 'application/pdf' : 'image/jpeg'
    });
    handleFileUpload(fakeFile);
  };

  const handleValueChange = (e) => {
    const { name, value } = e.target;
    setVerifiedValues((prev) => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  const handleTransferToDiabetes = () => {
    navigate('/diabetes', {
      state: {
        prefilled: {
          Glucose: verifiedValues.glucose || 120,
          BMI: verifiedValues.bmi || 25.0,
          BloodPressure: verifiedValues.diastolic_bp || 80,
          Age: verifiedValues.age || 45
        }
      }
    });
  };

  const handleTransferToHeart = () => {
    navigate('/heart', {
      state: {
        prefilled: {
          age: verifiedValues.age || 50,
          chol: verifiedValues.cholesterol || 220,
          trestbps: verifiedValues.systolic_bp || 130
        }
      }
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-16">
      
      {/* Title */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold">
          <FileText className="w-3.5 h-3.5 text-teal-600" />
          OCR Medical Document Intelligence
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-navy-900">
          Medical Report Scanner
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          Upload laboratory test sheets in PDF or image format. MediHybrid extracts verified biomarkers 
          (Fasting Glucose, Cholesterol, BP, BMI, and Age) to populate the clinical prediction forms.
        </p>
      </div>

      {/* Quick Test Samples */}
      <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm space-y-2.5">
        <div className="flex items-center justify-between text-xs">
          <span className="font-bold text-navy-900 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-teal-600" /> Quick Lab Report Templates
          </span>
          <span className="text-[11px] text-slate-400">Click to test OCR parsing</span>
        </div>

        <div className="flex flex-wrap gap-2">
          {sampleReports.map((s, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSampleClick(s)}
              className="px-3.5 py-1.5 rounded-xl border border-slate-200 hover:border-teal-500 hover:bg-teal-50/50 text-xs font-medium text-slate-700 hover:text-teal-700 transition-all flex items-center gap-1.5"
            >
              <FileText className="w-3.5 h-3.5 text-teal-500" />
              <span>{s.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Upload Zone */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files?.[0]) handleFileUpload(e.dataTransfer.files[0]);
          }}
          onDragOver={(e) => e.preventDefault()}
          onClick={() => document.getElementById('report-file-input').click()}
          className="border-2 border-dashed border-slate-300 hover:border-teal-500 rounded-2xl p-8 text-center space-y-3 cursor-pointer transition-colors bg-slate-50/50 hover:bg-teal-50/20"
        >
          <div className="w-12 h-12 rounded-full bg-teal-50 text-teal-600 flex items-center justify-center mx-auto">
            <Upload className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <p className="text-xs font-bold text-navy-900">
              {file ? file.name : "Upload Patient Laboratory Report (PDF, PNG, JPEG)"}
            </p>
            <p className="text-[11px] text-slate-500">Drag & drop report files or click to browse</p>
          </div>
          <input
            id="report-file-input"
            type="file"
            accept=".pdf,image/png,image/jpeg"
            onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
            className="hidden"
          />
        </div>

        {loading && (
          <div className="flex items-center justify-center gap-2 text-xs text-slate-500 py-4">
            <RefreshCw className="w-4 h-4 animate-spin text-teal-600" />
            <span>Parsing document structure and extracting biometric fields...</span>
          </div>
        )}

        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
            <div>
              <p className="font-bold">Extraction Notice</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Verified Extracted Fields Editor */}
        <div className="space-y-4 pt-2 border-t border-slate-100">
          <div className="flex justify-between items-center">
            <h3 className="text-xs font-bold text-navy-900 uppercase tracking-wider flex items-center gap-1.5">
              <Edit3 className="w-3.5 h-3.5 text-teal-600" />
              Verified Clinical Parameters (Editable)
            </h3>
            <span className="text-[11px] text-slate-400">Review & confirm values before submission</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <div className="space-y-1">
              <label className="text-xs font-semibold text-navy-900">Fasting Glucose (mg/dL)</label>
              <input
                type="number"
                name="glucose"
                value={verifiedValues.glucose}
                onChange={handleValueChange}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/50 outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-navy-900">Total Cholesterol (mg/dL)</label>
              <input
                type="number"
                name="cholesterol"
                value={verifiedValues.cholesterol}
                onChange={handleValueChange}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/50 outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-navy-900">Systolic BP (mm Hg)</label>
              <input
                type="number"
                name="systolic_bp"
                value={verifiedValues.systolic_bp}
                onChange={handleValueChange}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/50 outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-navy-900">Diastolic BP (mm Hg)</label>
              <input
                type="number"
                name="diastolic_bp"
                value={verifiedValues.diastolic_bp}
                onChange={handleValueChange}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/50 outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-navy-900">Body Mass Index (BMI)</label>
              <input
                type="number"
                step="0.1"
                name="bmi"
                value={verifiedValues.bmi}
                onChange={handleValueChange}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/50 outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-navy-900">Patient Age (Years)</label>
              <input
                type="number"
                name="age"
                value={verifiedValues.age}
                onChange={handleValueChange}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/50 outline-none"
              />
            </div>

          </div>

          {/* Action Transfer Buttons */}
          <div className="pt-4 flex flex-col sm:flex-row gap-3 justify-end border-t border-slate-100">
            <button
              type="button"
              onClick={handleTransferToDiabetes}
              className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-navy-900 font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm transition-all"
            >
              <span>Transfer to Diabetes Lab</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>

            <button
              type="button"
              onClick={handleTransferToHeart}
              className="px-5 py-2.5 rounded-xl bg-navy-800 hover:bg-navy-700 text-white font-semibold text-xs flex items-center justify-center gap-1.5 transition-all"
            >
              <span>Transfer to Heart Lab</span>
              <ArrowRight className="w-3.5 h-3.5 text-rose-400" />
            </button>
          </div>

        </div>

      </div>

    </div>
  );
}
