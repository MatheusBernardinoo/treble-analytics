---
name: informar-relatorio
description: Localiza o HTML do relatório validado e informa o caminho completo ao operador. Último passo do pipeline — o projeto encerra aqui.
allowed-tools: Glob, Read
---

# informar-relatorio

## Procedimento

### 1. Localizar o .html gerado
O arquivo está em `analises/[período] (geral)/[nome do relatório].html`. Localizar com Glob:
```
Glob: analises/**/Relat*.html
```
(ou confirmar o caminho da pasta da janela criada pelo Organizador).

### 2. Informar o caminho ao operador
```
O relatório está pronto em:
[caminho completo do .html]

Upload e distribuição são de responsabilidade do operador.
```

## Regras
- Não editar o relatório nem reescrever os destaques.
- Só informar o caminho. Este template não envia e-mail nem mensagens — a distribuição é manual, feita pelo operador.
- O pipeline encerra aqui.
