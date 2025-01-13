# Sistema de Controle de Demandas

Sistema web para controle e análise de contratos, com foco em relatórios diários e auditoria.

## Funcionalidades

- Dashboard de análise diária por grupos e funcionários
- Monitoramento de contratos (Quitados, Pendentes, Aprovados)
- Sistema de auditoria para rastreamento de alterações
- Interface responsiva e moderna

## Tecnologias Utilizadas

- React
- TypeScript
- Tailwind CSS
- Vite

## Requisitos

- Node.js 16+
- npm ou yarn

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/manfullwel/ddemandreport.git
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

## Estrutura de Arquivos

- `/src` - Código fonte
  - `/components` - Componentes React
  - `/data` - Dados mockados e tipos
  - `App.tsx` - Componente principal
  - `main.tsx` - Ponto de entrada

## Scripts Disponíveis

- `npm run dev` - Inicia o servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run preview` - Visualiza build de produção

## Estrutura de Dados

### Relatório Diário (Relatorio_Analise_Diaria.csv)
- Nome do Funcionário
- Contratos Resolvidos
- Pendentes (Receptivo/Ativo)
- Quitados
- Aprovados
- Data do Relatório

### Contratos (Contratos_Gerais.csv)
- Número do Contrato
- Nome do Cliente
- Banco Recebedor
- Responsável
- Status do Contrato
- Data de Atualização

## Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

MIT

## Autor

Igor Soares

---

⭐️ Se este projeto te ajudou, considere dar uma estrela!