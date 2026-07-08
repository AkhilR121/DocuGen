import { File } from './file';

export interface Document {
  document_id: number;
  contract_id: number;
  customer_name: string;
  sites_count: number;
  is_active: boolean;
  created_at: string | null;
  files: File[];
}

export interface DocumentData {
  customer_name: string;
  sites_count: number;
}
