
import React, { useState, useRef } from 'react';
import { voiceService } from './geminiService';
import { DetectionResponse, AnalysisHistoryItem } from './types';
import { ICONS } from './constants';
import Header from './components/Header';
import ResultCard from './components/ResultCard';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<string>("English");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'audio/mpeg' && !selectedFile.name.endsWith('.mp3')) {
        alert("System restricted to MP3 format only.");
        return;
      }
      setFile(selectedFile);
      setResult(null);
    }
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64String = (reader.result as string).split(',')[1];
        resolve(base64String);
      };
      reader.onerror = (error) => reject(error);
    });
  };

  const runVerification = async () => {
    if (!file) return;
    setAnalyzing(true);
    setResult(null);

    try {
      const base64 = await fileToBase64(file);
      // Pass the selected language
      const detectionResult = await voiceService.analyzeVoice(base64, language);

      setResult(detectionResult);

      if (detectionResult.status === 'success') {
        const historyItem: AnalysisHistoryItem = {
          ...detectionResult,
          id: Math.random().toString(36).substring(7),
          timestamp: new Date(),
          fileName: file.name
        };
        setHistory(prev => [historyItem, ...prev].slice(0, 5));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  const reset = () => {
    setFile(null);
    setResult(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="min-h-screen text-gray-100 pb-20">
      <Header />

      <main className="max-w-4xl mx-auto px-6 mt-12 space-y-12">
        {/* Header Section */}
        <section className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold uppercase tracking-widest">
            Vocal Forensic Platform v5.0 (Pro)
          </div>
          <h1 className="text-5xl font-black text-white leading-tight">
            Advanced Vocal Audit <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">Spectral Integrity Verification.</span>
          </h1>
          <p className="text-gray-400 max-w-xl mx-auto text-lg leading-relaxed">
            High-fidelity authentication engine detecting organic versus synthetic origins with Proof-of-Life verification for regional languages.
          </p>
        </section>

        {/* Console Interface */}
        <div className="glass p-8 rounded-[2rem] border border-white/10 space-y-8 shadow-2xl shadow-blue-900/10">
          {/* Language Selector */}
          <div className="flex justify-center mb-6">
            <div className="relative group">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-blue-400/80 text-[10px] font-bold uppercase tracking-widest pointer-events-none transition-colors group-hover:text-blue-300">
                Target Language:
              </span>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                disabled={analyzing}
                className="appearance-none bg-black/40 border border-white/10 rounded-xl py-4 pl-40 pr-12 text-white font-bold focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all cursor-pointer hover:bg-white/5 hover:border-white/20 w-full sm:w-auto min-w-[320px]"
              >
                {['Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu'].map(lang => (
                  <option key={lang} value={lang} className="bg-gray-900 text-white py-2">{lang}</option>
                ))}
              </select>
              <div className="absolute right-5 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg className="w-5 h-5 text-gray-500 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" /></svg>
              </div>
            </div>
          </div>

          {/* Upload Area */}
          <div
            onClick={() => !analyzing && fileInputRef.current?.click()}
            className={`
              relative group cursor-pointer rounded-2xl border-2 border-dashed transition-all duration-300
              ${file ? 'border-blue-500/50 bg-blue-500/5' : 'border-white/10 hover:border-white/20 hover:bg-white/5'}
              ${analyzing ? 'opacity-50 cursor-wait' : ''}
              p-12 text-center
            `}
          >
            <input type="file" ref={fileInputRef} onChange={handleFileChange} accept=".mp3" className="hidden" />

            {file ? (
              <div className="space-y-4">
                <div className="mx-auto w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                  <ICONS.FileAudio className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">{file.name}</h3>
                  <p className="text-sm text-gray-400">{(file.size / 1024).toFixed(1)} KB • Forensic Buffer Ready</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="mx-auto w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center">
                  <ICONS.Upload className="w-8 h-8 text-gray-400" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">Import Sample for Audit</h3>
                  <p className="text-sm text-gray-400">Load MP3 recording for deep-tissue waveform analysis</p>
                </div>
              </div>
            )}
          </div>

          {file && !result && (
            <button
              onClick={runVerification}
              disabled={analyzing}
              className={`w-full py-4 rounded-xl font-bold text-white transition-all shadow-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 active:scale-[0.98] ${analyzing ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {analyzing ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                  <span>Performing Forensic Waveform Scrutiny...</span>
                </div>
              ) : 'Initiate Deep Signature Verification'}
            </button>
          )}
        </div>

        {/* Results */}
        {result && result.status === 'success' && (
          <div className="animate-in fade-in slide-in-from-top-4 duration-500">
            <ResultCard result={result} />
            <div className="mt-6 flex justify-center">
              <button onClick={reset} className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
                <ICONS.Trash className="w-4 h-4" />
                Flush Audit Logs
              </button>
            </div>
          </div>
        )}

        {/* Technical Specification View */}
        <section className="p-8 glass rounded-[2rem] border border-blue-500/20 bg-blue-500/5">
          <h3 className="text-lg font-bold text-white mb-4">Forensic Data Output</h3>
          <p className="text-sm text-gray-400 mb-6">Real-time JSON serialization of the verification engine results.</p>
          <div className="bg-black/40 rounded-xl p-6 border border-white/5 shadow-inner">
            <pre className="text-xs text-blue-300 mono leading-relaxed">
              {`{
  "status": "${result?.status || 'success'}",
  "language": "${result?.language || 'Tamil'}",
  "classification": "${result?.classification || 'AI_GENERATED'}",
  "confidenceScore": ${result?.confidenceScore || 0.98},
  "explanation": "${result?.explanation || 'Awaiting forensic data stream...'}"
}`}
            </pre>
          </div>
        </section>
      </main>

      <footer className="mt-20 border-t border-white/5 pt-10 text-center pb-10">
        <p className="text-gray-500 text-xs font-medium uppercase tracking-widest">
          VoxGuard High-Resolution Forensic System • HCL GUVI 2026
        </p>
      </footer>
    </div>
  );
};

export default App;
