export interface File {
  file_id: number;
  file_name: string;
  file_type: 'html' | 'pdf' | 'docx' | 'css';
  file_path: string;
  created_at: string | null;
}

export interface FilesByType {
  html: File | null;
  docx: File | null;
  pdf: File | null;
  css: File | null;
}
