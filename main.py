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
cadastro = list()

#Define constantes de custo:
P_PORTE = 4.87
M_PORTE = 11.92
G_PORTE = 27.44

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

def cadastrar_transportes(cidades,cadastro):
    # Divide as cidades por vírgula e gera uma lista, tomando cuidado para substituir eventuais espaços com vírgula (, ) por apenas vírgulas
    cadastro[len(cadastro) - 1].lista_cidades = cidades.replace(", ", ',').split(',')

    #Cria variáveis para analisar validade das cidades dadas pelo usuário
    valido_i = False
    valido_j = True
    cidades_validas = 0

    # Declara array para colocar as cidades
    rota = [1] * len(cadastro[len(cadastro) - 1].lista_cidades)

    ponto_partida = 0
    cadastro[len(cadastro)-1].distancias = [1] * len(rota)

    # Para achar o ponto de partida
    for i in range(len(df.columns)):
        if unidecode(cadastro[len(cadastro) - 1].lista_cidades[0].upper()) == df.columns[i]:
            ponto_partida = i
            valido_i = True

    #Localiza cidades e faz um array com as rotas (rota[])
    for i in range(len(cadastro[len(cadastro) - 1].lista_cidades)):
        for j in range(len(df.columns)):
            if unidecode(cadastro[len(cadastro) - 1].lista_cidades[i].upper()) == df.columns[j]:
                rota[i] = j, ponto_partida
                ponto_partida = j
                cidades_validas +=1
                break

    #Analisa validade das cidades dadas pelo usuário
    if cidades_validas < len(cadastro[len(cadastro) - 1].lista_cidades):
        valido_j = False

    if valido_j == True and valido_i == True:

        #Registra distâncias em array, com base no array "rota", que registrou as coordenadas do dataframe com as cidades:
        for i in range(len(cadastro[len(cadastro) - 1].lista_cidades)):
            cadastro[len(cadastro)-1].distancias[i] = df.iloc[rota[i]]

        #Calcula distância total:
        for i in range(len(rota)):
            cadastro[len(cadastro)-1].distancia_total = cadastro[len(cadastro)-1].distancia_total + df.iloc[rota[i]]

        #Calcula o peso total:
        for i in range(len(cadastro[len(cadastro)-1].objetos)):
            cadastro[len(cadastro)-1].peso_total = cadastro[len(cadastro)-1].peso_total + (cadastro[len(cadastro)-1].pesos[i] * cadastro[len(cadastro)-1].quantidade[i] )


        #Estabelece o tamanho dos arrays dos atributos do objeto com base no tamanho da lista de cidades dada pelo usuário e pela quantidade de objetos, no caso no array "quantidade_descarga" e "descargas"
        cadastro[len(cadastro) - 1].grande = [0] *len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].medio = [0] *len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].pequeno = [0] *len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].peso_trecho = [0] *len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].quantidade_descarga = (cadastro[len(cadastro)-1].quantidade).copy()
        cadastro[len(cadastro) - 1].descargas = np.array([[0]*len(cadastro[len(cadastro)-1].objetos)] * (len(cadastro[len(cadastro) - 1].lista_cidades)-1))
        cadastro[len(cadastro) - 1].preco_trecho = [0] * len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].preco_modalidade_g = [0] * len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].preco_modalidade_m = [0] * len(cadastro[len(cadastro) - 1].lista_cidades)
        cadastro[len(cadastro) - 1].preco_modalidade_p = [0] * len(cadastro[len(cadastro) - 1].lista_cidades)

        #Declara variável para registrar produtos descarregados pelo usuário
        descarga = 0

        #Laço de repetição para verificar se o usuário quer descarregar cargas em uma parada do trajeto.
        for i in range(len(cadastro[len(cadastro) - 1].lista_cidades)-1):
            for j in range(len(cadastro[len(cadastro)-1].objetos)):
                if i+1 != (len(cadastro[len(cadastro) - 1].lista_cidades)-1):
                    descarga = int(input('Quantas unidades de '+ cadastro[len(cadastro)-1].objetos[j]+' você deseja descarregar em '+ cadastro[len(cadastro) - 1].lista_cidades[i+1].upper()+'?\n'))
                    cadastro[len(cadastro) - 1].descargas[i,j] = descarga
                cadastro[len(cadastro) - 1].peso_trecho[i] += (cadastro[len(cadastro)-1].quantidade_descarga[j]*cadastro[len(cadastro) - 1].pesos[j])
                cadastro[len(cadastro) - 1].quantidade_descarga[j] = cadastro[len(cadastro) - 1].quantidade_descarga[j] - descarga


            # Declara variável para divisão de pesos por caminhões
            peso_dividido = cadastro[len(cadastro) - 1].peso_trecho[i]


            while peso_dividido >0:
                if peso_dividido > 9200: #Peso acima do qual não vale mais a pena usar 2 caminhões médios
                    peso_dividido = peso_dividido - 10000
                    cadastro[len(cadastro) - 1].grande[i] += 1
                elif peso_dividido > 2400: #Peso acima do qual não vale mais a pena usar 2 caminhões pequenos
                    peso_dividido = peso_dividido - 4000
                    cadastro[len(cadastro) - 1].medio[i] += 1
                else:
                    peso_dividido = peso_dividido - 1000
                    cadastro[len(cadastro) - 1].pequeno[i] += 1


            #Calcula preço do trecho:
            cadastro[len(cadastro) - 1].preco_trecho[i] =round(((cadastro[len(cadastro) - 1].grande[i]*G_PORTE) +  (cadastro[len(cadastro) - 1].medio[i]*M_PORTE) + (cadastro[len(cadastro) - 1].pequeno[i]*P_PORTE)) * cadastro[len(cadastro)-1].distancias[i+1],2)

            #Calcula preço por modalidades de transporte:
            cadastro[len(cadastro) - 1].preco_modalidade_g[i] = round((cadastro[len(cadastro) - 1].grande[i]*G_PORTE) * cadastro[len(cadastro)-1].distancias[i+1],2)
            cadastro[len(cadastro) - 1].preco_modalidade_m[i] = round((cadastro[len(cadastro) - 1].medio[i] * M_PORTE) * cadastro[len(cadastro) - 1].distancias[i + 1],2)
            cadastro[len(cadastro) - 1].preco_modalidade_p[i] = round((cadastro[len(cadastro) - 1].pequeno[i] * P_PORTE) * cadastro[len(cadastro) - 1].distancias[i + 1],2)

        #Laço de repetição para relacionar todos os atributos do objeto colocados nos arrays e exibir as informações necessárias
        for i in range(len(cadastro[len(cadastro) - 1].lista_cidades)-1):
            print('\nTRECHO PERCORRIDO:\n',cadastro[len(cadastro) - 1].lista_cidades[i].upper(), '-', cadastro[len(cadastro) - 1].lista_cidades[i + 1].upper(), ':', cadastro[len(cadastro)-1].distancias[i + 1], 'km de distância.')

            if i + 1 <= len(cadastro[len(cadastro) - 1].lista_cidades) - 1:
                if i + 1 == len(cadastro[len(cadastro) - 1].lista_cidades) - 1:
                    print('\nO restante da carga foi descarregado em', cadastro[len(cadastro) - 1].lista_cidades[i + 1])
                else:
                    print('\nEntre', cadastro[len(cadastro) - 1].lista_cidades[i], 'e', cadastro[len(cadastro) - 1].lista_cidades[i + 1],'foram descarregados:')
                    for j in range(len(cadastro[len(cadastro)-1].objetos)):
                        print(cadastro[len(cadastro) - 1].descargas[i,j], cadastro[len(cadastro)-1].objetos[j])
                print('\nOs tipos de caminhões necessários foram:\nPequenos:',cadastro[len(cadastro) - 1].pequeno[i],'\nMédios:',cadastro[len(cadastro) - 1].medio[i],'\nGrandes:',cadastro[len(cadastro) - 1].grande[i],'\n')
                print('O custo do trecho foi de R$',(cadastro[len(cadastro) - 1].preco_trecho[i]))

        #Calcula custo total da viagem e o preço médio unitário e os imprime:
        cadastro[len(cadastro) - 1].custo_total = numpy.sum(cadastro[len(cadastro) - 1].preco_trecho)
        print('\nO custo total foi de R$',round(cadastro[len(cadastro) - 1].custo_total,2))
        print('O custo unitário médio foi de:',round(cadastro[len(cadastro) - 1].custo_total/numpy.sum(cadastro[len(cadastro) - 1].quantidade),2))

    #Retorno de erro caso o usuário não colocar uma cidade presente no arquivo.
    else:
        #Remove objeto em caso de falha
        cadastro.remove(cadastro[len(cadastro) - 1])
        return print('\nPor favor, tente novamente e insira cidades válidas\n')


