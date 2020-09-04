import * as qs from 'qs';

export const API_BASE = process.env.VUE_APP_API_SERVER;

export const apiConfig = {
  returnRejectedPromiseOnError: true,
  withCredentials: true,
  credentials: 'same-origin',
  timeout: 30000,
  baseURL: API_BASE,
  headers: {
    common: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      Pragma: 'no-cache',
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  },
  paramsSerializer: (params: any) => qs.stringify(params, { indices: false }),
};
