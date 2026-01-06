import React from 'react';
import Link from 'next/link';

const ForbiddenPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-xl text-center">
        <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-red-100">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h1 className="mt-4 text-3xl font-bold text-gray-900">403 - Forbidden</h1>
        <p className="mt-2 text-gray-600">
          You don't have permission to access this resource.
        </p>
        <div className="mt-6">
          <Link href="/dashboard" className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Go to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ForbiddenPage;