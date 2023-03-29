#Importação das bibliotecas numpy,pandas e unidecode para auxiliar nas tarefas do programa.
import numpy
import pandas as pd
import numpy as np
from unidecode import unidecode

#Inicializa leitura do CSV e cria um dataframe, utilizando como delimitador o ";":
df = pd.read_csv('DNIT-Distancias.csv', delimiter=';')

#Cria classe para registrar cadastros como objetos:
class Transporte:

    #Construtor dos objetos da classe:
    def __init__(self,peso_total=0,custo_total = 0,distancia_total=0):
        self.lista_cidades = []
        self.objetos = []
        self.pesos = []
        self.quantidade = []
        self.grande = []
        self.medio = []
        self.pequeno = []
        self.peso_total = peso_total
        self.quantidade_descarga = []
        self.peso_trecho = []
        self.descargas = []
        self.preco_trecho = []
        self.custo_total = custo_total
        self.distancias = []
        self.distancia_total = distancia_total
        self.preco_modalidade_p = []
        self.preco_modalidade_m = []
        self.preco_modalidade_g = []

#Cria lista de objetos para colocar os transportes cadastrados
objs = list()

#Define variáveis de custo:
p_porte = 4.87
m_porte = 11.92
g_porte = 27.44

#Define método para consultar trechos e modalidades:
def trechos_modalidades(partida,destino):

    # Declara Array utilizado para fazer relação entre cidades
    cidades = [1] * 2

    # Declaração de variáveis para analisar se o nome das cidades são válidos
    valido_i = False

    valido_j = False


    # Procura input nas colunas (destino)
    for i in range(len(df.columns)):
        if unidecode(destino.upper()) == df.columns[i]:
            cidades[1] = i
            valido_i = True

    # Procura input nas linhas (partida)
    for j in range(len(df.columns)):
        if unidecode(partida.upper()) == df.columns[j]:
            cidades[0] = j
            valido_j = True

    # Verifica se os nomes das cidades existem no arquivo e são válidos
    if valido_i == True and valido_j == True:

        # Faz a relação entre coluna e linha para achar a distância
        distancia = (df.iloc[cidades[0], cidades[1]])
        return distancia

    else:
        return False

