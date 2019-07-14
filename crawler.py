from lxml.html import fromstring, tostring
import csv
import json
import requests
import sys

"""***********************************************************************************
*       Descrição       :       Download do código HTML de uma página
*       Parametros      :       URL a ser baixada, Numero de tentativas caso ocorra 
*                               algum erro (default:2)
*       Retorno         :       (String) código HTML
**********************************************************************************"""
def download(url, num_retries=2, user_agent='wswp', proxies=None):
    print('Downloading:', url)
    headers = {'User-Agent': user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, stream=True)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
        html = None
    return html

"""***********************************************************************************
*       Descrição       :       Escreve os dados no console
*       Parametros      :       Dados a serem printados no console
*       Retorno         :       Nenhum
**********************************************************************************"""
def console_print(data):
    length = len(data)
    n_index = len(data[0])

    for i in range(length):
        print_string = ''
        for j in range(n_index):
            print_string += data[i][j]+"\t\t"
        print(print_string.expandtabs(15))
    print("-"*130)

"""***********************************************************************************
*       Descrição       :       Escreve os dados em um arquivo JSON
*       Parametros      :       Dados a serem escritos no arquivo JSON
*       Retorno         :       Nenhum
**********************************************************************************"""
def json_save(data,title):
    length = len(data) - 1
    n_index = len(data[0])

    json_data = {}
    for i in range(length):
        dummy_dict = {}
        for j in range(n_index):
            dummy_dict[data[0][j]] = data[i+1][j]
        json_data['machine ' + str(i+1)] = dummy_dict

    with open(title,'w') as json_file:
        json.dump(json_data,json_file)

"""***********************************************************************************
*       Descrição       :       Escreve os dados em um arquivo CSV
*       Parametros      :       Dados a serem escritos no arquivo CSV
*       Retorno         :       Nenhum
**********************************************************************************"""
def csv_save(data,title):
    length = len(data)

    with open(title,'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file,delimiter=';')

        for i in range(length):
            csv_writer.writerow(data[i])


"""***********************************************************************************
*       Descrição       :       Crawler da pagina-alvo 1
*       Parametros      :       Habilita escrita no console, Habilita arquivo JSON,
*                               Habilita arquivo CSV
*       Retorno         :       Nenhum
**********************************************************************************"""
def crawler_page1(console_print_var = False, json_save_var = False, csv_save_var = False):
    print("-" * 130)
    url = 'https://www.vultr.com/products/cloud-compute/'
    info = []
    html = download(url)
    tree = fromstring(html)

    #pega o cabeçalho da tabela
    i = 2
    dummy = []
    while i > 0:
        area = tree.xpath('//*[@id="compute"]/div[1]/div[1]/div['+str(i)+']/text()')
        if not area:
            i = 0
        else:
            dummy.append(area[0])
            i += 1
    info.append(dummy)

    #pega as informaçoes de cada linha da tabela
    i = 2
    while i > 0:
        area = tree.xpath('//*[@id="compute"]/div[1]/div[2]/div['+str(i)+']')
        if not area:
            i = 0
        else:
            dummy = []
            j = 2
            while j > 0:
                area = tree.xpath('//*[@id="compute"]/div[1]/div[2]/div['+str(i)+']/div[1]/div['+str(j)+']/span/strong/text()')
                if not area:
                    area = tree.xpath('//*[@id="compute"]/div[1]/div[2]/div['+str(i)+']/div[1]/div['+str(j)+']/strong/text()')
                    if not area:
                        j = 0
                    else:
                        dummy.append(area[0])
                        j += 1
                else:
                    dummy.append(area[0])
                    j += 1
            i += 1

            info.append(dummy)

    if console_print_var is True:
        console_print(info)
    if json_save_var is True:
        json_save(info,'page1.json')
    if csv_save_var is True:
        csv_save(info,'page1.csv')

"""***********************************************************************************
*       Descrição       :       Crawler da pagina-alvo 2
*       Parametros      :       Habilita escrita no console, Habilita arquivo JSON,
*                               Habilita arquivo CSV
*       Retorno         :       Nenhum
**********************************************************************************"""
def crawler_page2(console_print_var = False, json_save_var = False, csv_save_var = False):
    url = 'https://www.digitalocean.com/pricing/'
    info = []
    html = download(url)
    tree = fromstring(html)

    # pega o cabeçalho da tabela
    i = 1
    dummy = []
    while i > 0:
        area = tree.xpath('//*[@id="standard-droplets-pricing-table"]/div/div/table/thead/tr/th['+str(i)+']/text()')
        if not area:
            i = 0
        else:
            text_dummy = area[0]
            text_final = text_dummy.strip(' \n\t')
            dummy.append(text_final)
            i += 1
    info.append(dummy)

    # pega as informaçoes de cada linha da tabela
    i = 1
    length = len(info[0])
    while i > 0:
        area = tree.xpath('//*[@id="standard-droplets-pricing-table"]/div/div/table/tbody/tr['+str(i)+']')
        if not area:
            i = 0
        else:
            dummy = []
            j = 1
            while j > 0:
                area = tree.xpath('//*[@id="standard-droplets-pricing-table"]/div/div/table/tbody/tr['+str(i)+']'+
                                  '/td['+str(j)+']/strong/text()')
                if not area:
                    area = tree.xpath('//*[@id="standard-droplets-pricing-table"]/div/div/table/tbody/tr['+str(i)+']'+
                                      '/td['+str(j)+']/text()')
                    if not area:
                        j = 0
                    else:
                        if j <= length:
                            text_dummy = area[0]
                            text_final = text_dummy.strip(' \n\t')
                            dummy.append(text_final)
                            j += 1
                        else:
                            j = 0
                else:
                    if j <= length:
                        text_dummy = area[0]
                        text_final = text_dummy.strip(' \n\t')
                        dummy.append(text_final)
                        j += 1
                    else:
                        j = 0
            i += 1

            info.append(dummy)

    if console_print_var is True:
        console_print(info)
    if json_save_var is True:
        json_save(info, 'page2.json')
    if csv_save_var is True:
        csv_save(info, 'page2.csv')

"""***********************************************************************************
*       Descrição       :       Decodifica argumentos para chamar função correta
*       Parametros      :       Array de Argumentos
*       Retorno         :       Nenhum
**********************************************************************************"""
def main(argv,num_argv):
    enable_print = False
    enable_json  = False
    enable_csv   = False

    if(num_argv <= 1):
        print("crawler.py --help | --print | --save_json")
    else:
        if '--print' in argv:
            enable_print = True
        if '--save_json' in argv:
            enable_json = True
        if '--save_csv' in argv:
            enable_csv = True

        if '--help' in argv:
            print("--print\t\t Escreve na tela o resultado obtido pelo crawler\n"+
                  "--save_json\t Salva o resultado obtido pelo crawler em um arquivo json\n"+
                  "--save_csv\t Salva o resultado obtido pelo crawler em arquivos csv")
        else:
            crawler_page1(enable_print,enable_json,enable_csv)
            crawler_page2(enable_print, enable_json, enable_csv)


"""***********************************************************************************
*       Descrição       :       Recebe os argumentos enviados pelo usuário e envia
*                               para decodificador
*       Parametros      :       Nenhum
*       Retorno         :       Nenhum
**********************************************************************************"""
if __name__ == '__main__':
    main(str(sys.argv),len(sys.argv))
