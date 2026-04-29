import axios from "axios";

const API_BASE = "http://localhost:8000";

export const fetchDashboard = async (qProducts = "", qUsers = "") => {
  const params = {};
  if (qProducts) params.qProducts = qProducts;
  if (qUsers) params.qUsers = qUsers;

  const res = await axios.get(`${API_BASE}/api/dashboard`, { params });
  return res.data;
};