def cadastrar_transportes(cidades,objs):
    # Divide as cidades por vírgula e gera uma lista, tomando cuidado para substituir eventuais espaços com vírgula (, ) por apenas vírgulas
    objs[len(objs) - 1].lista_cidades = cidades.replace(", ", ',').split(',')

    #Cria variáveis para analisar validade das cidades dadas pelo usuário
    valido_i = False
    valido_j = True
    cidades_validas = 0

    # Declara array para colocar as cidades
    rota = [1] * len(objs[len(objs) - 1].lista_cidades)

    ponto_partida = 0
    objs[len(objs)-1].distancias = [1] * len(rota)

    # Para achar o ponto de partida
    for i in range(len(df.columns)):
        if unidecode(objs[len(objs) - 1].lista_cidades[0].upper()) == df.columns[i]:
            ponto_partida = i
            valido_i = True

    #Localiza cidades e faz um array com as rotas (rota[])
    for i in range(len(objs[len(objs) - 1].lista_cidades)):
        for j in range(len(df.columns)):
            if unidecode(objs[len(objs) - 1].lista_cidades[i].upper()) == df.columns[j]:
                rota[i] = j, ponto_partida
                ponto_partida = j
                cidades_validas +=1
                break

    #Analisa validade das cidades dadas pelo usuário
    if cidades_validas < len(objs[len(objs) - 1].lista_cidades):
        valido_j = False

    if valido_j == True and valido_i == True:

        #Registra distâncias em array, com base no array "rota", que registrou as coordenadas do dataframe com as cidades:
        for i in range(len(objs[len(objs) - 1].lista_cidades)):
            objs[len(objs)-1].distancias[i] = df.iloc[rota[i]]

        #Calcula distância total:
        for i in range(len(rota)):
            objs[len(objs)-1].distancia_total = objs[len(objs)-1].distancia_total + df.iloc[rota[i]]

        #Calcula o peso total:
        for i in range(len(objs[len(objs)-1].objetos)):
            objs[len(objs)-1].peso_total = objs[len(objs)-1].peso_total + (objs[len(objs)-1].pesos[i] * objs[len(objs)-1].quantidade[i] )


        #Estabelece o tamanho dos arrays dos atributos do objeto com base no tamanho da lista de cidades dada pelo usuário e pela quantidade de objetos, no caso no array "quantidade_descarga" e "descargas"
        objs[len(objs) - 1].grande = [0] *len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].medio = [0] *len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].pequeno = [0] *len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].peso_trecho = [0] *len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].quantidade_descarga = (objs[len(objs)-1].quantidade).copy()
        objs[len(objs) - 1].descargas = np.array([[0]*len(objs[len(objs)-1].objetos)] * (len(objs[len(objs) - 1].lista_cidades)-1))
        objs[len(objs) - 1].preco_trecho = [0] * len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].preco_modalidade_g = [0] * len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].preco_modalidade_m = [0] * len(objs[len(objs) - 1].lista_cidades)
        objs[len(objs) - 1].preco_modalidade_p = [0] * len(objs[len(objs) - 1].lista_cidades)

        #Laço de repetição para verificar se o usuário quer descarregar cargas em uma parada do trajeto.
        for i in range(len(objs[len(objs) - 1].lista_cidades)-1):
            for j in range(len(objs[len(objs)-1].objetos)):
                if i+1 != (len(objs[len(objs) - 1].lista_cidades)-1):
                    descarga = int(input('Quantas unidades de '+ objs[len(objs)-1].objetos[j]+' você deseja descarregar em '+ objs[len(objs) - 1].lista_cidades[i+1].upper()+'?\n'))
                    objs[len(objs) - 1].descargas[i,j] = descarga
                objs[len(objs) - 1].peso_trecho[i] += (objs[len(objs)-1].quantidade_descarga[j]*objs[len(objs) - 1].pesos[j])
                objs[len(objs) - 1].quantidade_descarga[j] = objs[len(objs) - 1].quantidade_descarga[j] - descarga


            # Declara variável para divisão de pesos por caminhões
            peso_dividido = objs[len(objs) - 1].peso_trecho[i]


            while peso_dividido >0:
                if peso_dividido > 9200: #Peso acima do qual não vale mais a pena usar 2 caminhões médios
                    peso_dividido = peso_dividido - 10000
                    objs[len(objs) - 1].grande[i] += 1
                elif peso_dividido > 2400: #Peso acima do qual não vale mais a pena usar 2 caminhões pequenos
                    peso_dividido = peso_dividido - 4000
                    objs[len(objs) - 1].medio[i] += 1
                else:
                    peso_dividido = peso_dividido - 1000
                    objs[len(objs) - 1].pequeno[i] += 1


            #Calcula preço do trecho:
            objs[len(objs) - 1].preco_trecho[i] =round(((objs[len(objs) - 1].grande[i]*g_porte) +  (objs[len(objs) - 1].medio[i]*m_porte) + (objs[len(objs) - 1].pequeno[i]*p_porte)) * objs[len(objs)-1].distancias[i+1],2)

            #Calcula preço por modalidades de transporte:
            objs[len(objs) - 1].preco_modalidade_g[i] = round((objs[len(objs) - 1].grande[i]*g_porte) * objs[len(objs)-1].distancias[i+1],2)
            objs[len(objs) - 1].preco_modalidade_m[i] = round((objs[len(objs) - 1].medio[i] * m_porte) * objs[len(objs) - 1].distancias[i + 1],2)
            objs[len(objs) - 1].preco_modalidade_p[i] = round((objs[len(objs) - 1].pequeno[i] * p_porte) * objs[len(objs) - 1].distancias[i + 1],2)

        #Laço de repetição para relacionar todos os atributos do objeto colocados nos arrays e exibir as informações necessárias
        for i in range(len(objs[len(objs) - 1].lista_cidades)-1):
            print('\nTRECHO PERCORRIDO:\n',objs[len(objs) - 1].lista_cidades[i].upper(), '-', objs[len(objs) - 1].lista_cidades[i + 1].upper(), ':', objs[len(objs)-1].distancias[i + 1], 'km de distância.')

            if i + 1 <= len(objs[len(objs) - 1].lista_cidades) - 1:
                if i + 1 == len(objs[len(objs) - 1].lista_cidades) - 1:
                    print('\nO restante da carga foi descarregado em', objs[len(objs) - 1].lista_cidades[i + 1])
                else:
                    print('\nEntre', objs[len(objs) - 1].lista_cidades[i], 'e', objs[len(objs) - 1].lista_cidades[i + 1],'foram descarregados:')
                    for j in range(len(objs[len(objs)-1].objetos)):
                        print(objs[len(objs) - 1].descargas[i,j], objs[len(objs)-1].objetos[j])
                print('\nOs tipos de caminhões necessários foram:\nPequenos:',objs[len(objs) - 1].pequeno[i],'\nMédios:',objs[len(objs) - 1].medio[i],'\nGrandes:',objs[len(objs) - 1].grande[i],'\n')
                print('O custo do trecho foi de R$',(objs[len(objs) - 1].preco_trecho[i]))

        #Calcula custo total da viagem e o preço médio unitário e os imprime:
        objs[len(objs) - 1].custo_total = numpy.sum(objs[len(objs) - 1].preco_trecho)
        print('\nO custo total foi de R$',round(objs[len(objs) - 1].custo_total,2))
        print('O custo unitário médio foi de:',round(objs[len(objs) - 1].custo_total/numpy.sum(objs[len(objs) - 1].quantidade),2))

    #Retorno de erro caso o usuário não colocar uma cidade presente no arquivo.
    else:
        return print('\nPor favor, tente novamente e insira cidades válidas\n')

