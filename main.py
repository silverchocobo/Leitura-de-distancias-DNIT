#Programa IT Academy – Processo Seletivo – Edição #18
#Nome do candidato: Pedro Christmann de Quadros
import numpy
import pandas as pd
import numpy as np

#Inicializa leitura do CSV e cria um dataframe, utilizando como delimitador o ";":
df = pd.read_csv('DNIT-Distancias.csv', delimiter=';')

#Define variáveis de custo:
#objetos = []
#pesos = []
#quantidade = []
#porte = ''
preco_porte = 0
p_porte = 4.87
m_porte = 11.92
g_porte = 27.44


#Cria classe para registrar cadastros como objetos:
class Transporte:

    #Construtor dos objetos da classe:
    def __init__(self,peso_total=0,custo_total = 0,distancia_total=0):
        self.lista_cidades = []
        self.objetos = []
        self.pesos = []
        self.quantidade = []
        self.porte = []
        self.grande = []
        self.medio = []
        self.pequeno = []
        self.peso_total = peso_total
        self.quantidade_descarga = []
        self.peso_trecho = []
        self.descargas = []
        self.quantidade_total = []
        self.preco_trecho = []
        self.custo_total = custo_total
        self.distancias = []
        self.distancia_total = 0
        self.preco_modalidade_p = []
        self.preco_modalidade_m = []
        self.preco_modalidade_g = []



    def mostrar(self):
        print('Cidades:',self.cidades)
        print('Objetos:',self.objetos)
        print('Pesos:',self.pesos)
        print('Quantidade:',self.quantidade)
        print('Caminhões de pequeno porte:', self.pequeno)
        print('Caminhões de médio porte:', self.medio)
        print('Caminhões de grande porte:', self.grande)

    def relatorio(self):
        print('Custo total:',round(self.custo_total))



objs = list()

#Define método para consultar trechos e modalidades:
def trechos_modalidades(partida,destino):

    # Declara Array utilizado para fazer relação entre cidades
    cidades = [1] * 2

    # Declaração de variáveis para analisar se o nome das cidades são válidos
    valido_i = False

    valido_j = False


    # Procura input nas colunas (destino)
    for i in range(len(df.columns)):
        if destino.upper() == df.columns[i]:
            cidades[1] = i
            valido_i = True

    # Procura input nas linhas (partida)
    for j in range(len(df.columns)):
        if partida.upper() == df.columns[j]:
            cidades[0] = j
            valido_j = True

    # Verifica se os nomes das cidades são válidos
    if valido_i == True and valido_j == True:

        # Faz a relação entre coluna e linha para achar a distância
        distancia = (df.iloc[cidades[0], cidades[1]])
        return distancia

    else:
        return False

