import React from 'react';
import TaskItem from './TaskItem';
import { Task } from '../types';
import EmptyState from './EmptyState';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: string) => void;
  selectedCategory?: string;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdated, onTaskDeleted, selectedCategory = 'All' }) => {
  // Filter tasks based on selected category
  const filteredTasks = selectedCategory === 'All'
    ? tasks
    : tasks.filter(task => task.category === selectedCategory);

  const pendingTasks = filteredTasks.filter(task => !task.completed);
  const completedTasks = filteredTasks.filter(task => task.completed);

  return (
    <div className="mt-6">
      {filteredTasks.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="space-y-6">
          {pendingTasks.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                In Progress ({pendingTasks.length})
              </h3>
              <div className="space-y-4">
                {pendingTasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onTaskUpdated={onTaskUpdated}
                    onTaskDeleted={onTaskDeleted}
                  />
                ))}
              </div>
            </div>
          )}

          {completedTasks.length > 0 && (
            <div className="mt-8">
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Completed ({completedTasks.length})
              </h3>
              <div className="space-y-4">
                {completedTasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onTaskUpdated={onTaskUpdated}
                    onTaskDeleted={onTaskDeleted}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TaskList;