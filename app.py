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
    return {"referencia": texto(data["referencia"]), "agenda": agenda,
            "fases_pendentes": [fase for fase in ETAPAS if fase not in realizadas],
            "minutos_livres": limite - atual}


import argparse
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8-sig") as source:
            data = json.load(source, object_pairs_hook=objeto_sem_campos_repetidos)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

