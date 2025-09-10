import apiClient from './api';

export const getAuditLogs = () => {
  return apiClient.get('/api/audit/logs/');
};
