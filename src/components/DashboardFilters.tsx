import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { CalendarIcon } from "lucide-react";
import { ReportFilters, INITIAL_FILTERS } from '@/types/report';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface DashboardFiltersProps {
    onFilterChange: (filters: ReportFilters) => void;
}

export const DashboardFilters = ({ onFilterChange }: DashboardFiltersProps) => {
    const [filters, setFilters] = useState<ReportFilters>(INITIAL_FILTERS);
    const [startDateOpen, setStartDateOpen] = useState(false);
    const [endDateOpen, setEndDateOpen] = useState(false);

    const handleFilterChange = (newFilters: Partial<ReportFilters>) => {
        const updatedFilters = { ...filters, ...newFilters };
        setFilters(updatedFilters);
        onFilterChange(updatedFilters);
    };

    return (
        <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Filtros do Relatório</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Filtro de Funcionário */}
                <div className="space-y-2">
                    <Label htmlFor="employee">Funcionário</Label>
                    <Select 
                        value={filters.employeeName || ''} 
                        onValueChange={(value) => handleFilterChange({ employeeName: value })}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Selecione um funcionário" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Todos</SelectItem>
                            <SelectItem value="Julio">Julio</SelectItem>
                            <SelectItem value="Adriano/Leandro">Adriano/Leandro</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                {/* Data Inicial */}
                <div className="space-y-2">
                    <Label>Data Inicial</Label>
                    <Popover open={startDateOpen} onOpenChange={setStartDateOpen}>
                        <PopoverTrigger asChild>
                            <Button variant="outline" className="w-full justify-start text-left font-normal">
                                <CalendarIcon className="mr-2 h-4 w-4" />
                                {filters.startDate ? (
                                    format(filters.startDate, "dd/MM/yyyy", { locale: ptBR })
                                ) : (
                                    <span>Selecione a data</span>
                                )}
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                                mode="single"
                                selected={filters.startDate}
                                onSelect={(date) => {
                                    handleFilterChange({ startDate: date || new Date() });
                                    setStartDateOpen(false);
                                }}
                                initialFocus
                                locale={ptBR}
                            />
                        </PopoverContent>
                    </Popover>
                </div>

                {/* Data Final */}
                <div className="space-y-2">
                    <Label>Data Final</Label>
                    <Popover open={endDateOpen} onOpenChange={setEndDateOpen}>
                        <PopoverTrigger asChild>
                            <Button variant="outline" className="w-full justify-start text-left font-normal">
                                <CalendarIcon className="mr-2 h-4 w-4" />
                                {filters.endDate ? (
                                    format(filters.endDate, "dd/MM/yyyy", { locale: ptBR })
                                ) : (
                                    <span>Selecione a data</span>
                                )}
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                                mode="single"
                                selected={filters.endDate}
                                onSelect={(date) => {
                                    handleFilterChange({ endDate: date || new Date() });
                                    setEndDateOpen(false);
                                }}
                                initialFocus
                                locale={ptBR}
                            />
                        </PopoverContent>
                    </Popover>
                </div>
            </div>
        </div>
    );
};