#Define método para exibir estatísticas:
def estatisticas():

    #Verifica se há transportes cadastrados:
    if len(objs) > 0:

        #Cria laço de repetição para analisar todos objetos criados:
        for i in range(len(objs)):

            #Imprime as informações na tela com base nos atributos de cada objeto e com os devidos cálculos necessários.
            print('\nCADASTRO Nº',i+1)

            print('\nCusto total:',round(objs[i].custo_total,2))

            print('\nCusto por trecho:')
            for j in range(len(objs[i].preco_trecho)):
                if j + 1 < len(objs[i].lista_cidades):
                    print(objs[i].lista_cidades[j].upper(),'-',objs[i].lista_cidades[j+1].upper(),': R$:',objs[i].preco_trecho[j])

            print('\nCusto médio por km: R$',round(objs[i].custo_total/objs[i].distancia_total,2))

            print('\nCusto médio por tipo de produto:')
            for j in range(len(objs[i].objetos)):
                print(objs[i].objetos[j], '- R$',round(objs[i].custo_total/objs[i].quantidade[j],2))

            print('\nCusto total por trecho:')
            cidade_anterior = 0
            for j in range(len(objs[i].preco_trecho)):
                if j + 1 < len(objs[i].lista_cidades):
                    print(objs[i].lista_cidades[j].upper(),'-',objs[i].lista_cidades[j+1].upper(),': R$:',objs[i].preco_trecho[j] + cidade_anterior)
                    cidade_anterior = objs[i].preco_trecho[j]

            print('\nCusto total por modalidade de transporte:')
            print('Caminhão de grande porte: R$',np.sum(objs[i].preco_modalidade_g))
            print('Caminhão de médio porte: R$', np.sum(objs[i].preco_modalidade_m))
            print('Caminhão de pequeno porte: R$', np.sum(objs[i].preco_modalidade_p))

            print('\nTotal de veículos deslocados:',np.sum(objs[i].grande)+np.sum(objs[i].medio)+np.sum(objs[i].pequeno))

            print('\nTotal de produtos transportados:',np.sum(objs[i].quantidade))

    #Exibe mensagem notificando o usuário caso não haja transportes cadastrados
    else:
        print('Não há nenhum transporte cadastrado para exibir')

