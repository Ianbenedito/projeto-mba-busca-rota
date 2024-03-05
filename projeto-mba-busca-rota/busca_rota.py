import pandas as pd
import numpy as np

class BuscaMapa:
    def __init__(self):
        self.tamanho = 0
        self.cidade = [None] * self.tamanho
        self.df = pd.read_excel('latlongdist.xlsx')
        self.tabela_logistica = pd.read_excel('tabela_logistica.xlsx')
        self.n_elementos = 0
        self.adjacente_calcula = 0
        self.motorista = []
        self.veiculo = []
        self.data_saida = []
        self.peso_carga = []
        self.cubicagem = [] 
        self.diaria = [] 
        
    def definir_numero_cidades(self, tamanho):
        self.tamanho = tamanho
        try:
            self.tamanho = int(self.tamanho)
            print(f"Número de cidades definido para: {self.tamanho}")
        except ValueError:
            print("Por favor, insira um valor válido para o número de cidades.")
        self.cidade = [None] * self.tamanho
          
    def inicio_objetivo(self, cidade1, cidade2):
        df = self.df
        cidade_inicial = cidade1
        objetivo = cidade2

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
    
    
    def importa_cidades(self,cidade):
        df = self.df
            
        if self.n_elementos == 0:
            self.cidade[0] = self.cidade_inicial
            self.cidade[1] = self.objetivo
            self.n_elementos = 2
            return



        i = 1
        p = 1

        cidade1 = cidade

        try:# bloquear o usuário de colocar a mais do tamanho da fila
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







            for k in range(self.n_elementos, p - 1, -1):
                self.cidade[k] = self.cidade[k - 1]


            self.cidade[p - 1] = cidade1
            self.n_elementos += 1
        except IndexError:
            print('Você já atingiu o número total de cidades')

        
    def mostra_lista(self):
        print('Essas são as cidades que você deve passar por ordem:')
        for cidades, posicao in zip(self.cidade, range(self.tamanho)):
            print(f'{cidades} - {posicao + 1}°') 
            
            
    def mostra_distancia(self):
        df = self.df
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
        
    def cadastro_dados(self, motorista, veiculo, data_hora, data_saida, cubicagem, peso_carga, diaria,):
        self.motorista = motorista
        self.veiculo = veiculo
        self.data_hora = data_hora
        self.data_saida = data_saida
        self.dias_chegada = round(self.adjacente_calcula, 2) / 500 #500 é a média de km rodado diariamente pelo caminhoneiro lembrando que esse valor deve ser multiplicado por 2 tendo em vista sua volta
        self.cubicagem = cubicagem
        self.peso_carga = peso_carga
        self.diaria = round(self.adjacente_calcula * 100, 2) #50 ticket medio diario de alimentação em sp e mais 50 para o chapa       

    def dados_tabela(self):
        base_dados = {'Cidades':[self.cidade], 'Pontos de entrega':[len(self.cidade)], 'Veiculo':[self.veiculo], 'Motorista':[self.motorista], 'Km rodado':[self.adjacente_calcula], 'Saída':[self.data_saida],
                   'Previsão de dias para chegada (DIAS)':[self.dias_chegada * 2], 'Peso carga':[self.peso_carga], 'Cubicagem':[self.cubicagem], 'Diaria Motorista':[self.diaria]}
        
        self.dados = pd.DataFrame(base_dados)
                   

    def importa_dados(self):
        self.tabela = pd.concat([self.dados, self.tabela_logistica], ignore_index=True)
        self.tabela.to_excel('tabela_logistica.xlsx', index=False)
        
    def mostra_tabela(self):
        from IPython.display import display
        display(self.tabela)
        
    def informacoes_tabela(self):
        display(self.tabela.describe())
        




classe_busca = BuscaMapa()
