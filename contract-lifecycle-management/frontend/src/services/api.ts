import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { Contract, ContractData, Document, DocumentData } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const contractsAPI = {
  getAll: (): Promise<AxiosResponse<Contract[]>> => api.get<Contract[]>('/contracts/'),

  getById: (id: number | string): Promise<AxiosResponse<Contract>> =>
    api.get<Contract>(`/contracts/${id}`),

  create: (data: ContractData): Promise<AxiosResponse<Contract>> =>
    api.post<Contract>('/contracts/', data),

  getDocuments: (contractId: number | string): Promise<AxiosResponse<Document[]>> =>
    api.get<Document[]>(`/contracts/${contractId}/documents`),

  createDocument: (contractId: number | string, data: DocumentData): Promise<AxiosResponse<Document>> =>
    api.post<Document>(`/contracts/${contractId}/documents`, data),
};

export const filesAPI = {
  getFileUrl: (fileId: number): string => `${API_BASE_URL}/files/${fileId}`,

  getFile: (fileId: number): Promise<AxiosResponse<Blob>> =>
    api.get<Blob>(`/files/${fileId}`, { responseType: 'blob' }),
};

export default api;
