import React from 'react';
import { Task } from '../types';
import { motion } from 'framer-motion';

interface CategoryOverviewProps {
  tasks: Task[];
  selectedCategory: string;
  onCategorySelect: (category: string) => void;
}

const CategoryOverview: React.FC<CategoryOverviewProps> = ({
  tasks,
  selectedCategory,
  onCategorySelect
}) => {
  // Count tasks by category
  const categoryCounts = tasks.reduce((acc, task) => {
    acc[task.category] = (acc[task.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Get unique categories
  const categories = Array.from(new Set(tasks.map(task => task.category)));

  // Include "All" category
  const allCategories = ['All', ...categories];

  return (
    <div className="mt-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Categories</h3>
      <div className="flex space-x-3 overflow-x-auto pb-2 -mx-2 px-2">
        {allCategories.map((category) => {
          const count = category === 'All'
            ? tasks.length
            : categoryCounts[category] || 0;

          const isActive = selectedCategory === category;

          let bgColor = 'bg-gray-100';
          let textColor = 'text-gray-800';
          let activeBgColor = 'bg-gray-200';

          switch (category) {
            case 'General':
              bgColor = 'bg-blue-50';
              textColor = 'text-blue-800';
              activeBgColor = 'bg-blue-100';
              break;
            case 'Work':
              bgColor = 'bg-purple-50';
              textColor = 'text-purple-800';
              activeBgColor = 'bg-purple-100';
              break;
            case 'Personal':
              bgColor = 'bg-pink-50';
              textColor = 'text-pink-800';
              activeBgColor = 'bg-pink-100';
              break;
            case 'Study':
              bgColor = 'bg-green-50';
              textColor = 'text-green-800';
              activeBgColor = 'bg-green-100';
              break;
            case 'Health':
              bgColor = 'bg-red-50';
              textColor = 'text-red-800';
              activeBgColor = 'bg-red-100';
              break;
            case 'Shopping':
              bgColor = 'bg-yellow-50';
              textColor = 'text-yellow-800';
              activeBgColor = 'bg-yellow-100';
              break;
            case 'All':
              bgColor = 'bg-indigo-50';
              textColor = 'text-indigo-800';
              activeBgColor = 'bg-indigo-100';
              break;
          }

          return (
            <motion.button
              key={category}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onCategorySelect(category)}
              className={`flex-shrink-0 px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-colors ${
                isActive
                  ? `${activeBgColor} ${textColor} border border-current shadow-sm`
                  : `${bgColor} ${textColor} hover:${activeBgColor}`
              }`}
            >
              <span className="flex items-center">
                {category}
                <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-medium ${
                  isActive ? 'bg-white bg-opacity-30' : 'bg-white bg-opacity-50'
                }`}>
                  {count}
                </span>
              </span>
            </motion.button>
          );
        })}
      </div>
    </div>
  );
};

export default CategoryOverview;