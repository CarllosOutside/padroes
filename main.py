import re
import glob
import timeit
import sys
import lex as lex
from decimal import Decimal

#reserved words
reserved = {
    'price': 'PRICE',

 }

# List of token names.   This is always required
tokens = [
    'DOLAR',
    'URL',
    'MAIL',
    'ADD',
] + list(reserved.values())


# A regular expression rule with some action code --COMENTARIOS DEVEM VIR ANTES DE STRING E CAR
dolar_count=0
dmax = 0
def t_DOLAR(t):
    r'\$[ ]?[0-9]?[0-9]?[0-9](\,[0-9][0-9][0-9])*(\.[0-9][0-9])?'
    global dolar_count
    global dmax
    dolar_count += 1
    t.value = float(t.value.replace('$', '').replace(' ', '').replace(',',''))
    if(t.value>dmax):
        dmax=t.value
    return t

urls = []
urlc=0
def t_URL(t):
    r'((https|http):\/\/)?(www\.)([a-z]+)((\.)?[a-z]+)*(\/[^/ ]+)*'
    global urlc
    global urls
    rx = '((https|http):\/\/)?(www\.)([a-z]+)'
    urls.append(re.findall(rx, t.value))
    urlc += 1
    return t


mailc=0
def t_MAIL(t):
    r'[a-zA-Z0-9.!#$%&*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*'
    global mailc
    mailc += 1
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    pass
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

#Lê o codigo
#filename = sys.argv[1]
#file_handle = open(filename, "r")
#file_contents = file_handle.read()

#Run the Lexer giving it input
#lexer.input(file_contents)
maiorNemails = 0
mailFilename = ""
for file in glob.iglob("maildir"+ '/allen-p/inbox/*', recursive=True):
    try:
        mailc = 0
        file_handle = open(file, 'r')  # abre cada arquivo
        file_contents = file_handle.read()
        lexer.input(file_contents)
        while True:
            tok = lexer.token()
            if not tok:
                if(mailc>maiorNemails):
                    maiorNemails = mailc
                    mailFilename = file
                break  # No more input
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        pass

# Tokenize
#while True:
    #tok = lexer.token()
    #if not tok:
        #break  # No more input
    #print('Token:',tok.type,'\nLexema:',tok.value, '\n')

print("Numero de dolares")
print(dolar_count)
print("Maior valor em dolares")
print(dmax)
print("Numero de url's")
print(urlc)
print("Arquivo com maior quantidade de email's")
print(mailFilename)
end = [add[0] for add in urls]
nomesSite = [nom[3] for nom in end]
#Contagem de url's repetidas
my_dict = {i:nomesSite.count(i) for i in nomesSite}
print("Sistes que mais aparecem")
print(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
# UNICODE
NO_OF_CHARS = 256

# BOYERMOORE - FUNCAO AUXILIAR
def badCharHeuristic(string, size):
    # Initialize all occurrence as -1
    badChar = [-1] * NO_OF_CHARS

    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i;

    # return initialized list
    return badChar


# BOYERMOORE
def searchB(patList, txt):
    n = len(txt)
    patCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # executa para cada padrao
    for k, pat in enumerate(patList):
        m = len(pat)  # tamanho padrao

        badChar = badCharHeuristic(pat, m)  # indices de cada caracter no padrao

        s = 0  # shift inicial
        while (s <= n - m):
            j = m - 1
            # compara padrao ao texto
            while j >= 0 and pat[j] == txt[s + j]:
                j -= 1
            # padrao encontrado
            if j < 0:
                patCount[k] += 1
                s += (m - badChar[ord(txt[
                                          s + m])] if s + m < n else 1)  # realiza shift alinhando ocorrencia da proxima letra do texto com o padrao
            else:  # padrao nao encontrado
                s += max(1, j - badChar[ord(txt[
                                                s + j])])  # realiza shift alinhando o termo errado com a ocorrencia no padrao, ou pulando o termo se nao houver ocorrencia
    return patCount

def searchPriceRegex(texto):
  buffer = [] #Buffer onde caracteres serão armazenados
  priceCount = 0; #Quantidade de "price" encontrados
#Percorre todos caracteres do texto
  for c in texto:
    #So executa no inicio
    if(len(buffer)<5): #Enquanto o buffer tiver menos de 5 caracteres(p r i c e)
      buffer.append(c) #Emenda um caracter do texto
    #Loop sempre iniciara aqui
    elif(len(buffer) == 5 and priceWord.match(''.join(i for i in buffer))): #Ao ter 5 caracteres, verifica se os 5 caracteres unidos foram a palavra price
      priceCount+=1 #Incrementa qtd de prices
      buffer.pop(0)  #retira o primeiro caracter do buffer
      buffer.append(c) #emenda o recem lido
    else: #Se nao der match
      buffer.pop(0)  #retira o primeiro caracter do buffer
      buffer.append(c) #emenda o recem lido
  return priceCount

pat = ["price"] #padrao BoyerMoore para price
priceWord = re.compile('price')#regex p palavra price

#Le todos arquivos do diretorio e subdiretorios de gang
def buscaB():
    countB=0
    for file in glob.iglob("maildir"+ '/allen-p/inbox/*', recursive=True):
        try:
            with open(file, 'r') as f: #abre cada arquivo
                dados = f.read().replace('\n', '')  # retira todas as quebras de linha
                texto = dados.replace(" ", "")  # remove todos os espaços em branco
                countB += searchB(pat, texto)[0]
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            pass
    return countB
def buscaReg():
    count=0
    for file in glob.iglob("maildir"+ '/allen-p/inbox/*', recursive=True):
        try:
            with open(file, 'r') as f: #abre cada arquivo
                dados = f.read().replace('\n', '')  # retira todas as quebras de linha
                texto = dados.replace(" ", "")  # remove todos os espaços em branco
                count += searchPriceRegex(texto)
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            pass
    return count

countB=buscaB()
count=buscaReg()

print("")
print("Quantidades de vezes que a palavra price foi encontrada")
print("BooyerMoo.:", countB)
print("Regex.:", count)

tb=timeit.timeit(buscaB, number=1)
tr=timeit.timeit(buscaReg, number=1)
print("Tempos de execucao:")
print("Boyer Moore:", tb)
print("Regex", tr)
