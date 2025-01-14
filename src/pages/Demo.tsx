import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

export const Demo: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Sistema de Gestão de Demandas
          </h1>
          <p className="text-xl text-gray-600">
            Uma solução completa para gerenciamento e análise de demandas em tempo real
          </p>
        </div>

        {/* Seção Desktop */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">Versão Desktop</h2>
          
          {/* Relatório Geral */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-2xl">Relatório Geral</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <img 
                    src="/screenshots/relatorio-geral-1.png" 
                    alt="Relatório Geral - Parte 1"
                    className="rounded-lg shadow-lg"
                  />
                  <p className="mt-4 text-gray-600">
                    Visão completa das demandas do Julio, incluindo resolvidos,
                    pendentes e análises do dia.
                  </p>
                </div>
                <div>
                  <img 
                    src="/screenshots/relatorio-geral-2.png" 
                    alt="Relatório Geral - Parte 2"
                    className="rounded-lg shadow-lg"
                  />
                  <p className="mt-4 text-gray-600">
                    Métricas detalhadas da equipe Adriano/Leandro, com total de
                    quitados e aprovados.
                  </p>
                </div>
              </div>
              <div className="mt-6">
                <Link to="/relatorio-geral">
                  <Button>Ver Relatório Geral</Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Relatório Diário */}
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Relatório Diário</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-6">
                <img 
                  src="/screenshots/relatorio-diario.png" 
                  alt="Relatório Diário"
                  className="rounded-lg shadow-lg w-full"
                />
                <p className="mt-4 text-gray-600">
                  Acompanhamento diário de todas as atividades, com métricas
                  atualizadas e gráficos comparativos.
                </p>
              </div>
              <Link to="/relatorio-diario">
                <Button>Ver Relatório Diário</Button>
              </Link>
            </CardContent>
          </Card>
        </section>

        {/* Seção Mobile */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">Versão Mobile</h2>
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Acesso Mobile</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-8">
                <div>
                  <img 
                    src="/screenshots/mobile-dashboard.png" 
                    alt="Dashboard Mobile"
                    className="rounded-lg shadow-lg"
                  />
                  <p className="mt-4 text-gray-600">
                    Dashboard otimizado para dispositivos móveis.
                  </p>
                </div>
                <div>
                  <img 
                    src="/screenshots/mobile-notifications.png" 
                    alt="Notificações Mobile"
                    className="rounded-lg shadow-lg"
                  />
                  <p className="mt-4 text-gray-600">
                    Sistema de notificações em tempo real.
                  </p>
                </div>
                <div>
                  <img 
                    src="/screenshots/mobile-analysis.png" 
                    alt="Análises Mobile"
                    className="rounded-lg shadow-lg"
                  />
                  <p className="mt-4 text-gray-600">
                    Visualização de análises e métricas importantes.
                  </p>
                </div>
              </div>
              <div className="mt-8">
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-xl font-semibold mb-4">
                    Principais Características
                  </h3>
                  <ul className="grid md:grid-cols-2 gap-4">
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                      Interface intuitiva e responsiva
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                      Notificações push para demandas urgentes
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                      Atualização em tempo real
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                      Acesso rápido às métricas principais
                    </li>
                  </ul>
                </div>
                <div className="mt-6">
                  <Link to="/mobile">
                    <Button>Experimentar Versão Mobile</Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Agradecimentos */}
        <section>
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Agradecimentos Especiais</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-blue-50 rounded-lg p-6">
                <p className="text-gray-700 mb-4">
                  Um agradecimento especial à <strong>Ediane F.</strong>, cuja experiência
                  e sugestões foram fundamentais para o desenvolvimento desta ferramenta.
                  Suas contribuições ajudaram a criar uma solução que realmente atende
                  às necessidades da equipe.
                </p>
                <p className="text-gray-700">
                  Suas dicas sobre o fluxo de trabalho e necessidades reais do ambiente
                  corporativo foram essenciais para tornar esta ferramenta mais
                  eficiente e prática.
                </p>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  );
};