def cadastrar_transportes(cidades,objs):
    # Divide as cidades por vírgula e gera uma lista
    objs[len(objs) - 1].lista_cidades = cidades.split(',')

    #Cria variáveis para analisar validade das cidades dadas pelo usuário
    valido_i = False
    valido_j = True
    cidades_validas = 0

    # Declara array para colocar as cidades
    rota = [1] * len(objs[len(objs) - 1].lista_cidades)

    ponto_partida = 0
    distancia_total = 0
    objs[len(objs)-1].distancias = [1] * len(rota)

    # Para achar o ponto de partida
    for i in range(len(df.columns)):
        if objs[len(objs) - 1].lista_cidades[0].upper() == df.columns[i]:
            ponto_partida = i
            valido_i = True

    #Localiza cidades e faz um array com as rotas (rota[])
    for i in range(len(objs[len(objs) - 1].lista_cidades)):
        for j in range(len(df.columns)):
            if objs[len(objs) - 1].lista_cidades[i].upper() == df.columns[j]:
                rota[i] = j, ponto_partida
                ponto_partida = j
                cidades_validas +=1
                break

    #Analisa validade das cidades dadas pelo usuário
    if cidades_validas < len(objs[len(objs) - 1].lista_cidades):
        valido_j = False

    if valido_j == True and valido_i == True:

        for i in range(len(objs[len(objs) - 1].lista_cidades)):
            objs[len(objs)-1].distancias[i] = df.iloc[rota[i]]

        #Calcula distância total:
        for i in range(len(rota)):
            objs[len(objs)-1].distancia_total = objs[len(objs)-1].distancia_total + df.iloc[rota[i]]

        #Calcula o peso total:
        for i in range(len(objs[len(objs)-1].objetos)):
            objs[len(objs)-1].peso_total = objs[len(objs)-1].peso_total + (objs[len(objs)-1].pesos[i] * objs[len(objs)-1].quantidade[i] )

        #print('\nA distância total é de:',distancia_total,'km')
        #print('\nO peso total é:',objs[len(objs)-1].peso_total,'kg\n')

        #Laço de repetição para imprimir trechos e suas respectivas distâncias
        for i in range(len(objs[len(objs) - 1].lista_cidades)):
            if i + 1 < len(objs[len(objs) - 1].lista_cidades):
                print(objs[len(objs) - 1].lista_cidades[i], '-', objs[len(objs) - 1].lista_cidades[i + 1], ':',objs[len(objs)-1].distancias[i + 1], 'km')

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

        print(objs[len(objs) - 1].descargas)

        for i in range(len(objs[len(objs) - 1].lista_cidades)-1):
            for j in range(len(objs[len(objs)-1].objetos)):
                if i+1 != (len(objs[len(objs) - 1].lista_cidades)-1):
                    descarga = int(input('O quanto de'+ objs[len(objs)-1].objetos[j]+'você deseja descarregar em'+ objs[len(objs) - 1].lista_cidades[i+1]+'?'))
                    objs[len(objs) - 1].descargas[i,j] = descarga
                    #print('Você descarregou',descarga,objs[len(objs)-1].objetos[j],'em',lista_cidades[i+1])
                objs[len(objs) - 1].peso_trecho[i] += (objs[len(objs)-1].quantidade_descarga[j]*objs[len(objs) - 1].pesos[j])
                objs[len(objs) - 1].quantidade_descarga[j] = objs[len(objs) - 1].quantidade_descarga[j] - descarga


                # Declara variável para divisão de pesos por caminhões
            peso_dividido = 0

            while peso_dividido < objs[len(objs) - 1].peso_trecho[i]:
                if peso_dividido + 10000 <= objs[len(objs) - 1].peso_trecho[i]:
                    objs[len(objs) - 1].grande[i] += 1
                    peso_dividido += 10000
                elif peso_dividido + 4000 <= objs[len(objs) - 1].peso_trecho[i]:
                    objs[len(objs) - 1].medio[i] += 1
                    peso_dividido += 4000
                elif peso_dividido + 1000 <= objs[len(objs) - 1].peso_trecho[i]:
                    objs[len(objs) - 1].pequeno[i] += 1
                    peso_dividido += 1000
                elif objs[len(objs) - 1].peso_trecho[i] - peso_dividido < 1000:
                    objs[len(objs) - 1].pequeno[i] += 1
                    break
                else:
                    break

            #Calcula preço do trecho:
            objs[len(objs) - 1].preco_trecho[i] =round(((objs[len(objs) - 1].grande[i]*g_porte) +  (objs[len(objs) - 1].medio[i]*m_porte) + (objs[len(objs) - 1].pequeno[i]*p_porte)) * objs[len(objs)-1].distancias[i+1],2)

            #Calcula preço por modalidades de transporte:
            objs[len(objs) - 1].preco_modalidade_g[i] = round((objs[len(objs) - 1].grande[i]*g_porte) * objs[len(objs)-1].distancias[i+1],2)
            objs[len(objs) - 1].preco_modalidade_m[i] = round((objs[len(objs) - 1].medio[i] * m_porte) * objs[len(objs) - 1].distancias[i + 1],2)
            objs[len(objs) - 1].preco_modalidade_p[i] = round((objs[len(objs) - 1].pequeno[i] * p_porte) * objs[len(objs) - 1].distancias[i + 1],2)


        for i in range(len(objs[len(objs) - 1].lista_cidades)-1):
            print('\nTrecho percorrido:\n',objs[len(objs) - 1].lista_cidades[i].upper(), '-', objs[len(objs) - 1].lista_cidades[i + 1].upper(), ':', objs[len(objs)-1].distancias[i + 1], 'km de distância.')
            if i + 1 <= len(objs[len(objs) - 1].lista_cidades) - 1:
                for j in range(len(objs[len(objs)-1].objetos)):
                    if i + 1 == len(objs[len(objs) - 1].lista_cidades) - 1:
                        print('\nO restante da carga foi descarregado em',objs[len(objs) - 1].lista_cidades[i+1])
                        break
                    else:
                        print('Entre', objs[len(objs) - 1].lista_cidades[i],'e',objs[len(objs) - 1].lista_cidades[i+1],'foram descarregados',objs[len(objs) - 1].descargas[i,j], objs[len(objs)-1].objetos[j],'.' )
                print('\nOs tipos de caminhões necessários foram:\nPequenos:',objs[len(objs) - 1].pequeno[i],'\nMédios:',objs[len(objs) - 1].medio[i],'\nGrandes:',objs[len(objs) - 1].grande[i],'\n')
                print('O custo do trecho foi de R$',(objs[len(objs) - 1].preco_trecho[i]))

        #Calcula custo total da viagem e o preço médio unitário e os imprime:
        objs[len(objs) - 1].custo_total = numpy.sum(objs[len(objs) - 1].preco_trecho)
        print('\nO custo total foi de R$',round(objs[len(objs) - 1].custo_total),2)
        print('O custo unitário médio foi de:',round(objs[len(objs) - 1].custo_total/numpy.sum(objs[len(objs) - 1].quantidade)),2)





    else:
        return print('\nInsira cidades válidas\n')


