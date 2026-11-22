# certidoes-fornecedores

Script em Python que puxa a CND Federal (Receita Federal e PGFN), a CNDT (TST) e o CRF/FGTS (Caixa) de uma lista de CNPJs pela API da [FiscalAPI](https://fiscalapi.com.br/?utm_source=github) e gera `certidoes.csv` com situação, validade, data para reconsultar, número e detalhe de cada certidão. A CND Federal vem pronta: a que ainda vale ou uma emitida na hora.

## Uso

1. `pip install -r requirements.txt`
2. Ponha sua chave em `HEADERS` no `certidoes.py`.
3. Um CNPJ por linha em `fornecedores.txt` (com ou sem máscara).
4. `python certidoes.py`

As pegadinhas que o script trata (positiva com efeitos de negativa, validade diferente por certidão, erro ≠ irregular, matriz, emissão demorada) estão explicadas [neste artigo no dev.to](https://dev.to/ludwigedward/5-pegadinhas-que-aprendi-automatizando-cnd-federal-cndt-e-fgts-em-python-2kj5).

## Documentação da API

- Guia deste caso (certidões de fornecedores): https://docs.fiscalapi.com.br/docs/guias/certidoes-fornecedor
- CND Federal: https://docs.fiscalapi.com.br/docs/certidoes-federais/consultar-cnd-federal
- CNDT: https://docs.fiscalapi.com.br/docs/certidoes-federais/consultar-cndt
- CRF/FGTS: https://docs.fiscalapi.com.br/docs/certidoes-federais/consultar-crf-fgts

Pela API, toda consulta pede plano ou créditos extras, a partir de R$ 50 por mês.

Licença MIT.
