import { useState } from 'react';
import { DailyReport as DailyReportType, ReportFilters, INITIAL_FILTERS } from '@/types/report';
import { DashboardFilters } from './DashboardFilters';
import { SheetImport } from './SheetImport';
import { DocumentViewer } from './DocumentViewer';
import { AnalyticsDashboard } from './AnalyticsDashboard';
import { DailyReport } from './DailyReport';
import { SpreadsheetGenerator } from './SpreadsheetGenerator';
import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/components/ui/tabs";
import { FileSpreadsheet, BarChart, CalendarDays } from 'lucide-react';

export const Dashboard = () => {
    const [filters, setFilters] = useState<ReportFilters>(INITIAL_FILTERS);
    const [allData, setAllData] = useState<DailyReportType[]>([]);
    const [rawData, setRawData] = useState<any[][]>([]);
    const [fileName, setFileName] = useState<string>();
    const [uploadDate, setUploadDate] = useState<Date>();
    const [activeTab, setActiveTab] = useState('daily');

    const handleDataImported = (importedData: DailyReportType[], name?: string) => {
        console.log('Dados importados:', importedData);
        setAllData(importedData);
        setFileName(name);
        setUploadDate(new Date());
    };

    const handleRawDataImported = (data: any[][], name?: string) => {
        console.log('Dados brutos importados:', data);
        setRawData(data);
        setFileName(name);
        setUploadDate(new Date());

        // Tenta converter para o formato DailyReport
        try {
            const headers = data[0].map(h => h.toString().trim());
            const requiredColumns = [
                'Nome_Funcionario',
                'Contratos_Resolvidos',
                'Pendentes_Receptivo',
                'Pendentes_Ativo',
                'Quitados',
                'Aprovados',
                'Data_Relatorio'
            ];

            const hasRequiredColumns = requiredColumns.every(col => 
                headers.some(h => h.toLowerCase() === col.toLowerCase())
            );

            if (hasRequiredColumns) {
                const mappedData = data.slice(1).map(row => {
                    const report: DailyReportType = {
                        Nome_Funcionario: row[headers.findIndex(h => h.toLowerCase() === 'nome_funcionario'.toLowerCase())] || '',
                        Contratos_Resolvidos: parseInt(row[headers.findIndex(h => h.toLowerCase() === 'contratos_resolvidos'.toLowerCase())]) || 0,
                        Pendentes_Receptivo: parseInt(row[headers.findIndex(h => h.toLowerCase() === 'pendentes_receptivo'.toLowerCase())]) || 0,
                        Pendentes_Ativo: parseInt(row[headers.findIndex(h => h.toLowerCase() === 'pendentes_ativo'.toLowerCase())]) || 0,
                        Quitados: parseInt(row[headers.findIndex(h => h.toLowerCase() === 'quitados'.toLowerCase())]) || 0,
                        Aprovados: parseInt(row[headers.findIndex(h => h.toLowerCase() === 'aprovados'.toLowerCase())]) || 0,
                        Data_Relatorio: new Date(row[headers.findIndex(h => h.toLowerCase() === 'data_relatorio'.toLowerCase())])
                    };
                    return report;
                });

                setAllData(mappedData);
            }
        } catch (error) {
            console.error('Erro ao converter dados:', error);
        }
    };

    const filteredData = allData.filter(report => {
        const dateMatch = report.Data_Relatorio >= filters.startDate && 
                        report.Data_Relatorio <= filters.endDate;
        
        const nameMatch = !filters.employeeName || 
                        filters.employeeName === 'all' ||
                        report.Nome_Funcionario.toLowerCase()
                            .includes(filters.employeeName.toLowerCase());

        return dateMatch && nameMatch;
    });

    return (
        <div className="space-y-4">
            <SheetImport 
                onDataImported={handleDataImported} 
                onRawDataImported={handleRawDataImported}
            />

            <div className="mb-8">
                <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
                <SpreadsheetGenerator />
            </div>

            <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList>
                    <TabsTrigger value="daily">
                        <CalendarDays className="h-4 w-4 mr-2" />
                        Relatório Diário
                    </TabsTrigger>
                    <TabsTrigger value="analytics">
                        <BarChart className="h-4 w-4 mr-2" />
                        Dashboard Analítico
                    </TabsTrigger>
                    <TabsTrigger value="document">
                        <FileSpreadsheet className="h-4 w-4 mr-2" />
                        Dados Brutos
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="daily">
                    <DailyReport 
                        data={allData}
                        fileName={fileName}
                    />
                </TabsContent>

                <TabsContent value="analytics" className="space-y-4">
                    <DashboardFilters onFilterChange={setFilters} />
                    <AnalyticsDashboard data={filteredData} />
                </TabsContent>

                <TabsContent value="document">
                    <DocumentViewer 
                        data={rawData}
                        fileName={fileName}
                        uploadDate={uploadDate}
                    />
                </TabsContent>
            </Tabs>
        </div>
    );
};