def estatisticas():
    for i in range(len(objs)):
        print('CADASTRO Nº',i)

        print('\nCusto total:',round(objs[i].custo_total),2)

        print('Custo por trecho:')
        for j in range(len(objs[i].preco_trecho)):
            if j + 1 < len(objs[i].lista_cidades):
                print(objs[i].lista_cidades[j].upper(),'-',objs[i].lista_cidades[j+1].upper(),': R$:',objs[i].preco_trecho[j])

        print('Custo médio por km: R$',round(objs[i].custo_total/objs[i].distancia_total))

        print('Custo médio por tipo de produto:')
        for j in range(len(objs[i].objetos)):
            print(objs[i].objetos[j], '- R$',round(objs[i].custo_total/objs[i].quantidade[j],2))

        print('Custo total por trecho:')
        cidade_anterior = 0
        for j in range(len(objs[i].preco_trecho)):
            if j + 1 < len(objs[i].lista_cidades):
                print(objs[i].lista_cidades[j].upper(),'-',objs[i].lista_cidades[j+1].upper(),': R$:',objs[i].preco_trecho[j] + cidade_anterior)
                cidade_anterior = objs[i].preco_trecho[j]

        print('Custo total por modalidade de transporte:')
        print('Caminhão de grande porte: R$',np.sum(objs[i].preco_modalidade_g))
        print('Caminhão de médio porte: R$', np.sum(objs[i].preco_modalidade_m))
        print('Caminhão de pequeno porte: R$', np.sum(objs[i].preco_modalidade_p))

        print('Total de veículos deslocados:',np.sum(objs[i].grande)+np.sum(objs[i].medio)+np.sum(objs[i].pequeno))

        print('Total de produtos transportados:',np.sum(objs[i].quantidade))






def menu():
    escolha = int(input('O que você deseja fazer?\n1 - Consultar trechos e modalidades\n2 - Cadastrar transporte\n3 - Dados estatísticos\n4 - Sair do programa\n'))

    if escolha == 1:
        #Imprime rotas disponíveis:
        print('Estes são os trechos disponíveis: ')
        for i in range(len(df.columns)):
            for j in range(len(df.columns)):
                if df.columns[i] != df.columns[j]:
                    print(df.columns[i],'-',df.columns[j])
        print('\n')

        #Permite que usuário digite local de partida:
        while True:
            try:
                partida = input('De onde você quer partir?\n')
            except ValueError:
                print('Por favor, insira o nome de uma cidade\n')
                continue
            break

        #Permite que usuário digite o destino:
        while True:
            try:
                destino = input('Digite o destino:\n')
            except ValueError:
                print('Por favor, insira o nome de uma cidade\n')
                continue
            break

        #Verifica a validade das cidades dadas pelo usuário:
        if trechos_modalidades(partida, destino) == False:
              print('Insira cidades válidas\n')
              menu()

        #Permite que o usuário escolha o porte do caminhão através de um input de inteiro:
        porte_escolha = int(input('Qual o porte do caminhão?\n1 - Pequeno\n2 - Médio\n3 - Grande\n'))

        if porte_escolha == 1:
            preço_porte = p_porte
            porte = 'pequeno porte'
        elif porte_escolha == 2:
            preço_porte = m_porte
            porte = 'médio porte'
        elif porte_escolha == 3:
            preço_porte = g_porte
            porte = 'grande porte'
        else:
            print('Escolha um porte válido')

        #Calcula o preço por porte
        custo = preço_porte * trechos_modalidades(partida,destino)

        #Imprime informações:
        print('A distância entre',partida.upper(),'e',destino.upper(),'é de',trechos_modalidades(partida, destino),'km.\nO custo total em um caminhão de',porte,'será de R$', round(custo,2),'\n')

        #Retorna ao menu:
        menu()

    elif escolha == 2:

        #Declara variável de cidades:
        cidades = ''

        while True:

            objs.append(Transporte())

            try:
                cidades = input('Para quais cidades você quer ir? Digite-as separadas apenas por vírgulas\n')
            except ValueError:
                print("\nPor favor, insira palavras que representem nomes de cidade separadas apenas por vírgulas\n")
                continue
            objs[len(objs)-1].lista_cidades.append(cidades)
            break

        while True:
            try:
                adicionar_obj = input('Que objeto quer colocar na lista?\n')
                objs[len(objs)-1].objetos.append(adicionar_obj)
            except ValueError:
                print('Por favor adicine um objeto válido.\n')
                continue


            try:
                adicionar_peso = float(input('Qual o peso (em quilogramas) do objeto? '))
            except ValueError:
                print('Por favor, adicione um peso válido.\n')
                continue
            objs[len(objs)-1].pesos.append(adicionar_peso)

            try:
                adicionar_quantidade = float(input('Qual a quantidade desse objeto? '))
            except ValueError:
                print('Por favor, adicione uma quantidade válida.\n')
                continue
            objs[len(objs)-1].quantidade.append(adicionar_quantidade)

            continuar = input('Deseja adicionar mais objetos? S ou N?')

            if continuar.lower() == 's':
                pass

            elif continuar.lower() == 'n':
                break


        cadastrar_transportes(cidades,objs)
        menu()

    elif escolha == 3:
        estatisticas()
        menu()




menu()