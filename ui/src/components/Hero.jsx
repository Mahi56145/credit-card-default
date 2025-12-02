import React from "react";
import { motion } from "framer-motion";

export default function Hero() {
  return (
    <header className="bg-gradient-to-r from-brand-100 to-white border-b">
      <div className="container mx-auto px-4 py-6 flex items-center justify-between">
        <div>
          <motion.h1
            initial={{ y: -8, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="text-2xl font-semibold text-slate-900"
          >
            Credit Risk Studio
          </motion.h1>
          <motion.p
            initial={{ y: 6, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.12 }}
            className="text-sm text-slate-600"
          >
            Predict default probability — interactive demo & model playground
          </motion.p>
        </div>

        <div className="hidden sm:flex gap-3 items-center">
          <span className="text-xs bg-slate-100 px-3 py-1 rounded-full text-slate-700">ML Model: RandomForest</span>
          <a href="/docs" className="text-xs text-brand-500 underline">API docs</a>
        </div>
      </div>
    </header>
  );
}
