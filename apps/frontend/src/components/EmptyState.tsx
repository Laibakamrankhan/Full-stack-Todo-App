import React from 'react';
import { motion } from 'framer-motion';

const EmptyState: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center py-12"
    >
      <div className="mx-auto h-24 w-24 flex items-center justify-center rounded-full bg-gradient-to-r from-blue-100 to-indigo-100">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      </div>
      <h3 className="mt-6 text-xl font-bold text-gray-900">No tasks yet</h3>
      <p className="mt-2 text-gray-600">
        Get started by creating your first task.
      </p>
      <p className="mt-1 text-sm text-gray-500">
        Add a task using the form above to get started.
      </p>
    </motion.div>
  );
};

export default EmptyState;