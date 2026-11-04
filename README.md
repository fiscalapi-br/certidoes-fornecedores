# certidoes-fornecedores

Consulta CND Federal, CNDT e CRF/FGTS de uma lista de CNPJs pela [FiscalAPI](https://fiscalapi.com.br/?utm_source=github) e gera `certidoes.csv` com situação, validade, data para reconsultar, número e detalhe de cada certidão.

## Uso

1. `pip install -r requirements.txt`
2. Ponha sua chave em `HEADERS` no `certidoes.py`.
3. Um CNPJ por linha em `fornecedores.txt` (com ou sem máscara).
4. `python certidoes.py`

As pegadinhas que o script trata (positiva com efeitos de negativa, validade diferente por certidão, erro ≠ irregular, matriz, emissão demorada) estão explicadas no artigo do dev.to (link em breve).

Documentação da API: https://docs.fiscalapi.com.br/docs/certidoes-federais/consultar-cnd-federal

Licença MIT.
