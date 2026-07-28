---
name: atualizar-memoria
description: Escreve no MEMORIA_APRENDIZADO.md na seção certa, datado, sem duplicar; incrementa o contador de execuções e adiciona a linha de histórico da semana. Usar após curar-aprendizados.
allowed-tools: Read, Edit, Write
---

# atualizar-memoria

## Procedimento
1. Abrir `MEMORIA_APRENDIZADO.md` (raiz do projeto). Se não existir, criar com a estrutura de seções fixas do CLAUDE.md §5.1.
2. Para cada item aprovado pela curadoria, escrever na seção certa:
   - §1 Convenções confirmadas · §2 Padrões recorrentes · §3 Armadilhas resolvidas · §4 Ajustes sugeridos (pendentes).
   - Formato de armadilha: `[AAAA-MM-DD] Sintoma: ... | Causa: ... | Solução: ... | Agente: ...`
3. Antes de adicionar, procurar se o item já existe; se sim, atualizar a data em vez de duplicar.
4. Atualizar o cabeçalho: `Última atualização: {AAAA-MM-DD}` e incrementar `Execuções acumuladas`.
5. Adicionar a linha de histórico em §5: `[semana DD/MM–DD/MM] {ok | com alertas}, {1 frase do que marcou}`.

## Regras
- Só registrar quando algo relevante aconteceu, não a cada execução por obrigação.
- Nunca dados sensíveis. Respeitar o teto por seção (~15 itens).
- Datas relativas viram absolutas.
