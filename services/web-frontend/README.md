# Frontend - Plataforma de Análise de Risco de Crédito

Este é o frontend da aplicação de análise de risco de crédito, construído com React, TypeScript e Tailwind CSS.

## Instalação

1. Instale as dependências:
```bash
npm install --ignore-scripts
```

**Nota:** No Windows, pode ser necessário usar a flag `--ignore-scripts` para evitar problemas com scripts pós-instalação do rollup. O projeto funciona normalmente sem executar esses scripts.

## Execução

Para executar o servidor de desenvolvimento:

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:5173` (ou outra porta se 5173 estiver ocupada).

## Build

Para gerar a build de produção:

```bash
npm run build
```

Os arquivos compilados estarão na pasta `dist/`.

## Funcionalidades

- Upload de arquivos CSV e Excel (.csv, .xlsx, .xls)
- Drag and drop de arquivos
- Validação de tipos de arquivo
- Feedback visual de status (sucesso/erro)
- Interface responsiva e moderna

## Estrutura

- `src/App.tsx` - Componente principal da aplicação
- `src/main.tsx` - Ponto de entrada da aplicação
- `src/index.css` - Estilos globais com Tailwind CSS

