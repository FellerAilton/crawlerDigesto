import requests
import sys
import re

"""***********************************************************************************
*       Descrição       :       Download do código HTML de uma página
*       Parametros      :       url a ser baixada, numero de tentativas caso ocorra 
*                               algum erro (default:2)
*       Retorno         :       (String) código HTML
**********************************************************************************"""
def download(url, num_retries=2, user_agent='wswp', proxies=None):
    print('Downloading:', url)
    headers = {'User-Agent': user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
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
*       Descrição       :       Decodifica argumentos para chamar função correta
*       Parametros      :       Array de Argumentos
*       Retorno         :       Nenhum
**********************************************************************************"""
def main(argv,num_argv):
    if(num_argv <= 1):
        print("crawler.py --print")
    elif '--print' in argv:
        print("printa arquivos na tela")

    url = 'https://www.vultr.com/products/cloud-compute/'
    #url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
    html = download(url)
    result = re.findall(r'section--pricing-tabs(.*?)</section>', html)
    #result =  re.findall(r'<td class="w2p_fw">(.*?)</td>', html)
    print(result)
    print("END")

"""***********************************************************************************
*       Descrição       :       Recebe os argumentos enviados pelo usuário e envia
*                               para decodificador
*       Parametros      :       Nenhum
*       Retorno         :       Nenhum
**********************************************************************************"""
if __name__ == '__main__':
    main(str(sys.argv),len(sys.argv))
