import apiClient from './api';
import type { Clinic } from '@/stores/clinic'; // Assuming you have this type

export interface GuideType {
  id: string;
  name: string;
  is_active: boolean;
  clinics: string[];
}

export interface ProcedureStatus {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  clinics: string[];
}

export interface ExitType {
  id: string;
  name: string;
  code: string;
  clinics: string[];
}

export interface Role {
  id: string;
  name: string;
}

export interface User {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_superuser: boolean;
  clinics: string[];
  roles: string[];
  password?: string;
}

export interface Payer {
  id: string;
  name: string;
  payer_type: 'SUS' | 'PRIVATE';
  is_active: boolean;
  clinics: string[];
}

// Role API
export const getRoles = () => apiClient.get<Role[]>('/api/administration/roles/');


// Clinic API
export const getClinics = () => apiClient.get<Clinic[]>('/api/administration/clinics/');
export const createClinic = (data: Omit<Clinic, 'id'>) => apiClient.post<Clinic>('/api/administration/clinics/', data);
export const updateClinic = (id: string, data: Partial<Clinic>) => apiClient.put<Clinic>(`/api/administration/clinics/${id}/`, data);
export const deleteClinic = (id: string) => apiClient.delete(`/api/administration/clinics/${id}/`);

// Payer API
export const getPayers = () => apiClient.get<Payer[]>('/api/billing/payers/');
export const createPayer = (data: Partial<Payer>) => apiClient.post<Payer>('/api/billing/payers/', data);
export const updatePayer = (id: string, data: Partial<Payer>) => apiClient.put<Payer>(`/api/billing/payers/${id}/`, data);
export const deletePayer = (id: string) => apiClient.delete(`/api/billing/payers/${id}/`);

// GuideType API
export const getGuideTypes = () => apiClient.get<GuideType[]>('/api/administration/guide-types/');
export const createGuideType = (data: Omit<GuideType, 'id'>) => apiClient.post<GuideType>('/api/administration/guide-types/', data);
export const updateGuideType = (id: string, data: Partial<GuideType>) => apiClient.put<GuideType>(`/api/administration/guide-types/${id}/`, data);
export const deleteGuideType = (id: string) => apiClient.delete(`/api/administration/guide-types/${id}/`);

// ProcedureStatus API
export const getProcedureStatuses = () => apiClient.get<ProcedureStatus[]>('/api/administration/procedure-statuses/');
export const createProcedureStatus = (data: Omit<ProcedureStatus, 'id'>) => apiClient.post<ProcedureStatus>('/api/administration/procedure-statuses/', data);
export const updateProcedureStatus = (id: string, data: Partial<ProcedureStatus>) => apiClient.put<ProcedureStatus>(`/api/administration/procedure-statuses/${id}/`, data);
export const deleteProcedureStatus = (id: string) => apiClient.delete(`/api/administration/procedure-statuses/${id}/`);

// ExitType API
export const getExitTypes = () => apiClient.get<ExitType[]>('/api/administration/exit-types/');
export const createExitType = (data: Omit<ExitType, 'id'>) => apiClient.post<ExitType>('/api/administration/exit-types/', data);
export const updateExitType = (id: string, data: Partial<ExitType>) => apiClient.put<ExitType>(`/api/administration/exit-types/${id}/`, data);
export const deleteExitType = (id: string) => apiClient.delete(`/api/administration/exit-types/${id}/`);

// User API
export const getUsers = () => apiClient.get<User[]>('/api/administration/users/');
export const createUser = (data: Partial<User>) => apiClient.post<User>('/api/administration/users/', data);
export const updateUser = (id: string, data: Partial<User>) => apiClient.put<User>(`/api/administration/users/${id}/`, data);
export const deleteUser = (id: string) => apiClient.delete(`/api/administration/users/${id}/`);

// Mandatory Documents API
export const getMandatoryDocuments = (clinicId: string) => apiClient.get<string[]>(`/api/administration/clinics/${clinicId}/mandatory-documents/`);
export const setMandatoryDocuments = (clinicId: string, documentTypeIds: string[]) => apiClient.post(`/api/administration/clinics/${clinicId}/mandatory-documents/`, { document_type_ids: documentTypeIds });
