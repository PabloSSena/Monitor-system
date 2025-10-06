# Interface do Serviço de Monitoramento de Hosts

## Informações Gerais

**Protocolo:** WebSocket  
**Endpoint:** `ws://localhost:8765`  
**Formato de Mensagens:** JSON

---

## Operações Disponíveis

### 1. Iniciar Monitoramento de Host

Inicia o monitoramento periódico de um host específico.

**Requisição:**

```json
{
  "cmd": "monitor",
  "host": "string",
  "interval": "integer (opcional)"
}
```

**Parâmetros:**

- `cmd` (obrigatório): Deve ser `"monitor"`
- `host` (obrigatório): Nome do host ou endereço IP a ser monitorado
- `interval` (opcional): Intervalo em segundos entre verificações (padrão: 5)

**Exemplos de Requisição:**

```json
{
  "cmd": "monitor",
  "host": "google.com",
  "interval": 10
}
```

```json
{
  "cmd": "monitor",
  "host": "192.168.1.1"
}
```

---

## Respostas do Serviço

### Confirmação de Início de Monitoramento

```json
{
  "info": "Iniciando monitoramento de {host}"
}
```

### Status de Monitoramento (Periódico)

Enviado automaticamente a cada intervalo definido:

```json
{
  "host": "string",
  "tcp": "boolean"
}
```

**Campos:**

- `host`: Host que foi verificado
- `tcp`: `true` se a porta TCP 443 está aberta, `false` caso contrário

**Exemplo:**

```json
{
  "host": "google.com",
  "tcp": true
}
```

### Mensagens de Erro

**Host já sendo monitorado:**

```json
{
  "info": "{host} ja está sendo monitorado"
}
```

**Nenhum host fornecido:**

```json
{
  "error": "nenhum host fornecido"
}
```

**Comando inválido:**

```json
{
  "error": "comando invalido"
}
```

---

## Comportamento do Serviço

### Conexão

- O cliente estabelece uma conexão WebSocket com `ws://localhost:8765`
- A conexão permanece aberta para comunicação bidirecional

### Monitoramento Múltiplo

- É possível monitorar múltiplos hosts simultaneamente
- Cada host pode ter seu próprio intervalo de verificação
- Hosts são identificados de forma única pelo seu nome/endereço

### Verificação TCP

- O serviço verifica se a porta **443 (HTTPS)** está aberta
- Resultado enviado periodicamente ao cliente

### Encerramento

- Ao desconectar, todas as tasks de monitoramento são canceladas automaticamente
- Em caso de erro, as tasks são limpas e a conexão é encerrada

---
