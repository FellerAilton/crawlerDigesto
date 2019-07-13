from lxml.html import fromstring, tostring
import json
import requests
import sys

"""***********************************************************************************
*       Descrição       :       Mostra o progresso do download na tela
*       Parametros      :       Objeto da lib Requests, Nome do arquivo que recebera
*                               os dados para calcular o progresso
*       Retorno         :       Nenhum
**********************************************************************************"""
def download_progress(resp,file_name):
    with open(file_name, "wb") as f:
        total_length = resp.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(resp.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in resp.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

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
        #download_progress(resp,"download.data")
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
        print(print_string+"\n")

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
*       Descrição       :       Crawler da pagina-alvo 1
*       Parametros      :       Habilita escrita no console, Habilita arquivo JSON
*       Retorno         :       Nenhum
**********************************************************************************"""
def crawler_page1(console_print_var = False, json_save_var = False):
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

"""***********************************************************************************
*       Descrição       :       Decodifica argumentos para chamar função correta
*       Parametros      :       Array de Argumentos
*       Retorno         :       Nenhum
**********************************************************************************"""
def main(argv,num_argv):
    enable_print = False
    enable_json  = False

    if(num_argv <= 1):
        print("crawler.py --help | --print | --save_json")
    else:
        if '--print' in argv:
            enable_print = True
        if '--save_json' in argv:
            enable_json = True
            
        if '--help' in argv:
            print("--print\t\t Escreve na tela o resultado obtido pelo crawler\n"+
                  "--save_json\t Salva o resultado obtido pelo crawler em um arquivo json\n"
                  )
        else:
            crawler_page1(enable_print,enable_json)


"""***********************************************************************************
*       Descrição       :       Recebe os argumentos enviados pelo usuário e envia
*                               para decodificador
*       Parametros      :       Nenhum
*       Retorno         :       Nenhum
**********************************************************************************"""
if __name__ == '__main__':
    main(str(sys.argv),len(sys.argv))