#Define método para exibir menu:
def menu():
    #Cria variável para ser possibilitar ao usuário a navegação entre tarefas.
    while True:
        escolha = int(input('\nO que você deseja fazer?\n\n1 - Consultar trechos e modalidades\n2 - Cadastrar transporte\n3 - Dados estatísticos\n4 - Sair do programa\n'))

        if escolha == 1:
            #Imprime rotas disponíveis:
            print('\nEstes são os trechos disponíveis: ')
            for i in range(len(df.columns)):
                for j in range(len(df.columns)):
                    if df.columns[i] != df.columns[j]:
                        print(df.columns[i],'-',df.columns[j])
            print('\n')

            #Permite que usuário digite local de partida:
            while True:
                try:
                    partida = input('De onde você quer partir? Para sair do programa, digite 0.\n')
                    if partida == 0:
                        print('Saindo do programa.')
                        exit()
                except ValueError:
                    print('Por favor, insira o nome de uma cidade\n')
                    continue
                break

            #Permite que usuário digite o destino:
            while True:
                try:
                    destino = input('\nDigite o destino:\n')
                    if destino == 0:
                        print('Saindo do programa.')
                        exit()
                except ValueError:
                    print('Por favor, insira o nome de uma cidade\n')
                    continue
                break

            #Verifica a validade das cidades dadas pelo usuário:
            if trechos_modalidades(partida, destino) == False:
                print('Por favor, tente novamente, inserindo cidades válidas.\n')
                menu()

            #Permite que o usuário escolha o porte do caminhão através de um input de inteiro:

            while True:
                porte_escolha = int(input('\nQual o porte do caminhão?Pressione 0 para sair do programa.\n1 - Pequeno\n2 - Médio\n3 - Grande\n'))
                if porte_escolha == 1:
                    preco_porte = p_porte
                    porte = 'pequeno porte'
                    break
                elif porte_escolha == 2:
                    preco_porte = m_porte
                    porte = 'médio porte'
                    break
                elif porte_escolha == 3:
                    preco_porte = g_porte
                    porte = 'grande porte'
                    break
                elif porte_escolha == 0:
                    print('Saindo do programa.')
                    exit()
                else:
                    print('Escolha um porte válido')

            #Calcula o preço por porte
            custo = preco_porte * trechos_modalidades(partida,destino)

            #Imprime informações:
            print('\nA distância entre',partida.upper(),'e',destino.upper(),'é de',trechos_modalidades(partida, destino),'km.\nO custo total em um caminhão de',porte,'será de R$', round(custo,2),'\n')

            #Retorna ao menu:
            menu()

        elif escolha == 2:

            #Declara variável de cidades:
            cidades = ''

            while True:
                #Cria objeto na classe Transporte
                objs.append(Transporte())

                #Pede para o usuário digitar a lista de cidades.
                try:
                    cidades = input('\nPara quais cidades você quer ir? Digite-as separadas apenas por vírgulas.Para sair do programa digite 0\n')
                    if cidades == '0':
                        print('\nSaindo do programa')
                        exit()
                except ValueError:
                    print("\nPor favor, insira palavras que representem nomes de cidade separados apenas por vírgulas\n")
                    continue
                break

            while True:
                #Pede para o usuário digitar um objeto que queira adicionar ao transporte
                while True:
                    try:
                        adicionar_obj = input('\nQue objeto quer colocar na lista? Digite um de cada vez. Para sair do programa digite 0.\n')
                        if adicionar_obj == '0':
                            print("\nSaindo do programa.")
                            exit()
                    except ValueError:
                        print('\nPor favor adicine um objeto válido.\n')
                        continue
                    #Coloca objeto no array do atributo "objetos"
                    objs[len(objs) - 1].objetos.append(adicionar_obj)
                    break

                #Pede para o usuário digitar o peso do objeto
                while True:
                    try:
                        adicionar_peso = float(input('\nQual o peso (em quilogramas) do objeto? Para sair do programa digite 0.\n '))
                        if adicionar_peso == 0:
                            print("\nSaindo do programa.")
                            exit()
                    except ValueError:
                        print('\nPor favor, adicione um peso válido.\n')
                        continue
                    #Coloca o peso digitado no array do atributo "pesos"
                    objs[len(objs)-1].pesos.append(adicionar_peso)
                    break

                #Pede para o usuário digitar a quantidade do objeto digitado anteriormente
                while True:
                    try:
                        adicionar_quantidade = float(input('\nQual a quantidade desse objeto? Para sair do programa digite 0\n'))
                        if adicionar_quantidade == 0:
                            print("\nSaindo do programa.")
                            exit()
                    except ValueError:
                        print('\nPor favor, adicione uma quantidade válida.\n')
                        continue
                    #Coloca a quantidade desse objeto no array "quantidade"
                    objs[len(objs)-1].quantidade.append(adicionar_quantidade)
                    break

                #Dá a possibilidade de o usuário escolher se quer continuar adicionando objetos
                continuar = input('\nDeseja adicionar mais objetos? S ou N? Caso desejar sair do programa, qualquer outro valor\n')

                if continuar.lower() == 's':
                    pass

                elif continuar.lower() == 'n':
                    break
                else:
                    print("\nSaindo do programa.")
                    exit()

            #Chama método de cadastrar transportes
            cadastrar_transportes(cidades,objs)

            #Retorna ao menu
            menu()

        elif escolha == 3:
            #Chama método de exibir estatísticas
            estatisticas()

            #Retorna ao menu
            menu()

        elif escolha == 4:
            #Sai do programa
            print("Saindo do programa.")
            exit()

        #Se o usuário digitar um número fora das escolhas propostas, uma mensagem de erro aparece e o menu é exibido novamente.
        else:
            print('\nDigite uma escolha válida\n')

#Chama método do menu para a sua exibição inicial
print('------SEJA BEM-VINDO!------')
menu()