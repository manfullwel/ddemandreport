import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Loader2, Upload } from "lucide-react";
import { DailyReport } from '@/types/report';
import * as XLSX from 'xlsx';

interface FileUploadProps {
    onDataImported: (data: DailyReport[], fileName: string) => void;
}

export const FileUpload = ({ onDataImported }: FileUploadProps) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const processExcelFile = async (file: File) => {
        try {
            const data = await file.arrayBuffer();
            const workbook = XLSX.read(data);
            const worksheet = workbook.Sheets[workbook.SheetNames[0]];
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { 
                header: 1,
                raw: false,
                dateNF: 'yyyy-mm-dd'
            });

            // Log para debug
            console.log('Dados lidos do arquivo:', jsonData);

            if (jsonData.length > 0) {
                const reports = (jsonData as any[][]).slice(1).map((row): DailyReport => ({
                    Nome_Funcionario: row[0] || '',
                    Contratos_Resolvidos: parseInt(row[1]) || 0,
                    Pendentes_Receptivo: parseInt(row[2]) || 0,
                    Pendentes_Ativo: parseInt(row[3]) || 0,
                    Quitados: parseInt(row[4]) || 0,
                    Aprovados: parseInt(row[5]) || 0,
                    Data_Relatorio: new Date(row[6]),
                }));
                onDataImported(reports, file.name);
            } else {
                throw new Error('Arquivo vazio ou sem dados válidos');
            }
        } catch (err) {
            console.error('Erro ao processar arquivo:', err);
            throw new Error('Erro ao processar arquivo. Verifique se o formato está correto.');
        }
    };

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        setLoading(true);
        setError(null);

        try {
            const file = acceptedFiles[0];
            if (!file) {
                throw new Error('Nenhum arquivo selecionado');
            }

            await processExcelFile(file);
        } catch (err: any) {
            setError(err.message || 'Erro ao processar arquivo');
        } finally {
            setLoading(false);
        }
    }, [onDataImported]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/vnd.ms-excel': ['.xls'],
            'text/csv': ['.csv']
        },
        multiple: false
    });

    return (
        <div className="space-y-4">
            <div
                {...getRootProps()}
                className={`
                    border-2 border-dashed rounded-lg p-8
                    flex flex-col items-center justify-center
                    cursor-pointer transition-colors
                    ${isDragActive ? 'border-primary bg-primary/10' : 'border-gray-300'}
                `}
            >
                <input {...getInputProps()} />
                <Upload className="h-10 w-10 mb-4 text-gray-400" />
                <div className="text-center">
                    {isDragActive ? (
                        <p>Solte o arquivo aqui...</p>
                    ) : (
                        <>
                            <p className="text-lg font-medium">Arraste e solte seu arquivo aqui</p>
                            <p className="text-sm text-gray-500">ou clique para selecionar</p>
                            <p className="text-xs text-gray-400 mt-2">
                                Formatos suportados: XLSX, XLS, CSV
                            </p>
                        </>
                    )}
                </div>
            </div>

            {error && (
                <Alert variant="destructive">
                    <AlertTitle>Erro</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}

            {loading && (
                <div className="flex items-center justify-center">
                    <Loader2 className="h-6 w-6 animate-spin" />
                    <span className="ml-2">Processando arquivo...</span>
                </div>
            )}
        </div>
    );
};
