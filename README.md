# Roteiro para grupo bíblico

Distribua o tempo da reunião entre leitura, observação, interpretação e aplicação.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Informe o tempo total e as atividades com minutos inteiros. O resultado traz horários relativos, espaço livre e as etapas que ainda precisam ser contempladas.

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar as etapas e os minutos da reunião. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```


## Horários reais da reunião

Adicione a propriedade opcional `"horario_inicial": "19:30"` ao objeto JSON
de entrada para calcular os horários reais de cada atividade. Na saída JSON,
`inicio_real` e `fim_real` contêm o horário no formato HH:MM e o deslocamento
de dia (0 = dia inicial; 1 = dia seguinte). Por exemplo, uma atividade de
20 minutos que começa às 23:50 termina às 00:10 no dia 1. Sem a propriedade,
a saída anterior permanece igual. O CSV mantém os minutos relativos.
