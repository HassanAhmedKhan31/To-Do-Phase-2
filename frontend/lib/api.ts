// T-310: Create frontend/lib/api.ts with logic to switch the baseURL to '/api' in production.

const getBaseURL = () => {
  if (process.env.NODE_ENV === 'production') {
    return '/api';
  }
  return 'http://localhost:8000';
};

export const baseURL = getBaseURL();
