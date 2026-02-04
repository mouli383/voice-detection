
import React from 'react';
import { ICONS } from '../constants';

const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 glass border-b border-white/10 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-xl shadow-lg shadow-blue-500/20">
            <ICONS.Shield className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">VoxGuard <span className="text-blue-500">Forensics</span></h1>
            <p className="text-xs text-gray-400 font-medium uppercase tracking-widest">HCL GUVI Hackathon 2026</p>
          </div>
        </div>
        
        <div className="hidden md:flex items-center gap-6">
          <nav className="flex items-center gap-6">
            <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">Documentation</a>
            <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">Network Status</a>
          </nav>
          <div className="h-6 w-px bg-white/10"></div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
            <span className="text-xs font-mono text-gray-400">ENGINE ONLINE</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
