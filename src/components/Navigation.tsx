import { Link } from 'react-router-dom';
import { cn } from "@/lib/utils";
import { BarChart2, FileSpreadsheet, Home } from 'lucide-react';

interface NavigationProps {
    currentPath: string;
}

export const Navigation = ({ currentPath }: NavigationProps) => {
    const links = [
        {
            href: '/',
            icon: Home,
            label: 'Relatório Diário'
        },
        {
            href: '/analytics',
            icon: BarChart2,
            label: 'Dashboard'
        },
        {
            href: '/data',
            icon: FileSpreadsheet,
            label: 'Dados'
        }
    ];

    return (
        <nav className="border-b">
            <div className="max-w-screen-xl mx-auto px-4">
                <div className="flex h-14 items-center space-x-4">
                    {links.map(({ href, icon: Icon, label }) => (
                        <Link
                            key={href}
                            to={href}
                            className={cn(
                                "flex items-center space-x-2 px-3 py-2 text-sm font-medium rounded-md",
                                currentPath === href
                                    ? "bg-primary text-primary-foreground"
                                    : "text-muted-foreground hover:bg-muted"
                            )}
                        >
                            <Icon className="h-4 w-4" />
                            <span>{label}</span>
                        </Link>
                    ))}
                </div>
            </div>
        </nav>
    );
};
