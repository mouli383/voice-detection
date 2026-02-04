
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { DetectionResponse } from '../types';
import { ICONS } from '../constants';

interface Props {
  result: DetectionResponse;
}

const ResultCard: React.FC<Props> = ({ result }) => {
  const isSynthetic = result.classification === 'AI_GENERATED';
  const confidence = Math.round((result.confidenceScore || 0) * 100);
  
  const data = [
    { value: confidence },
    { value: 100 - confidence }
  ];

  return (
    <div className={`rounded-3xl border overflow-hidden transition-all duration-500 ${
      isSynthetic ? 'border-red-500/30 bg-red-950/10' : 'border-green-500/30 bg-green-950/10'
    }`}>
      <div className="p-8">
        <div className="flex flex-col md:flex-row items-center gap-8">
          <div className="relative w-48 h-48 flex-shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={80} startAngle={90} endAngle={450} paddingAngle={0} dataKey="value">
                  <Cell fill={isSynthetic ? '#ef4444' : '#22c55e'} stroke="none" />
                  <Cell fill="rgba(255,255,255,0.1)" stroke="none" />
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-4xl font-bold ${isSynthetic ? 'text-red-500' : 'text-green-500'}`}>{confidence}%</span>
              <span className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Confidence</span>
            </div>
          </div>

          <div className="flex-1 space-y-4 text-center md:text-left">
            <div>
              <div className="inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-white/10 text-gray-300 mb-2">
                Detected: {result.language}
              </div>
              <h2 className={`text-4xl font-black tracking-tight ${isSynthetic ? 'text-red-500' : 'text-green-500'}`}>
                {result.classification}
              </h2>
            </div>
            <div className="space-y-2">
              <div className="flex items-start gap-3 justify-center md:justify-start">
                <ICONS.Check className="w-5 h-5 text-gray-500 mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-sm font-semibold text-gray-300">Analysis Summary</h4>
                  <p className="text-sm text-gray-400 italic leading-relaxed">"{result.explanation}"</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
