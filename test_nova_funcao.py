import unittest
from app import run

class Horarios(unittest.TestCase):
    def test_virada_do_dia(self):
        result = run({"referencia":"Jo 15","minutos":40,"hora_inicio":"23:50","atividades":[{"fase":"leitura","descricao":"Ler","minutos":20}]})
        self.assertEqual(result["agenda"][0]["hora_fim"], {"hora":"00:10","dias_depois":1})
        self.assertEqual(result["hora_limite"], {"hora":"00:30","dias_depois":1})
    def test_invalid(self):
        for hora in ("25:00", "9:00", "12:60"):
            with self.assertRaises(ValueError):
                run({"referencia":"Jo 15","minutos":10,"hora_inicio":hora,"atividades":[]})
