import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8001',
  withCredentials: true, // to send cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to get the CSRF token from cookies
function getCookie(name: string): string | null {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Add a request interceptor to include the CSRF token
apiClient.interceptors.request.use((config) => {
  // Always send CSRF token for any state-changing method, and for GET to ensure session integrity
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default apiClient;
