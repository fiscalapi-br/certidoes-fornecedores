import csv
import re
import time
from datetime import date, timedelta

import requests

API = "https://api.fiscalapi.com.br/api"
HEADERS = {"X-API-Key": "fapi_sua_chave_aqui"}
ENDPOINTS = {
    "cnd_federal": "consultar-cnd-federal",
    "cndt": "consultar-cndt",
    "crf_fgts": "consultar-crf-fgts",
}
REGULAR = {"negativa", "positiva_com_efeitos_de_negativa"}
FOLGA = {"cnd_federal": 3, "cndt": 10, "crf_fgts": 5}  # ver pegadinha 2


def consultar(endpoint: str, cnpj: str, tentativas: int = 5) -> dict:
    data: dict = {"result": None, "source_status": {"error_code": "SEM_RESPOSTA"}}
    for tentativa in range(tentativas):
        r = requests.get(f"{API}/{endpoint}", headers=HEADERS,
                         params={"cnpj": cnpj}, timeout=120)
        if r.status_code in (401, 402, 403):  # chave errada ou sem saldo: não adianta seguir
            raise SystemExit(f"HTTP {r.status_code}: {r.text[:200]}")
        if r.status_code == 429:  # passou do limite por minuto do plano
            espera = int(r.headers.get("Retry-After", 60))
        elif r.status_code >= 400:
            return {"result": None, "source_status": {"error_code": f"HTTP_{r.status_code}"}}
        else:
            data = r.json()
            if (data.get("source_status") or {}).get("error_code") != "EM_PROCESSAMENTO":
                return data
            espera = int(r.headers.get("Retry-After", 30))  # pegadinha 5
        if tentativa < tentativas - 1:
            time.sleep(espera)
    return data


def situacao(data: dict) -> str:
    status = (data.get("result") or {}).get("status")
    if not status or status == "erro":
        return "pendente"
    return "regular" if status in REGULAR else "irregular"


def detalhe(data: dict) -> str:
    res = data.get("result") or {}
    return res.get("status_raw") or (data.get("source_status") or {}).get("error_code", "")


def normalizar(cnpj: str) -> str:
    cnpj = re.sub(r"[./\s-]", "", cnpj)
    return cnpj.zfill(14) if cnpj.isdigit() else cnpj


with open("fornecedores.txt", encoding="utf-8-sig") as f:
    cnpjs = [normalizar(linha) for linha in f if linha.strip()]

with open("certidoes.csv", "w", newline="", encoding="utf-8-sig") as saida:
    csv_out = csv.writer(saida, delimiter=";")  # ";" abre direto no Excel em português
    csv_out.writerow(["cnpj", "certidao", "situacao", "validade",
                      "reconsultar_em", "protocolo", "detalhe"])
    for cnpj in cnpjs:
        for tipo, endpoint in ENDPOINTS.items():
            data = consultar(endpoint, cnpj)
            res = data.get("result") or {}
            validade = res.get("validade_iso", "")
            quando = (date.fromisoformat(validade) - timedelta(days=FOLGA[tipo])
                      if validade else date.today())
            csv_out.writerow([cnpj, tipo, situacao(data), validade, quando.isoformat(),
                              res.get("protocolo", ""), detalhe(data)])