#Define método para exibir estatísticas:
def estatisticas():

    #Verifica se há transportes cadastrados:
    if len(cadastro) > 0:

        #Cria laço de repetição para analisar todos objetos criados:
        for i in range(len(cadastro)):

            #Imprime as informações na tela com base nos atributos de cada objeto e com os devidos cálculos necessários.
            print('\nCADASTRO Nº',i+1)

            print('\nCusto total:',round(cadastro[i].custo_total,2))

            print('\nCusto por trecho:')
            for j in range(len(cadastro[i].preco_trecho)):
                if j + 1 < len(cadastro[i].lista_cidades):
                    print(cadastro[i].lista_cidades[j].upper(),'-',cadastro[i].lista_cidades[j+1].upper(),': R$:',cadastro[i].preco_trecho[j])

            print('\nCusto médio por km: R$',round(cadastro[i].custo_total/cadastro[i].distancia_total,2))

            print('\nCusto médio por tipo de produto:')
            for j in range(len(cadastro[i].objetos)):
                print(cadastro[i].objetos[j], '- R$',round(cadastro[i].custo_total/cadastro[i].quantidade[j],2))

            print('\nCusto total por trecho:')
            cidade_anterior = 0
            for j in range(len(cadastro[i].preco_trecho)):
                if j + 1 < len(cadastro[i].lista_cidades):
                    print(cadastro[i].lista_cidades[j].upper(),'-',cadastro[i].lista_cidades[j+1].upper(),': R$:',cadastro[i].preco_trecho[j] + cidade_anterior)
                    cidade_anterior = cadastro[i].preco_trecho[j]

            print('\nCusto total por modalidade de transporte:')
            print('Caminhão de grande porte: R$',np.sum(cadastro[i].preco_modalidade_g))
            print('Caminhão de médio porte: R$', np.sum(cadastro[i].preco_modalidade_m))
            print('Caminhão de pequeno porte: R$', np.sum(cadastro[i].preco_modalidade_p))

            print('\nTotal de veículos deslocados:',np.sum(cadastro[i].grande)+np.sum(cadastro[i].medio)+np.sum(cadastro[i].pequeno))

            print('\nTotal de produtos transportados:',np.sum(cadastro[i].quantidade))

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
                    preco_porte = P_PORTE
                    porte = 'pequeno porte'
                    break
                elif porte_escolha == 2:
                    preco_porte = M_PORTE
                    porte = 'médio porte'
                    break
                elif porte_escolha == 3:
                    preco_porte = G_PORTE
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
                cadastro.append(Transporte())

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
                    cadastro[len(cadastro) - 1].objetos.append(adicionar_obj)
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
                    cadastro[len(cadastro)-1].pesos.append(adicionar_peso)
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
                    cadastro[len(cadastro)-1].quantidade.append(adicionar_quantidade)
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
            cadastrar_transportes(cidades,cadastro)

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