# Dicionário de Dados — arquivo unificado

O arquivo unificado (`Dados_Treble_Semana.xlsx`) tem 3 abas essenciais. Os scripts identificam cada
aba **pelas colunas** (não pelo nome), então o importante é que as colunas abaixo existam. Veja
`exemplo/gerar_dados_exemplo.py` para um exemplo executável do schema.

> Os nomes de coluna são casados por um matcher tolerante (ignora acentos, espaços, maiúsculas). Use
> os nomes canônicos abaixo para não ter surpresa.

## Aba `atendimento-treble` — base de verdade (1 linha por conversa com vendedor)

Identificada por ter as colunas `agent` + `finish_type` (e `last_message_sender`).

| Coluna | Descrição |
|---|---|
| `phone` | Telefone do contato (identificador; o match ignora o prefixo 55) |
| `agent` | Vendedor que recebeu a conversa (deve casar com `AGENTES_CANONICOS`) |
| `created_at` | Timestamp de criação da conversa |
| `assigned_at` | Timestamp de atribuição ao vendedor |
| `agent_first_message` | Timestamp da 1ª resposta do vendedor (vazio = não respondida) |
| `finish_type` | Tipo de encerramento: `AUTO` ou `MANUAL` |
| `last_message_sender` | Quem enviou a última mensagem (`AGENT` / `USER` / `IA`) |
| `last_transfer_from` | E-mail de quem **originou** a última transferência (vazio se não houve) |
| `last_transfer_time` | Timestamp da última transferência |

Derivadas pelo script: `respondido`, `respondido_24h`, `tempo_1a_resposta_h` (= `agent_first_message` − `assigned_at`, em horas).

## Aba `sessoes-gerais` — log de sessões do fluxo

Identificada por ter a coluna `user_cellphone`.

| Coluna | Descrição |
|---|---|
| `user_cellphone` | Telefone do contato |
| `session_started_timestamp` | Início da sessão |
| `first_message_timestamp` | 1ª mensagem |
| `last_message_timestamp` | Última mensagem |
| `session_finished_timestamp` | Fim da sessão |
| `session_status` | Estado (ex.: `HumanHandover`, `Completed`, `Expired`, `InProgress`) |
| `conversation_version` | Número da versão do fluxo |
| `last_message`, `last_node_id` | Auxiliares |

## Aba `Versao N` — qualificação do fluxo (variáveis do CRM)

Uma aba por versão do fluxo (`Versao 1`, `Versao 2`, …). Identificada por ter a coluna `Celular` e um
número no nome da aba. As colunas são as variáveis capturadas pelo fluxo:

| Coluna | Descrição |
|---|---|
| `Celular` | Telefone do contato |
| `você é novo por aqui ou já é cliente?` | **Primeira pergunta** — define o caminho: `Sou novo por aqui` / `Já sou cliente` / vazio |
| `hubspot_email` | E-mail |
| `hubspot_firstname` | Nome |
| `hubspot_company` | Empresa |
| `hubspot_cpf` / `hubspot_cnpj` | CPF/CNPJ (contam como preenchido se qualquer um existir) |
| `hubspot_state` / `hubspot_city` | Estado / cidade |
| `hubspot_tipo_de_residuo` | Tipo de resíduo (ex.: `Industrial`, `Hospitalar`) — **fluxo de exemplo** |
| `hubspot_truora_classe_residuo` | Classe (ex.: `Perigoso (Classe 1)`, `Não perigoso (Classe 2)`, `Não sei informar`) |
| `hubspot_truora_quantidade_residuo` | Quantidade de resíduo |
| `hubspot_truora_tipo_de_servico` | Tipo de serviço |

> **Adaptação:** as colunas `hubspot_*` de resíduo e a lista de campos por caminho (`FLOW_NOVO` /
> `FLOW_CLI` em `scripts/geral/_analise_comum.py`) são específicas de um fluxo de gestão de resíduos
> (o exemplo de referência). Ajuste-as para os campos do seu fluxo.
