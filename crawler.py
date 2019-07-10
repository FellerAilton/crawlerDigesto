import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import sys

"""***********************************************************************************
*       Descrição       :       Download do código HTML de uma página
*       Parametros      :       url a ser baixada, numero de tentativas caso ocorra 
*                               algum erro (default:2)
*       Retorno         :       (String) código HTML
**********************************************************************************"""
def download(url, user_agent='wswp', num_retries=2):
    print('Fazendo download:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Erro:', e.reason)
        html = None
        if num_retries > 0:
            #erro no servidor, tenta novamente recursivamente
            if hasattr(e,'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1)
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

"""***********************************************************************************
*       Descrição       :       Recebe os argumentos enviados pelo usuário e envia
*                               para decodificador
*       Parametros      :       Nenhum
*       Retorno         :       Nenhum
**********************************************************************************"""
if __name__ == '__main__':
    main(str(sys.argv),len(sys.argv))
