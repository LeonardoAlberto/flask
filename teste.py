from datetime import datetime
from dateutil.relativedelta import relativedelta


def aumentar(meses, data_atual):
    try:
        data = datetime.strptime(f"{data_atual}", "%Y-%m-%d")
    except ValueError:
        print("Erro: A data de entrada é inválida!")
        return None

    data_proximo_mes = data + relativedelta(months=meses, day=data.day)

    dia_atual = data.day
    proximo_dia = data_proximo_mes.day

    if dia_atual == proximo_dia:
        return data_proximo_mes
    else:
        data_proximo_mes = data + relativedelta(months=meses - 1)
        data_proximo_mes = data_proximo_mes + relativedelta(days=30)
        return data_proximo_mes


def validar_data_hora(data_hora):
    try:
        datetime.strptime(data_hora, '%Y/%m/%d-%H:%M')
        return True
    except ValueError:
        return False
