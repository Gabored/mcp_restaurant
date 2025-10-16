// fetch.ts
import axios from 'axios';

export const fetchJSON = async (url: string, params?: Record<string, any>) => {
  const { data } = await axios.get(url, { params, timeout: 10000 });
  return data;
};
