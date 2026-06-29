import axios from "axios";

const BASE_URL = "http://localhost:8000/api";

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await axios.post(`${BASE_URL}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

export const analyzeIssues = async (filename) => {
  const response = await axios.get(`${BASE_URL}/analyze/${filename}`);
  return response.data;
};

export const cleanDataset = async (filename, instructions) => {
  const response = await axios.post(`${BASE_URL}/clean/${filename}`, instructions);
  return response.data;
};

export const getDownloadUrl = (filename) => `${BASE_URL}/download/${filename}`;

export const getEDA = async (filename) => {
  const response = await axios.get(`${BASE_URL}/eda/${filename}`);
  return response.data;
};

export const getInsights = async (filename) => {
  const response = await axios.get(`${BASE_URL}/insights/${filename}`);
  return response.data;
};

export const generateReport = async (filename) => {
  const response = await axios.post(`${BASE_URL}/report/${filename}`, {}, {
    responseType: "blob",
  });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `DataPilot_Report_${filename.replace(".csv", "")}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};