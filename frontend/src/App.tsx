import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, AlertCircle, Loader2, Database, ShieldAlert, CheckCircle, BarChart3, List, FileSpreadsheet } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export interface DatasetResponse {
  dataset: { rows: number; columns: number };
  schema: any[];
  quality: { score: number; duplicates: number; missing_values: any; outliers: any };
  statistics: any;
  insights: string[];
}

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<DatasetResponse | null>(null);

  const handleUpload = async (file: File) => {
    if (!file.name.endsWith('.csv')) return setError('Please upload a valid CSV file.');
    setLoading(true); setError(null);
    const formData = new FormData(); formData.append('file', file);
    try {
      const { data } = await axios.post('http://localhost:8000/api/analyze', formData);
      setReport(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200 p-4 md:p-8 text-slate-800 font-sans">
      <header className="max-w-6xl mx-auto mb-10 flex items-center gap-3">
        <div className="bg-blue-600 p-2.5 rounded-xl shadow-lg shadow-blue-200">
          <Database className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight">DataLens</h1>
          <p className="text-sm text-slate-500 font-medium">Automated Dataset Intelligence</p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        {!report ? (
          <div className="max-w-2xl mx-auto mt-20">
            <label className="flex flex-col items-center justify-center w-full h-80 bg-white/60 backdrop-blur-lg border border-white/40 shadow-xl rounded-3xl cursor-pointer hover:bg-white/80 transition-all duration-300 group">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                {loading ? (
                  <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
                ) : (
                  <UploadCloud className="w-14 h-14 mb-4 text-blue-500 group-hover:scale-110 transition-transform" />
                )}
                <p className="text-xl font-bold text-slate-700">{loading ? 'Analyzing...' : 'Drop your CSV here'}</p>
              </div>
              <input type="file" className="hidden" accept=".csv" onChange={(e) => e.target.files && handleUpload(e.target.files[0])} disabled={loading} />
            </label>
            {error && (
              <div className="mt-6 flex items-center gap-3 p-4 bg-red-50/80 backdrop-blur-md text-red-700 rounded-2xl border border-red-200">
                <AlertCircle className="w-5 h-5" /><p className="font-semibold">{error}</p>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Top Row: Overview & Quality */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="col-span-1 md:col-span-2 bg-white/70 backdrop-blur-xl p-6 rounded-3xl border border-white/50 shadow-lg flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-bold flex items-center gap-2"><FileSpreadsheet className="w-5 h-5 text-blue-500" /> Dataset Overview</h2>
                  <p className="text-slate-500 mt-1">Successfully parsed</p>
                </div>
                <div className="flex gap-8 text-center">
                  <div><p className="text-3xl font-black text-slate-800">{report.dataset.rows}</p><p className="text-sm font-semibold text-slate-500 uppercase">Rows</p></div>
                  <div><p className="text-3xl font-black text-slate-800">{report.dataset.columns}</p><p className="text-sm font-semibold text-slate-500 uppercase">Columns</p></div>
                </div>
              </div>

              <div className="bg-white/70 backdrop-blur-xl p-6 rounded-3xl border border-white/50 shadow-lg flex flex-col justify-center items-center">
                <h2 className="text-lg font-bold text-slate-700 mb-2">Quality Score</h2>
                <div className="text-5xl font-black text-blue-600">{report.quality.score}<span className="text-2xl text-slate-400">/100</span></div>
              </div>
            </div>

            {/* Middle Row: Insights & Chart */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/70 backdrop-blur-xl p-6 rounded-3xl border border-white/50 shadow-lg">
                <h3 className="text-lg font-bold flex items-center gap-2 mb-4"><ShieldAlert className="w-5 h-5 text-amber-500" /> Automated Insights</h3>
                <ul className="space-y-3">
                  {report.insights.map((insight, i) => (
                    <li key={i} className="flex items-start gap-3 bg-white/50 p-3 rounded-xl">
                      <CheckCircle className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                      <span className="text-sm font-medium text-slate-700">{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-white/70 backdrop-blur-xl p-6 rounded-3xl border border-white/50 shadow-lg">
                <h3 className="text-lg font-bold flex items-center gap-2 mb-6"><BarChart3 className="w-5 h-5 text-indigo-500" /> Unique Values per Column</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={report.schema}>
                      <XAxis dataKey="name" tick={{fontSize: 12}} interval={0} angle={-45} textAnchor="end" height={60} />
                      <YAxis />
                      <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'}} />
                      <Bar dataKey="unique_count" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            <button onClick={() => setReport(null)} className="w-full py-4 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-bold shadow-xl shadow-slate-900/20 transition-all">
              Analyze Another Dataset
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
