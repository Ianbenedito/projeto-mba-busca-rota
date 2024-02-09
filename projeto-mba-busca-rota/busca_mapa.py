#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
df = pd.read_excel('latlongdist.xlsx')
df_logistica = pd.read_excel('tabela_logistica.xlsx')


# In[29]:


class BuscaMapa:
    def __init__(self, df, df_logistica):
        self.tamanho = int(input('quantas cidades o caminhão vai passar? (Somente números): '))
        self.cidade = [None] * self.tamanho
        self.df = df
        self.tabela_logistica = df_logistica
        self.n_elementos = 0
        self.adjacente_calcula = 0
        self.valor_disel = 0
        self.motorista = []
        self.veiculo = []
        self.data_saida = []
        self.peso_carga = 0 #adicionado posteriormente
        self.cubicagem = 0 #adicionado posteriormente
        self.diaria = 0 #adicionado posteriormente
          
    def inicio_objetivo(self):
        df = self.df
        cidade_inicial = input('Qual vai ser a cidade inicial? ')
        objetivo = input('Qual vai ser a cidade final? ')

        self.cidade_inicial = cidade_inicial
        self.objetivo = objetivo
        self.visitado = True
        
    
        #calculo adjacente
        nome_cidade_inicial = df.groupby('Cidade').get_group(cidade_inicial)
        nome_objetivo = df.groupby('Cidade').get_group(objetivo)
        self.lat_obj = np.radians(nome_objetivo['Latitude'].values[0])
        self.lon_obj = np.radians(nome_objetivo['Longitude'].values[0])

        print(f'Você vai começar na cidade: {cidade_inicial}, e vai acabar sua rota na cidade: {objetivo}')
        return  
    
    
    def importa_cidades(self):
        df = self.df
            
        if self.n_elementos == 0:
            self.cidade[0] = self.cidade_inicial
            self.cidade[1] = self.objetivo
            self.n_elementos = 2
            return



        i = 1
        p = 1

        cidade1 = input('Inclua a cidade que o caminhão irá passar: ')

        #if not self.n_elementos == self.tamanho: futuramente bloquear o usuário de colocar a mais do tamanho da fila
        while i < self.n_elementos:
            cidade_escolha = df.groupby('Cidade').get_group(cidade1)
            

                    #cidade menor distância
            distancia_cidade_menor_adjacente = df.groupby('Cidade').get_group(self.cidade[p])
            

                    #cidade maior distância
            distancia_cidade_maior_adjacente = df.groupby('Cidade').get_group(self.cidade[p - 1])
            

                    #adjacente entre maior e menor
            lat1 = np.radians(distancia_cidade_menor_adjacente['Latitude'].values[0])
            lon1 = np.radians(distancia_cidade_menor_adjacente['Longitude'].values[0])
            lat2 = np.radians(distancia_cidade_maior_adjacente['Latitude'].values[0])
            lon2 = np.radians(distancia_cidade_maior_adjacente['Longitude'].values[0])


            a = np.sin((lat2 - lat1) / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2)**2
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
            adjacente = 6371.19 * c #adjacente entre posicção p e p-1


                    #distancia com objetivo ou p-1 com objetivo
            a_obj = np.sin((self.lat_obj - lat2) / 2)**2 + np.cos(lat2) * np.cos(self.lat_obj) * np.sin((self.lon_obj - lon2) / 2)**2
            c_obj = 2 * np.arctan2(np.sqrt(a_obj), np.sqrt(1 - a_obj))
            adjacente_obj = 6371.19 * c_obj

            adjacente_obj_final = adjacente_obj + adjacente


                    #diatancia entre cidade atual e objetivo
            lat_atual = np.radians(cidade_escolha['Latitude'].values[0])
            lon_atual = np.radians(cidade_escolha['Longitude'].values[0])
            a_atual = np.sin((self.lat_obj - lat_atual) / 2)**2 + np.cos(lat_atual) * np.cos(self.lat_obj) * np.sin((self.lon_obj - lon_atual) / 2)**2
            c_atual = 2 * np.arctan2(np.sqrt(a_atual), np.sqrt(1 - a_atual))
            adjacente_cidade_atual_obj = 6371.19 * c_atual 
                    #distancia entre cidade atual e adjacente
            a_obj_atual = np.sin((lat_atual - lat1) / 2)**2 + np.cos(lat1) * np.cos(lat_atual) * np.sin((lon_atual - lon1) / 2)**2
            c_obj_atual = 2 * np.arctan2(np.sqrt(a_obj_atual), np.sqrt(1 - a_obj_atual))
            adjacente_cidade_atual_menor = 6371.19 * c_obj_atual
                    #soma entre duas distancias
            adjacente_cidade_atual = adjacente_cidade_atual_menor + adjacente_cidade_atual_obj


            if adjacente_obj_final > adjacente_cidade_atual:
                p +=1
            i +=1
            #else:
                #print('Você já atingiu o número total de cidades')






        for k in range(self.n_elementos, p - 1, -1):
            self.cidade[k] = self.cidade[k - 1]


        self.cidade[p - 1] = cidade1
        self.n_elementos += 1


        
    def mostra_lista(self):
        print('Essas são as cidades que você deve passar por ordem:')
        for cidades, posicao in zip(self.cidade, range(self.tamanho)):
            print(f'{cidades} - {posicao + 1}°') 
            
            
    def mostra_distancia(self):
        for posicao in range(self.tamanho - 1):
            cidade01 = df.groupby('Cidade').get_group(self.cidade[posicao])
            cidade02 = df.groupby('Cidade').get_group(self.cidade[posicao + 1])
            lat_cidade01 = np.radians(cidade01['Latitude'].values[0])
            lon_cidade01 = np.radians(cidade01['Longitude'].values[0])
            lat_cidade02 = np.radians(cidade02['Latitude'].values[0])
            lon_cidade02 = np.radians(cidade02['Longitude'].values[0])
            a_distancia = np.sin((lat_cidade02 - lat_cidade01) / 2)**2 + np.cos(lat_cidade01) * np.cos(lat_cidade02) * np.sin((lon_cidade02 - lon_cidade01) / 2)**2
            c_distancia = 2 * np.arctan2(np.sqrt(a_distancia), np.sqrt(1 - a_distancia))
            self.adjacente_calcula = 6371.19 * c_distancia
            print(f'de {self.cidade[posicao]} até {self.cidade[posicao + 1]} a distancia é de {round(self.adjacente_calcula, 2)}km')
            self.adjacente_calcula += self.adjacente_calcula
        
    def calcula_km(self):
        print(f'distancia total a ser percorrida é de {round(self.adjacente_calcula, 2)}km') #Considerando que possa haver muitas transportadoras prestadoras de serviço e não somente caminhão da casa, 
                                                                                    #realidade de quase todas as empresas, o km do retorno não é contado.
        
    def cadastro_dados(self):
        motorista = str(input('Qual nome do motorista?'))
        veiculo = str(input('Qual a placa do veículo'))
        data_hora = str(input('informe a data de saída do veiculo, no formato "dia/mês/ano":'))
        data_saida = pd.to_datetime(data_hora, format='%d/%m/%Y')
        self.dias_chegada = round(self.adjacente_calcula, 2) / 500 #500 é a média de km rodado diariamente pelo caminhoneiro
        self.veiculo.append(veiculo)
        self.motorista.append(motorista)
        self.data_saida.append(data_saida)
        
    def dados_tabela(self):
        self.dados = {'Cidades':[self.cidade], 'Pontos de entrega':[len(self.cidade)], 'Veiculo':[self.veiculo], 'Motorista':[self.motorista], 'Km rodado':[self.adjacente_calcula], 'Saída':[self.data_saida],
                   'Previsão de dias para chegada':[self.dias_chegada], 'Peso carga':[self.peso_carga], 'Cubicagem':[self.cubicagem], 'Diaria Motorista':[self.diaria]}
                   

    def importa_dados(self):
        self.tabela = self.df_logistica.append(self.dados, ignore_index=True)
        


# In[30]:


classe = BuscaMapa(df, df_logistica)
classe.inicio_objetivo()


# In[32]:


classe.importa_cidades()


# In[33]:


classe.importa_cidades()


# In[34]:


classe.mostra_lista()
classe.mostra_distancia()


# In[35]:


classe.calcula_km()
classe.cadastro_dados()


# In[36]:


classe.dados_tabela()


# In[37]:


classe.importa_dados()

