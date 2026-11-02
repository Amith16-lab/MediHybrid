import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import MediBotDrawer from './components/MediBotDrawer';

import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import DiabetesAssessment from './pages/DiabetesAssessment';
import HeartAssessment from './pages/HeartAssessment';
import RetinaScan from './pages/RetinaScan';
import AlgorithmLaboratory from './pages/AlgorithmLaboratory';
import PredictionResults from './pages/PredictionResults';
import AssessmentHistory from './pages/AssessmentHistory';

export default function App() {
  const [isBotOpen, setIsBotOpen] = useState(false);
  const [activeContext, setActiveContext] = useState(null);

  const handleAssessmentCompleted = (resultData) => {
    setActiveContext(resultData);
  };

  const handleOpenBotWithContext = (contextData) => {
    setActiveContext(contextData);
    setIsBotOpen(true);
  };

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen bg-slate-50 text-slate-800">
        
        {/* Navigation Bar */}
        <Navbar onOpenBot={() => setIsBotOpen(true)} />

        {/* Main Content Area */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8">
          <Routes>
            <Route path="/" element={<Home onOpenBot={() => setIsBotOpen(true)} />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route
              path="/diabetes"
              element={<DiabetesAssessment onAssessmentCompleted={handleAssessmentCompleted} />}
            />
            <Route
              path="/heart"
              element={<HeartAssessment onAssessmentCompleted={handleAssessmentCompleted} />}
            />
            <Route
              path="/retina"
              element={<RetinaScan onRetinaCompleted={handleAssessmentCompleted} />}
            />
            <Route path="/laboratory" element={<AlgorithmLaboratory />} />
            <Route
              path="/results"
              element={<PredictionResults onOpenBotWithContext={handleOpenBotWithContext} />}
            />
            <Route
              path="/history"
              element={<AssessmentHistory onOpenBotWithContext={handleOpenBotWithContext} />}
            />
          </Routes>
        </main>

        {/* Floating Quick Action Button for MediBot on bottom-right of viewport */}
        <div className="fixed bottom-6 right-6 z-30">
          <button
            onClick={() => setIsBotOpen(true)}
            className="group flex items-center gap-2.5 px-4 py-3 rounded-full bg-navy-900 hover:bg-navy-800 text-white font-bold text-xs shadow-xl border border-navy-700 hover:scale-105 transition-all"
            title="Chat with MediBot AI Assistant"
          >
            <div className="w-2.5 h-2.5 rounded-full bg-teal-400 animate-pulse"></div>
            <span>Ask MediBot AI</span>
          </button>
        </div>

        {/* MediBot Drawer Pop-up (Right side) */}
        <MediBotDrawer
          isOpen={isBotOpen}
          onClose={() => setIsBotOpen(false)}
          activeContext={activeContext}
        />

        {/* Site Footer */}
        <Footer />

      </div>
    </BrowserRouter>
  );
}
