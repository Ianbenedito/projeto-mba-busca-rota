{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 139,
   "id": "f0535210",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "#df = pd.read_excel('latlongdist.xlsx')\n",
    "#df_logistica = pd.read_excel('tabela_logistica.xlsx')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 153,
   "id": "23eeace6",
   "metadata": {},
   "outputs": [],
   "source": [
    "class BuscaMapa:\n",
    "    def __init__(self):\n",
    "        self.tamanho = 0\n",
    "        self.cidade = [None] * self.tamanho\n",
    "        self.df = pd.read_excel('latlongdist.xlsx')\n",
    "        self.tabela_logistica = pd.read_excel('tabela_logistica.xlsx')\n",
    "        self.n_elementos = 0\n",
    "        self.adjacente_calcula = 0\n",
    "        self.motorista = []\n",
    "        self.veiculo = []\n",
    "        self.data_saida = []\n",
    "        self.peso_carga = []\n",
    "        self.cubicagem = [] \n",
    "        self.diaria = [] \n",
    "        \n",
    "    def definir_numero_cidades(self):\n",
    "        self.tamanho = input('Quantas cidades o caminhão irá passar? ')\n",
    "        try:\n",
    "            self.tamanho = int(self.tamanho)\n",
    "            print(f\"Número de cidades definido para: {self.tamanho}\")\n",
    "        except ValueError:\n",
    "            print(\"Por favor, insira um valor válido para o número de cidades.\")\n",
    "        self.cidade = [None] * self.tamanho\n",
    "          \n",
    "    def inicio_objetivo(self):\n",
    "        df = self.df\n",
    "        cidade_inicial = input('Qual vai ser a cidade inicial? ')\n",
    "        objetivo = input('Qual vai ser a cidade final? ')\n",
    "\n",
    "        self.cidade_inicial = cidade_inicial\n",
    "        self.objetivo = objetivo\n",
    "        self.visitado = True\n",
    "        \n",
    "    \n",
    "        #calculo adjacente\n",
    "        nome_cidade_inicial = df.groupby('Cidade').get_group(cidade_inicial)\n",
    "        nome_objetivo = df.groupby('Cidade').get_group(objetivo)\n",
    "        self.lat_obj = np.radians(nome_objetivo['Latitude'].values[0])\n",
    "        self.lon_obj = np.radians(nome_objetivo['Longitude'].values[0])\n",
    "\n",
    "        print(f'Você vai começar na cidade: {cidade_inicial}, e vai acabar sua rota na cidade: {objetivo}')\n",
    "        return  \n",
    "    \n",
    "    \n",
    "    def importa_cidades(self):\n",
    "        df = self.df\n",
    "            \n",
    "        if self.n_elementos == 0:\n",
    "            self.cidade[0] = self.cidade_inicial\n",
    "            self.cidade[1] = self.objetivo\n",
    "            self.n_elementos = 2\n",
    "            return\n",
    "\n",
    "\n",
    "\n",
    "        i = 1\n",
    "        p = 1\n",
    "\n",
    "        cidade1 = input('Inclua a cidade que o caminhão irá passar: ')\n",
    "\n",
    "        try:# bloquear o usuário de colocar a mais do tamanho da fila\n",
    "            while i < self.n_elementos:\n",
    "                cidade_escolha = df.groupby('Cidade').get_group(cidade1)\n",
    "\n",
    "\n",
    "                        #cidade menor distância\n",
    "                distancia_cidade_menor_adjacente = df.groupby('Cidade').get_group(self.cidade[p])\n",
    "\n",
    "\n",
    "                        #cidade maior distância\n",
    "                distancia_cidade_maior_adjacente = df.groupby('Cidade').get_group(self.cidade[p - 1])\n",
    "\n",
    "\n",
    "                        #adjacente entre maior e menor\n",
    "                lat1 = np.radians(distancia_cidade_menor_adjacente['Latitude'].values[0])\n",
    "                lon1 = np.radians(distancia_cidade_menor_adjacente['Longitude'].values[0])\n",
    "                lat2 = np.radians(distancia_cidade_maior_adjacente['Latitude'].values[0])\n",
    "                lon2 = np.radians(distancia_cidade_maior_adjacente['Longitude'].values[0])\n",
    "\n",
    "\n",
    "                a = np.sin((lat2 - lat1) / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2)**2\n",
    "                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))\n",
    "                adjacente = 6371.19 * c #adjacente entre posicção p e p-1\n",
    "\n",
    "\n",
    "                        #distancia com objetivo ou p-1 com objetivo\n",
    "                a_obj = np.sin((self.lat_obj - lat2) / 2)**2 + np.cos(lat2) * np.cos(self.lat_obj) * np.sin((self.lon_obj - lon2) / 2)**2\n",
    "                c_obj = 2 * np.arctan2(np.sqrt(a_obj), np.sqrt(1 - a_obj))\n",
    "                adjacente_obj = 6371.19 * c_obj\n",
    "\n",
    "                adjacente_obj_final = adjacente_obj + adjacente\n",
    "\n",
    "\n",
    "                        #diatancia entre cidade atual e objetivo\n",
    "                lat_atual = np.radians(cidade_escolha['Latitude'].values[0])\n",
    "                lon_atual = np.radians(cidade_escolha['Longitude'].values[0])\n",
    "                a_atual = np.sin((self.lat_obj - lat_atual) / 2)**2 + np.cos(lat_atual) * np.cos(self.lat_obj) * np.sin((self.lon_obj - lon_atual) / 2)**2\n",
    "                c_atual = 2 * np.arctan2(np.sqrt(a_atual), np.sqrt(1 - a_atual))\n",
    "                adjacente_cidade_atual_obj = 6371.19 * c_atual \n",
    "                        #distancia entre cidade atual e adjacente\n",
    "                a_obj_atual = np.sin((lat_atual - lat1) / 2)**2 + np.cos(lat1) * np.cos(lat_atual) * np.sin((lon_atual - lon1) / 2)**2\n",
    "                c_obj_atual = 2 * np.arctan2(np.sqrt(a_obj_atual), np.sqrt(1 - a_obj_atual))\n",
    "                adjacente_cidade_atual_menor = 6371.19 * c_obj_atual\n",
    "                        #soma entre duas distancias\n",
    "                adjacente_cidade_atual = adjacente_cidade_atual_menor + adjacente_cidade_atual_obj\n",
    "\n",
    "\n",
    "                if adjacente_obj_final > adjacente_cidade_atual:\n",
    "                    p +=1\n",
    "                i +=1\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "            for k in range(self.n_elementos, p - 1, -1):\n",
    "                self.cidade[k] = self.cidade[k - 1]\n",
    "\n",
    "\n",
    "            self.cidade[p - 1] = cidade1\n",
    "            self.n_elementos += 1\n",
    "        except IndexError:\n",
    "            print('Você já atingiu o número total de cidades')\n",
    "\n",
    "        \n",
    "    def mostra_lista(self):\n",
    "        print('Essas são as cidades que você deve passar por ordem:')\n",
    "        for cidades, posicao in zip(self.cidade, range(self.tamanho)):\n",
    "            print(f'{cidades} - {posicao + 1}°') \n",
    "            \n",
    "            \n",
    "    def mostra_distancia(self):\n",
    "        df = self.df\n",
    "        for posicao in range(self.tamanho - 1):\n",
    "            cidade01 = df.groupby('Cidade').get_group(self.cidade[posicao])\n",
    "            cidade02 = df.groupby('Cidade').get_group(self.cidade[posicao + 1])\n",
    "            lat_cidade01 = np.radians(cidade01['Latitude'].values[0])\n",
    "            lon_cidade01 = np.radians(cidade01['Longitude'].values[0])\n",
    "            lat_cidade02 = np.radians(cidade02['Latitude'].values[0])\n",
    "            lon_cidade02 = np.radians(cidade02['Longitude'].values[0])\n",
    "            a_distancia = np.sin((lat_cidade02 - lat_cidade01) / 2)**2 + np.cos(lat_cidade01) * np.cos(lat_cidade02) * np.sin((lon_cidade02 - lon_cidade01) / 2)**2\n",
    "            c_distancia = 2 * np.arctan2(np.sqrt(a_distancia), np.sqrt(1 - a_distancia))\n",
    "            self.adjacente_calcula = 6371.19 * c_distancia\n",
    "            print(f'de {self.cidade[posicao]} até {self.cidade[posicao + 1]} a distancia é de {round(self.adjacente_calcula, 2)}km')\n",
    "            self.adjacente_calcula += self.adjacente_calcula\n",
    "        \n",
    "    def calcula_km(self):\n",
    "        print(f'distancia total a ser percorrida é de {round(self.adjacente_calcula, 2)}km') #Considerando que possa haver muitas transportadoras prestadoras de serviço e não somente caminhão da casa, \n",
    "                                                                                    #realidade de quase todas as empresas, o km do retorno não é contado.\n",
    "        \n",
    "    def cadastro_dados(self):\n",
    "        motorista = str(input('Qual nome do motorista?'))\n",
    "        veiculo = str(input('Qual a placa do veículo'))\n",
    "        data_hora = str(input('informe a data de saída do veiculo, no formato \"dia/mês/ano\":'))\n",
    "        data_saida = pd.to_datetime(data_hora, format='%d/%m/%Y')\n",
    "        self.dias_chegada = round(self.adjacente_calcula, 2) / 500 #500 é a média de km rodado diariamente pelo caminhoneiro lembrando que esse valor deve ser multiplicado por 2 tendo em vista sua volta\n",
    "        cubicagem = int(input('Quantos m³ deu a carga? :'))\n",
    "        peso_carga = int(input('Quantas toneladas deu a carga? :'))\n",
    "        self.diaria = round(self.adjacente_calcula * 100, 2) #50 ticket medio diario de alimentação em sp e mais 50 para o chapa       \n",
    "        self.cubicagem.append(cubicagem)\n",
    "        self.peso_carga.append(peso_carga)\n",
    "        self.veiculo.append(veiculo)\n",
    "        self.motorista.append(motorista)\n",
    "        self.data_saida.append(data_saida)\n",
    "        \n",
    "    def dados_tabela(self):\n",
    "        base_dados = {'Cidades':[self.cidade], 'Pontos de entrega':[len(self.cidade)], 'Veiculo':[self.veiculo], 'Motorista':[self.motorista], 'Km rodado':[self.adjacente_calcula], 'Saída':[self.data_saida],\n",
    "                   'Previsão de dias para chegada (DIAS)':[self.dias_chegada * 2], 'Peso carga':[self.peso_carga], 'Cubicagem':[self.cubicagem], 'Diaria Motorista':[self.diaria]}\n",
    "        \n",
    "        self.dados = pd.DataFrame(base_dados)\n",
    "                   \n",
    "\n",
    "    def importa_dados(self):\n",
    "        self.tabela = pd.concat([self.dados, self.tabela_logistica], ignore_index=True)\n",
    "        self.tabela.to_excel('tabela_logistica.xlsx', index=False)\n",
    "        \n",
    "    def mostra_tabela(self):\n",
    "        from IPython.display import display\n",
    "        display(self.tabela)\n",
    "        \n",
    "    def informacoes_tabela(self):\n",
    "        display(self.tabela.describe())\n",
    "        "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 154,
   "id": "998cb88e",
   "metadata": {},
   "outputs": [],
   "source": [
    "classe = BuscaMapa()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 155,
   "id": "e6926783",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Quantas cidades o caminhão irá passar? 5\n",
      "Número de cidades definido para: 5\n"
     ]
    }
   ],
   "source": [
    "classe.definir_numero_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 156,
   "id": "1247d6d2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Qual vai ser a cidade inicial? Tupã\n",
      "Qual vai ser a cidade final? Caraguatatuba\n",
      "Você vai começar na cidade: Tupã, e vai acabar sua rota na cidade: Caraguatatuba\n"
     ]
    }
   ],
   "source": [
    "classe.inicio_objetivo()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 158,
   "id": "6c505732",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inclua a cidade que o caminhão irá passar: São Paulo\n"
     ]
    }
   ],
   "source": [
    "classe.importa_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 159,
   "id": "462a5892",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inclua a cidade que o caminhão irá passar: Osasco\n"
     ]
    }
   ],
   "source": [
    "classe.importa_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 160,
   "id": "c6ca83ce",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inclua a cidade que o caminhão irá passar: São Manuel\n"
     ]
    }
   ],
   "source": [
    "classe.importa_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 161,
   "id": "5ba9a74c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inclua a cidade que o caminhão irá passar: Aparecida\n",
      "Você já atingiu o número total de cidades\n"
     ]
    }
   ],
   "source": [
    "classe.importa_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "id": "d13a5070",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inclua a cidade que o caminhão irá passar: São Carlos\n",
      "Você já atingiu o número total de cidades\n"
     ]
    }
   ],
   "source": [
    "classe.importa_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 149,
   "id": "ed53d4d4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inclua a cidade que o caminhão irá passar: Ubatuba\n",
      "Você já atingiu o número total de cidades\n"
     ]
    }
   ],
   "source": [
    "classe.importa_cidades()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 163,
   "id": "8d370526",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Essas são as cidades que você deve passar por ordem:\n",
      "Tupã - 1°\n",
      "São Manuel - 2°\n",
      "Osasco - 3°\n",
      "São Paulo - 4°\n",
      "Caraguatatuba - 5°\n",
      "de Tupã até São Manuel a distancia é de 224.01km\n",
      "de São Manuel até Osasco a distancia é de 206.88km\n",
      "de Osasco até São Paulo a distancia é de 16.91km\n",
      "de São Paulo até Caraguatatuba a distancia é de 136.58km\n"
     ]
    }
   ],
   "source": [
    "classe.mostra_lista()\n",
    "classe.mostra_distancia()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 164,
   "id": "5b798c7a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "distancia total a ser percorrida é de 273.15km\n",
      "Qual nome do motorista?Adalberto\n",
      "Qual a placa do veículoFBE4040\n",
      "informe a data de saída do veiculo, no formato \"dia/mês/ano\":28/08/2024\n",
      "Quantos m³ deu a carga? :54\n",
      "Quantas toneladas deu a carga? :17500\n"
     ]
    }
   ],
   "source": [
    "classe.calcula_km()\n",
    "classe.cadastro_dados()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 165,
   "id": "c6f95546",
   "metadata": {},
   "outputs": [],
   "source": [
    "classe.dados_tabela()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 166,
   "id": "8a06d139",
   "metadata": {},
   "outputs": [],
   "source": [
    "classe.importa_dados()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 167,
   "id": "b331cb06",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Cidades</th>\n",
       "      <th>Pontos de entrega</th>\n",
       "      <th>Veiculo</th>\n",
       "      <th>Motorista</th>\n",
       "      <th>Km rodado</th>\n",
       "      <th>Saída</th>\n",
       "      <th>Previsão de dias para chegada (DIAS)</th>\n",
       "      <th>Peso carga</th>\n",
       "      <th>Cubicagem</th>\n",
       "      <th>Diaria Motorista</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>[Tupã, São Manuel, Osasco, São Paulo, Caraguat...</td>\n",
       "      <td>5</td>\n",
       "      <td>[FBE4040]</td>\n",
       "      <td>[Adalberto]</td>\n",
       "      <td>273.154453</td>\n",
       "      <td>[2024-08-28 00:00:00]</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>[17500]</td>\n",
       "      <td>[54]</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                             Cidades Pontos de entrega  \\\n",
       "0  [Tupã, São Manuel, Osasco, São Paulo, Caraguat...                 5   \n",
       "\n",
       "     Veiculo    Motorista   Km rodado                  Saída  \\\n",
       "0  [FBE4040]  [Adalberto]  273.154453  [2024-08-28 00:00:00]   \n",
       "\n",
       "   Previsão de dias para chegada (DIAS) Peso carga Cubicagem  Diaria Motorista  \n",
       "0                                1.0926    [17500]      [54]      27315.445315  "
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "classe.mostra_tabela()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 168,
   "id": "cbd93022",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Km rodado</th>\n",
       "      <th>Previsão de dias para chegada (DIAS)</th>\n",
       "      <th>Diaria Motorista</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>1.000000</td>\n",
       "      <td>1.0000</td>\n",
       "      <td>1.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>273.154453</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>273.154453</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>273.154453</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>273.154453</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>273.154453</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>273.154453</td>\n",
       "      <td>1.0926</td>\n",
       "      <td>27315.445315</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        Km rodado  Previsão de dias para chegada (DIAS)  Diaria Motorista\n",
       "count    1.000000                                1.0000          1.000000\n",
       "mean   273.154453                                1.0926      27315.445315\n",
       "std           NaN                                   NaN               NaN\n",
       "min    273.154453                                1.0926      27315.445315\n",
       "25%    273.154453                                1.0926      27315.445315\n",
       "50%    273.154453                                1.0926      27315.445315\n",
       "75%    273.154453                                1.0926      27315.445315\n",
       "max    273.154453                                1.0926      27315.445315"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "classe.informacoes_tabela()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "1eef3a51",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "62ddc266",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d1f0468c",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
