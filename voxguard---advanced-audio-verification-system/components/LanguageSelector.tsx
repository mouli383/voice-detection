
import React from 'react';
import { LANGUAGES } from '../constants';
import { SupportedLanguage } from '../types';

interface Props {
  selected: SupportedLanguage;
  onSelect: (lang: SupportedLanguage) => void;
  disabled?: boolean;
}

const LanguageSelector: React.FC<Props> = ({ selected, onSelect, disabled }) => {
  return (
    <div className="w-full">
      <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
        Detection Language
      </label>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
        {LANGUAGES.map((lang) => (
          <button
            key={lang}
            onClick={() => onSelect(lang as SupportedLanguage)}
            disabled={disabled}
            className={`
              px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 border
              ${selected === lang 
                ? 'bg-blue-600/20 border-blue-500 text-blue-100 shadow-[0_0_15px_rgba(59,130,246,0.3)]' 
                : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:border-white/20'
              }
              ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            {lang}
          </button>
        ))}
      </div>
    </div>
  );
};

export default LanguageSelector;
