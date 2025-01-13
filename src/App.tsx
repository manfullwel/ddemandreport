import { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import { SheetImport } from './components/SheetImport';
import { DailyReport as DailyReportType, Demanda } from './types/report';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { mockDemandas, mockReportData } from './data/mockData';

const queryClient = new QueryClient();

function App() {
    const location = useLocation();
    const [data, setData] = useState<DailyReportType[]>(mockReportData);
    const [demandas, setDemandas] = useState<Demanda[]>(mockDemandas);
    const [rawData, setRawData] = useState<any[][]>([]);
    const [fileName, setFileName] = useState<string>();

    const handleDataImported = (importedData: DailyReportType[], importedDemandas: Demanda[], name?: string) => {
        setData(importedData);
        setDemandas(importedDemandas);
        setFileName(name);
    };

    const handleRawDataImported = (data: any[][], name?: string) => {
        setRawData(data);
        setFileName(name);
    };

    return (
        <QueryClientProvider client={queryClient}>
            <TooltipProvider>
                <Toaster />
                <Sonner />
                <div className="min-h-screen bg-background">
                    <Navigation currentPath={location.pathname} />
                    <div className="max-w-screen-xl mx-auto p-4">
                        <SheetImport 
                            onDataImported={handleDataImported}
                            onRawDataImported={handleRawDataImported}
                        />
                        <div className="mt-4">
                            <Outlet context={{ data, demandas, rawData, fileName }} />
                        </div>
                    </div>
                </div>
            </TooltipProvider>
        </QueryClientProvider>
    );
}

export default App;
