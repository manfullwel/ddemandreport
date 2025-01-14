import { createBrowserRouter } from 'react-router-dom';
import { Dashboard } from './components/Dashboard';
import { TestPage } from './pages/TestPage';
import { RelatorioDiario } from './pages/RelatorioDiario';
import { RelatorioGeral } from './pages/RelatorioGeral';
import { MobileDemo } from './pages/MobileDemo';
import { Demo } from './pages/Demo';
import { ErrorBoundary } from './components/ErrorBoundary';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Demo />,
    errorElement: <ErrorBoundary />,
  },
  {
    path: '/test',
    element: <TestPage />,
    errorElement: <ErrorBoundary />,
  },
  {
    path: '/dashboard',
    element: <Dashboard />,
    errorElement: <ErrorBoundary />,
  },
  {
    path: '/relatorio-diario',
    element: <RelatorioDiario />,
    errorElement: <ErrorBoundary />,
  },
  {
    path: '/relatorio-geral',
    element: <RelatorioGeral />,
    errorElement: <ErrorBoundary />,
  },
  {
    path: '/mobile',
    element: <MobileDemo />,
    errorElement: <ErrorBoundary />,
  },
]);
