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

export interface User {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_superuser: boolean;
  clinics: string[];
  password?: string;
}


// Clinic API
export const getClinics = () => apiClient.get<Clinic[]>('/api/administration/clinics/');
export const createClinic = (data: Omit<Clinic, 'id'>) => apiClient.post<Clinic>('/api/administration/clinics/', data);
export const updateClinic = (id: string, data: Partial<Clinic>) => apiClient.put<Clinic>(`/api/administration/clinics/${id}/`, data);
export const deleteClinic = (id: string) => apiClient.delete(`/api/administration/clinics/${id}/`);

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
