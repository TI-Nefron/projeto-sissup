import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8001/api',
  withCredentials: true, // to send cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
