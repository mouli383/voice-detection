
export type SupportedLanguage = 'Tamil' | 'English' | 'Hindi' | 'Malayalam' | 'Telugu';

export type Classification = 'AI_GENERATED' | 'HUMAN';

export interface DetectionResponse {
  status: 'success' | 'error';
  language?: SupportedLanguage;
  classification?: Classification;
  confidenceScore?: number;
  explanation?: string;
  message?: string;
}

export interface AnalysisHistoryItem extends DetectionResponse {
  id: string;
  timestamp: Date;
  fileName: string;
}
