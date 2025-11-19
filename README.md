# ✈️ Agente de Manutenção Preditiva para Motores Aeronáuticos

**Um assistente inteligente para análise de telemetria e suporte à decisão na manutenção de motores de aeronaves.**

---

## 📖 Visão Geral

Este projeto implementa um agente especializado, construído com o Google AI, para atuar como um copiloto para engenheiros e mecânicos de manutenção aeronáutica. O agente analisa dados de telemetria em tempo real — como **Temperatura dos Gases de Exaustão (EGT)**, **vibração**, **pressão do óleo** e **ciclos de voo** — para fornecer diagnósticos precisos e recomendações de manutenção acionáveis.

O principal objetivo é aumentar a segurança operacional, otimizar os processos de manutenção e reduzir o tempo de inatividade da aeronave (AOG - Aircraft on Ground), seguindo uma lógica de diagnóstico hierárquica que espelha os protocolos da indústria.

---

## ✨ Principais Funcionalidades

- **Análise Hierárquica de Falhas:** O agente prioriza as condições mais críticas, garantindo que os problemas de maior risco (como falhas mecânicas severas) sejam identificados primeiro.
- **Diagnóstico Estruturado:** As respostas são fornecidas em um formato `JSON` claro e consistente, incluindo:
  - `status`: Nível de severidade (e.g., `CRITICAL`, `WARNING`, `NORMAL`).
  - `action`: Ação recomendada para a equipe de solo.
  - `reason`: Justificativa técnica para o diagnóstico.
  - `ata_chapter`: Referência ao capítulo do manual ATA correspondente, agilizando a consulta de documentação.
  - `confidence`: Nível de confiança do diagnóstico.
- **Validação de Dados:** Utiliza `Pydantic` para garantir que os dados de telemetria de entrada sejam válidos e estejam dentro dos limites esperados antes de qualquer análise.
- **Lógica Baseada em Limites Operacionais:** As regras de diagnóstico são baseadas em constantes que representam os limites de operação e segurança do motor, como `LIMIT_EGT_MAX`, `LIMIT_VIB_MAX`, etc.

---

## ⚙️ Como Funciona: A Lógica de Diagnóstico

O núcleo do agente é a função `analyze_engine_health`, que processa a telemetria do motor através de uma série de verificações priorizadas:

1.  **Condição Crítica (Risco Imediato de Voo):**
    - **Gatilho:** Vibração excessivamente alta (`> LIMIT_VIB_MAX`) ou uma combinação perigosa de vibração e EGT (`vibration > 1.6` e `egt > LIMIT_EGT_CRITICAL`).
    - **Ação:** `INTERDIÇÃO DE VOO (AOG)`. Recomenda boroscopia mandatória e possível troca do motor.
    - **ATA Chapter:** `72-00-00` (Motor).

2.  **Manutenção Preventiva (Fim de Vida Útil):**
    - **Gatilho:** O número de ciclos acumulados excede o limite de vida útil do componente (`cycles > LIMIT_CYCLES_LIFE`).
    - **Ação:** Planejar a remoção do motor para revisão geral (Overhaul).
    - **ATA Chapter:** `05-10-00` (Manutenção Programada).

3.  **Alerta (Condição Fora do Normal):**
    - **Gatilho:** Parâmetros que saem da faixa nominal, mas não representam risco imediato.
      - Pressão do óleo abaixo do mínimo (`oil_pressure < LIMIT_OIL_MIN`).
      - EGT acima do limite máximo, mas abaixo do crítico (`LIMIT_EGT_MAX < egt <= LIMIT_EGT_CRITICAL`).
    - **Ação:** Realizar testes de solo e verificar componentes como filtros.
    - **ATA Chapter:** `79-00-00` (Sistema de Óleo) ou `72-00-00` (Motor).

4.  **Condição Normal:**
    - **Gatilho:** Nenhum dos limites acima foi violado.
    - **Ação:** Motor liberado para serviço, sem necessidade de intervenção.

---

## 🏗️ Estrutura do Projeto

```
engine_suport/
├── __init__.py           # Inicializa o pacote do agente
├── agent.py              # Define o agente principal e sua configuração
├── prompt/
│   ├── __init__.py
│   └── prompt.py         # Contém os templates de prompt para o LLM
├── schema/
│   └── schemas.py        # Define os modelos de dados (Pydantic) para telemetria
└── tool/
    ├── __init__.py
    ├── constants.py      # Constantes de limites operacionais do motor
    └── tool.py           # Contém a lógica principal de diagnóstico (analyze_engine_health)
```

---

## 🚀 Como Executar

Este agente foi desenvolvido para ser executado dentro do ecossistema do **ADK (Agent Development Kit)** do Google.

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure as variáveis de ambiente:**
    Crie uma cópia do arquivo `.env.example` e renomeie-a para `.env`. Em seguida, preencha o valor da sua chave de API do Google.

    ```bash
    # No Windows (Command Prompt)
    copy .env.example .env
    ```
    O conteúdo do arquivo `.env` deve ser semelhante a:
    ```
    GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
    ```

3.  **Inicie o servidor do ADK:**
    ```bash
    adk web
    ```

4.  **Interaja com o agente:**
    Acesse a interface web do ADK (geralmente em `http://127.0.0.1:8000`) para enviar solicitações de análise ao agente `engine_suport`.

### Exemplo de Chamada da Ferramenta

Internamente, o agente invoca a ferramenta de análise da seguinte forma:

```python
analyze_engine_health(
    egt=955.0,
    vibration=1.8,
    oil_pressure=85.0,
    cycles=15200
)
```
### ADK web

<img width="1850" height="940" alt="Image" src="https://github.com/user-attachments/assets/0c17f8ff-7b59-4479-84c2-89715ca48def" />
---

## 🤝 Contribuição

Contribuições são bem-vindas! Para sugestões, melhorias na lógica de diagnóstico ou novas funcionalidades, por favor, abra uma *Issue* ou envie um *Pull Request*.
