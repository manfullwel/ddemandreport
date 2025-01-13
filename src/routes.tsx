import { createBrowserRouter } from 'react-router-dom';
import { DailyReport } from './components/DailyReport';
import { AnalyticsDashboard } from './components/AnalyticsDashboard';
import { DocumentViewer } from './components/DocumentViewer';
import App from './App';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {
                index: true,
                element: <DailyReport />
            },
            {
                path: 'analytics',
                element: <AnalyticsDashboard />
            },
            {
                path: 'data',
                element: <DocumentViewer />
            }
        ]
    }
]);
