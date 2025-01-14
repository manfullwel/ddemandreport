import React, { useState, useCallback, useMemo } from 'react';
import { DashboardFilters } from './DashboardFilters';
import { DailyChart } from './DailyChart';
import { DataTable } from './DataTable';
import { SummaryCards } from './SummaryCards';
import { ReportFilters, INITIAL_FILTERS } from '@/types/report';
import { ErrorBoundary } from './ErrorBoundary';
import { errorHandler } from '@/utils/errorHandler';

export const Dashboard: React.FC = () => {
  const [filters, setFilters] = useState<ReportFilters>(INITIAL_FILTERS);

  const handleFilterChange = useCallback((newFilters: ReportFilters) => {
    try {
      setFilters(newFilters);
    } catch (error) {
      errorHandler.logError(error as Error, {
        component: 'Dashboard',
        action: 'handleFilterChange',
      });
    }
  }, []);

  // Memoize components to prevent unnecessary re-renders
  const memoizedFilters = useMemo(
    () => <DashboardFilters filters={filters} onFilterChange={handleFilterChange} />,
    [filters, handleFilterChange]
  );

  const memoizedChart = useMemo(() => <DailyChart filters={filters} />, [filters]);

  const memoizedTable = useMemo(() => <DataTable filters={filters} />, [filters]);

  const memoizedSummary = useMemo(() => <SummaryCards filters={filters} />, [filters]);

  return (
    <ErrorBoundary>
      <div className="container mx-auto p-4 space-y-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h1 className="text-2xl font-bold mb-6">Dashboard de Demandas</h1>
          {memoizedFilters}
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {memoizedSummary}
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Análise Diária</h2>
          {memoizedChart}
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Demandas</h2>
          {memoizedTable}
        </div>
      </div>
    </ErrorBoundary>
  );
};
