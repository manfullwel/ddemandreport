export interface DailyReport {
    Nome_Funcionario: string;
    Contratos_Resolvidos: number;
    Pendentes_Receptivo: number;
    Pendentes_Ativo: number;
    Quitados: number;
    Aprovados: number;
    Data_Relatorio: Date;
}

export interface Demanda {
    Nome: string;
    Grupo: string;
    Banco: string;
    Status: string;
    Prioridade: string;
    Analises_do_Dia: number;
    Quitado: boolean;
    Aprovado: boolean;
    Receptivo: boolean;
}

export interface ReportFilters {
    startDate?: Date;
    endDate?: Date;
    funcionario?: string;
    banco?: string;
    grupo?: string;
    status?: string;
}

export const INITIAL_FILTERS: ReportFilters = {
    startDate: new Date('2025-01-01'),
    endDate: new Date('2025-01-15'),
    funcionario: undefined,
    banco: undefined,
    grupo: undefined,
    status: undefined
};
