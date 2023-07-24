import axios from 'axios';

const useBirdcageAPI = axios.create({
  baseURL: import.meta.env.VITE_BIRDCAGE_API_URL,
});

// export the instance
export default useBirdcageAPI;
