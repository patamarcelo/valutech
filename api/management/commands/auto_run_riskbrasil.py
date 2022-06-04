from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from api.models import ValuRisk
import datetime
import requests


def check_date(date):
    try:
        old_date = datetime.datetime.strptime(date, '%d.%m.%Y')
        new_date = old_date.strftime("%Y-%m-%d")
        return new_date
    except ValueError:
        return False

def check_date_valid(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class Command(BaseCommand):
    help = "collect jobs"
    SUMARIO = {
        0: 'Data',
        1: 'Fechamento',
        2: 'Abertura',
        3: 'Maxima',
        4: 'Minimo'
    }
    # define logic of command
    def handle(self, *args, **options):
        try:
            # collect html
            url = 'https://br.investing.com/rates-bonds/brazil-5-year-bond-yield-historical-data'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            list_p = soup.find_all(attrs={"data-real-value": True})
        except Exception as e:
            print(f'Erro: {e} - Problema ao pegar os dados em: {url}')
            print(type(e))
            print(e.args)
        query_list = []
        count_list = 0
        add_dict = {}

        if len(list_p) > 0:
            for i in list_p:
                value = i.get_text()
                verify_value = check_date(value)
                if count_list == 5:
                    query_list.append(add_dict)
                    count_list = 0
                    add_dict = {}
                if count_list < 5:
                    if verify_value == False:
                        add_dict[self.SUMARIO.get(count_list)] = value
                    else:
                        add_dict[self.SUMARIO.get(count_list)] = verify_value    
                count_list = count_list + 1

            print(len(query_list))
            count = 0
            list_obj = []
            for i in query_list[1:]:
                data_value = i['Data']
                abertura = float(i['Abertura'].replace(',', '.'))
                fechamento = float(i['Fechamento'].replace(',', '.'))
                maxima = float(i['Maxima'].replace(',', '.'))
                minimo = float(i['Minimo'].replace(',', '.'))
                try:
                    if check_date_valid(data_value) == True:
                        if ValuRisk.objects.filter(data=data_value).exists():
                            print(f"Operação já registrada: {data_value} - {fechamento}")
                        else:
                            nova_operacao = ValuRisk(
                                data=data_value,
                                abertura=abertura,
                                fechamento=fechamento,
                                minimo=minimo,
                                maxima=maxima,
                            )
                            nova_operacao.save()
                            print("Operação salva!!!!!")
                            count += 1
                            atualizacao_dict = {"data": data_value, "valor": fechamento}
                            list_obj.append(atualizacao_dict)
                except Exception as e:
                    print(f'Problema ao salvar a operação {data_value} - {fechamento} no DB - {e}')
                    print(type(e))
                    print(e.args)
            
            if count > 0:
                print(f'Abaixo as {count} operações que foram salva no DB:')        
                for i in list_obj:
                    print(i)
            else:
                print('Sem operações salvas no DB')

