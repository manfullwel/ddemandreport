import React, { useState } from 'react';
import { DailyReport as DailyReportType } from '../types/report';
import { SpreadsheetGenerator } from './SpreadsheetGenerator';
import { DashboardFilters } from './DashboardFilters';
import { ReportFilters, INITIAL_FILTERS } from '../types/report';
import { DataTable } from './DataTable';
import { SummaryCards } from './SummaryCards';
import { Contract, Employee } from '../types/spreadsheet';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { generateSpreadsheetData } from '../utils/mockDataGenerator';

export const Dashboard = () => {
    const [filters, setFilters] = useState<ReportFilters>(INITIAL_FILTERS);
    const [allData, setAllData] = useState<DailyReportType[]>([]);
    const [fileName, setFileName] = useState<string>();
    const [uploadDate, setUploadDate] = useState<Date>();
    const [activeTab, setActiveTab] = useState('summary');
    
    // Dados de exemplo para visualização
    const { contracts, employees } = generateSpreadsheetData();

    const handleFilterChange = (newFilters: ReportFilters) => {
        setFilters(newFilters);
    };

    return (
        <div className="p-4 space-y-8">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold">Dashboard</h1>
                <SpreadsheetGenerator />
            </div>
            
            <div className="mb-6">
                <DashboardFilters onFilterChange={handleFilterChange} />
            </div>

            <SummaryCards contracts={contracts} employees={employees} />
            
            <Tabs value={activeTab} onValueChange={setActiveTab} className="mt-6">
                <TabsList>
                    <TabsTrigger value="summary">Resumo</TabsTrigger>
                    <TabsTrigger value="contracts">Contratos</TabsTrigger>
                    <TabsTrigger value="employees">Funcionários</TabsTrigger>
                </TabsList>
                
                <TabsContent value="summary" className="mt-4">
                    <div className="grid gap-4 md:grid-cols-2">
                        <div>
                            <h3 className="text-lg font-semibold mb-2">Últimos Contratos</h3>
                            <DataTable 
                                data={contracts.slice(0, 5)} 
                                type="contracts" 
                            />
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold mb-2">Funcionários Ativos</h3>
                            <DataTable 
                                data={employees.slice(0, 5)} 
                                type="employees" 
                            />
                        </div>
                    </div>
                </TabsContent>
                
                <TabsContent value="contracts" className="mt-4">
                    <DataTable data={contracts} type="contracts" />
                </TabsContent>
                
                <TabsContent value="employees" className="mt-4">
                    <DataTable data={employees} type="employees" />
                </TabsContent>
            </Tabs>
        </div>
    );
};
