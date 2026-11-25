'Distribua o tempo da reunião entre leitura, observação, interpretação e aplicação.'


from unicodedata import combining, normalize


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


def chave(value):
    return "".join(c for c in normalize("NFKD", texto(value).casefold()) if not combining(c))


ETAPAS = ("leitura", "observação", "interpretação", "aplicação")


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    if not isinstance(data["atividades"], list) or any(not isinstance(item, dict) for item in data["atividades"]):
        raise ValueError("O campo atividades deve ser uma lista de objetos.")
    limite = inteiro(data["minutos"], 1)
    atual, agenda = 0, []
    fases = {chave(fase): fase for fase in ETAPAS}
    for item in data["atividades"]:
        fase = chave(item["fase"])
        if fase not in fases:
            raise ValueError("Escolha leitura, observação, interpretação ou aplicação.")
        fim = atual + inteiro(item["minutos"], 1)
        if fim > limite:
            raise ValueError("O roteiro excede o tempo disponível.")
        agenda.append({"fase": fases[fase], "descricao": texto(item["descricao"]),
                       "inicio": atual, "fim": fim})
        atual = fim
    realizadas = {item["fase"] for item in agenda}
    resultado = {"referencia": texto(data["referencia"]), "agenda": agenda,
                 "fases_pendentes": [fase for fase in ETAPAS if fase not in realizadas],
                 "minutos_livres": limite - atual}
    if "hora_inicio" in data:
        from datetime import datetime
        hora = texto(data["hora_inicio"])
        if len(hora) != 5 or hora[2] != ":" or not (hora[:2] + hora[3:]).isascii() or not (hora[:2] + hora[3:]).isdigit():
            raise ValueError("Informe hora_inicio no formato HH:MM.")
        inicio = datetime.strptime(hora, "%H:%M")
        def horario(minutos):
            dias, resto = divmod(inicio.hour * 60 + inicio.minute + minutos, 1440)
            h, m = divmod(resto, 60)
            return {"hora": f"{h:02d}:{m:02d}", "dias_depois": dias}
        for etapa in agenda:
            etapa["hora_inicio"] = horario(etapa["inicio"])
            etapa["hora_fim"] = horario(etapa["fim"])
        resultado["hora_limite"] = horario(limite)
    return resultado


import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


MAX_JSON_BYTES = 1_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar as etapas e os minutos da reunião em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open("rb")
        with entrada as source:
            raw = source.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON excede o limite de 1 MB.")
        data = json.loads(
            raw.decode("utf-8-sig"),
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, UnicodeError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

