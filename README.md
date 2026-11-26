# Citizen Assist AI

Assistente em linha de comando (CLI) desenvolvido em Python para orientar cidadãos sobre serviços de transporte e atendimento público em São Paulo, com busca por pontuação, suporte a sinônimos, aprendizado interativo salvo em JSON, relatório de uso e exportação em CSV.

## Identificação
- Nome: Pedro Vianna
- RM: 570747
- Tema: Serviços de Transporte Público e Atendimento ao Cidadão (SPTrans / Mobilidade e Atendimento)

## Estrutura do Projeto
- `main.py`: ponto de entrada e menu principal no terminal.
- `orientacao.py`: classe `Orientacao` e serialização via `para_dict()`.
- `base_conhecimento.py`: classe `BaseConhecimento`, leitura/escrita JSON, normalização, pontuação com sinônimos, extração de palavras candidatas e ranking.
- `assistente.py`: classe `Assistente` (composição com `BaseConhecimento`), fluxos de pergunta, navegação por categorias, aprendizado, validações, relatório e exportação CSV.
- `data/base_conhecimento.json`: base de orientações em formato JSON.
- `data/sinonimos.json`: dicionário de sinônimos para expansão de busca.
- `data/relatorio.csv`: relatório exportado com métricas de acesso por orientação.

## Como Executar
Certifique-se de ter o **Python 3** instalado (utiliza apenas a biblioteca padrão do Python). No terminal, dentro da pasta `citizen-assist-ai`, execute:

```bash
python main.py
