import apiClient from './api';

export interface DocumentType {
  id: string;
  name: string;
  category: 'PATIENT' | 'GUIDE';
  is_active: boolean;
}

export const getDocumentTypes = () => apiClient.get<DocumentType[]>('/api/document-types/');
export const createDocumentType = (data: Omit<DocumentType, 'id'>) => apiClient.post<DocumentType>('/api/document-types/', data);
export const updateDocumentType = (id: string, data: Partial<DocumentType>) => apiClient.put<DocumentType>(`/api/document-types/${id}/`, data);
export const deleteDocumentType = (id: string) => apiClient.delete(`/api/document-types/${id}/`);
