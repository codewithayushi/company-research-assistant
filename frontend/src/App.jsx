import React, { useState } from 'react';
import { Send, Download, Settings, Loader2, Building2, Globe, ShieldAlert, Users } from 'lucide-react';

export default function App() {
  const [query, setQuery] = useState('');
  const [model, setModel] = useState('openai/gpt-3.5-turbo');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  
  // Discord & Applicant Config
  const [showSettings, setShowSettings] = useState(false);
  const [applicantName, setApplicantName] = useState('');
  const [applicantEmail, setApplicantEmail] = useState('');
  const [discordToken, setDiscordToken] = useState('');
  const [discordChannelId, setDiscordChannelId] = useState('');

  const handleResearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setReport(null);
    setPdfFile(null);

    try {
      const res = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          model,
          applicant_name: applicantName,
          applicant_email: applicantEmail,
          discord_token: discordToken,
          discord_channel_id: discordChannelId
        })
      });
      const data = await res.json();
      if (res.ok) {
        setReport(data.data);
        setPdfFile(data.pdf_file);
      } else {
        alert(data.detail || 'Error generating report');
      }
    } catch (err) {
      alert('Failed to connect to backend server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* Sidebar / Settings Modal Drawer */}
      <div className={`fixed inset-y-0 left-0 z-50 w-80 bg-slate-900 border-r border-slate-800 p-6 transform transition-transform ${showSettings ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-semibold flex items-center gap-2"><Settings size={20}/> Settings & Config</h2>
          <button onClick={() => setShowSettings(false)} className="text-slate-400 hover:text-white">✕</button>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">AI Model (OpenRouter)</label>
            <select value={model} onChange={(e) => setModel(e.target.value)} className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm">
              <option value="meta-llama/llama-3-8b-instruct:free">Llama 3 8B (Free)</option>
              <option value="google/gemma-7b-it:free">Gemma 7B (Free)</option>
              <option value="openai/gpt-3.5-turbo">GPT-3.5 Turbo</option>
            </select>           
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Applicant Name</label>
            <input type="text" value={applicantName} onChange={(e) => setApplicantName(e.target.value)} placeholder="John Doe" className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Applicant Email</label>
            <input type="email" value={applicantEmail} onChange={(e) => setApplicantEmail(e.target.value)} placeholder="john@example.com" className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Discord Bot Token</label>
            <input type="password" value={discordToken} onChange={(e) => setDiscordToken(e.target.value)} placeholder="Bot Token" className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Discord Channel ID</label>
            <input type="text" value={discordChannelId} onChange={(e) => setDiscordChannelId(e.target.value)} placeholder="Channel ID" className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-sm" />
          </div>
        </div>
      </div>

      {/* Main Chat / Dashboard Area */}
      <div className="flex-1 flex flex-col h-full">
        <header className="flex justify-between items-center px-6 py-4 border-b border-slate-800 bg-slate-900/50">
          <h1 className="font-bold text-lg flex items-center gap-2"><Building2 className="text-blue-500"/> AI Company Research Assistant</h1>
          <button onClick={() => setShowSettings(true)} className="flex items-center gap-1 text-sm bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded transition">
            <Settings size={16}/> Settings
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {!report && !loading && (
            <div className="h-full flex flex-col items-center justify-center text-center text-slate-500 space-y-3">
              <Building2 size={48} className="text-slate-700"/>
              <p className="text-lg">Enter a company name or website URL below to start researching.</p>
            </div>
          )}

          {loading && (
            <div className="flex flex-col items-center justify-center py-20 space-y-4">
              <Loader2 className="animate-spin text-blue-500" size={36}/>
              <p className="text-slate-400 text-sm">Crawling website, analyzing data, and compiling report...</p>
            </div>
          )}

          {report && (
  <div className="max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
    <div className="flex justify-between items-start">
      <div>
        <h2 className="text-2xl font-bold">{report?.company_name || 'Unknown'}</h2>
        <a href={report?.website} target="_blank" rel="noreferrer" className="text-blue-400 text-sm flex items-center gap-1 mt-1 hover:underline">
          <Globe size={14}/> {report?.website || 'N/A'}
        </a>
      </div>
      {pdfFile && (
        <a href={`http://127.0.0.1:8000/api/download/${pdfFile}`} target="_blank" rel="noreferrer" className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
          <Download size={16}/> Download PDF Report
        </a>
      )}
    </div>

    <div className="grid grid-cols-2 gap-4 text-sm bg-slate-950 p-4 rounded-lg border border-slate-800">
      <div><span className="text-slate-500">Phone:</span> {report?.phone || 'N/A'}</div>
      <div><span className="text-slate-500">Address:</span> {report?.address || 'N/A'}</div>
    </div>

    <div>
      <h3 className="text-md font-semibold text-slate-300 mb-2">Executive Summary</h3>
      <p className="text-slate-400 text-sm leading-relaxed">{report?.summary || 'No summary available.'}</p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h3 className="text-md font-semibold text-slate-300 mb-2">Products & Services</h3>
        <ul className="list-disc list-inside text-sm text-slate-400 space-y-1">
          {report?.products_services?.length > 0 ? (
            report.products_services.map((item, idx) => <li key={idx}>{item}</li>)
          ) : (
            <li>N/A</li>
          )}
        </ul>
      </div>
      <div>
        <h3 className="text-md font-semibold text-slate-300 mb-2 flex items-center gap-1"><ShieldAlert size={16} className="text-amber-500"/> AI Pain Points</h3>
        <ul className="list-disc list-inside text-sm text-slate-400 space-y-1">
          {report?.pain_points?.length > 0 ? (
            report.pain_points.map((item, idx) => <li key={idx}>{item}</li>)
          ) : (
            <li>N/A</li>
          )}
        </ul>
      </div>
    </div>

    <div>
      <h3 className="text-md font-semibold text-slate-300 mb-2 flex items-center gap-1"><Users size={16}/> Competitor Analysis</h3>
      <div className="border border-slate-800 rounded-lg overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-950 text-slate-400">
            <tr>
              <th className="p-3">Competitor Name</th>
              <th className="p-3">Website</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {report?.competitors?.length > 0 ? (
              report.competitors.map((comp, idx) => (
                <tr key={idx}>
                  <td className="p-3 font-medium">{comp?.name || 'N/A'}</td>
                  <td className="p-3 text-blue-400"><a href={comp?.website} target="_blank" rel="noreferrer" className="hover:underline">{comp?.website || '#'}</a></td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2" className="p-3 text-center text-slate-500">No competitors found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  </div>
)}
        </div>

        <div className="p-4 border-t border-slate-800 bg-slate-900/50">
          <form onSubmit={handleResearch} className="max-w-4xl mx-auto flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter company name (e.g. Stripe) or website URL (e.g. https://stripe.com)..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-blue-600"
            />
            <button type="submit" disabled={loading} className="bg-blue-600 hover:bg-blue-500 text-white px-5 rounded-lg flex items-center justify-center transition disabled:opacity-50">
              <Send size={18}/>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}