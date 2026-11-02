import React, { useState, useEffect, useRef } from 'react';
import {
  X,
  Send,
  Bot,
  User,
  Sparkles,
  RotateCcw,
  ShieldCheck,
  ExternalLink
} from 'lucide-react';
import { sendChatMessage } from '../services/api';

export default function MediBotDrawer({ isOpen, onClose, activeContext }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hello! I am **MediBot**, your AI Health Assistant. Ask me anything about your predictions, medical terms, or how our Genetic Algorithm, ANN, Fuzzy Logic, and CNN models work!"
    }
  ]);
  const [inputVal, setInputVal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const quickChips = [
    "Explain my current assessment",
    "How does the GA + ANN + Fuzzy hybrid work?",
    "What is the difference between Mild and Moderate Retinopathy?",
    "Why does elevated BMI increase diabetes risk?",
    "What is a Grad-CAM attention heatmap?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (textToSend) => {
    const text = textToSend || inputVal;
    if (!text.trim() || isLoading) return;

    const userMsg = { id: Date.now(), sender: 'user', text };
    setMessages((prev) => [...prev, userMsg]);
    setInputVal('');
    setIsLoading(true);

    try {
      const res = await sendChatMessage(text, 'medihybrid-session', activeContext);
      const botMsg = { id: Date.now() + 1, sender: 'bot', text: res.data.reply };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: "I experienced a temporary communication hiccup. Please ask again or select one of the soft computing topics below."
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden pointer-events-none">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-navy-900/40 backdrop-blur-sm pointer-events-auto transition-opacity"
        onClick={onClose}
      />

      {/* Drawer Container (Right side pop-up) */}
      <div className="absolute inset-y-0 right-0 max-w-full flex pl-10 pointer-events-auto">
        <div className="w-screen max-w-md bg-white border-l border-slate-200 shadow-2xl flex flex-col">
          
          {/* Header */}
          <div className="p-4 bg-navy-900 text-white flex items-center justify-between border-b border-navy-800">
            <div className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-xl bg-teal-500/20 border border-teal-400/40 flex items-center justify-center text-teal-300">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-sm tracking-tight flex items-center gap-1.5">
                  MediBot AI
                  <span className="px-1.5 py-0.5 text-[10px] rounded bg-teal-500/20 text-teal-300 border border-teal-500/30">
                    Online
                  </span>
                </h3>
                <p className="text-[11px] text-slate-400">Context-Aware Clinical & Soft Computing Assistant</p>
              </div>
            </div>

            <div className="flex items-center space-x-1">
              <button
                onClick={() => setMessages([messages[0]])}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-navy-800"
                title="Reset Conversation"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
              <button
                onClick={onClose}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-navy-800"
                title="Close MediBot"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Context Banner if active */}
          {activeContext && (
            <div className="bg-teal-50/80 px-3.5 py-1.5 border-b border-teal-100 flex items-center justify-between text-xs text-teal-800">
              <span className="flex items-center gap-1.5 font-medium truncate">
                <Sparkles className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                Active Context: {activeContext.disease || 'Assessment'} Loaded
              </span>
              <span className="text-[10px] bg-teal-200/60 px-1.5 py-0.5 rounded text-teal-900">Live</span>
            </div>
          )}

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-slate-50">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex gap-2.5 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {m.sender === 'bot' && (
                  <div className="w-7 h-7 rounded-lg bg-teal-600 text-white flex items-center justify-center shrink-0 text-xs shadow-sm mt-0.5">
                    <Bot className="w-4 h-4" />
                  </div>
                )}
                
                <div
                  className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed shadow-sm ${
                    m.sender === 'user'
                      ? 'bg-navy-900 text-white rounded-tr-none'
                      : 'bg-white border border-slate-200 text-slate-800 rounded-tl-none prose prose-xs'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{m.text}</div>
                </div>

                {m.sender === 'user' && (
                  <div className="w-7 h-7 rounded-lg bg-navy-800 text-teal-400 flex items-center justify-center shrink-0 text-xs shadow-sm mt-0.5">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-2 items-center text-xs text-slate-500 pl-9">
                <span className="w-2 h-2 rounded-full bg-teal-500 animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.4s]"></span>
                <span className="text-[11px] text-slate-400 ml-1">Analyzing knowledge graph...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Suggestion Chips */}
          <div className="px-3 py-2 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto no-scrollbar">
            {quickChips.map((chip, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(chip)}
                className="text-[11px] bg-slate-100 hover:bg-teal-50 text-slate-700 hover:text-teal-700 border border-slate-200 rounded-full px-2.5 py-1 whitespace-nowrap transition-colors shrink-0"
              >
                {chip}
              </button>
            ))}
          </div>

          {/* Input Box */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="p-3 bg-white border-t border-slate-200 flex items-center gap-2"
          >
            <input
              type="text"
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              placeholder="Ask MediBot about models or results..."
              className="flex-1 px-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 transition-all"
            />
            <button
              type="submit"
              disabled={isLoading || !inputVal.trim()}
              className="p-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-navy-900 disabled:opacity-50 transition-colors shadow-sm"
              title="Send Message"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

          {/* Safety Notice Footer */}
          <div className="bg-slate-100 px-3 py-1.5 border-t border-slate-200 text-[10px] text-slate-500 flex items-center justify-between">
            <span className="flex items-center gap-1">
              <ShieldCheck className="w-3 h-3 text-teal-600" />
              Educational Assistant • No Prescriptions
            </span>
            <span className="text-slate-400">v1.0</span>
          </div>

        </div>
      </div>
    </div>
  );
}
