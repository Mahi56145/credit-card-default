import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function ShapBarChart({ shap }) {
  if (!shap || shap.length === 0) return null;
  const take = shap.slice(0, 8).reverse();
  const labels = take.map(d => d.feature);
  const values = take.map(d => d.shap_value ?? d.approx_contribution ?? 0);
  const colors = values.map(v => (v >= 0 ? "rgba(239,68,68,0.85)" : "rgba(34,197,94,0.85)"));
  const data = { labels, datasets: [{ label: "Contribution", data: values, backgroundColor: colors }] };
  const options = { indexAxis: "y", responsive: true, plugins: { legend: { display: false } } };
  return <div style={{height:360}}><Bar data={data} options={options} /></div>;
}
