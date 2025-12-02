import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function FeatureImportanceChart({ features }) {
  if (!features || features.length === 0) return null;
  const labels = features.map(f => f.feature);
  const data = {
    labels,
    datasets: [{ label: "Importance", data: features.map(f => f.importance), backgroundColor: "rgba(59,130,246,0.8)" }]
  };
  const options = { responsive: true, plugins: { legend: { display: false } } };
  return <div style={{height:320}}><Bar data={data} options={options} /></div>;
}
