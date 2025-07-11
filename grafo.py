
    
class Grafo:
    def __init__(self):
        self.cidades = []
        self.conexoes = []
        self.buscar_dados('dados.csv')

    def buscar_dados(self, caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
                for i, linha in enumerate(linhas, 1):
                    linha = linha.strip()
                    if linha != '':
                        partes = linha.split(',')
                        if len(partes) == 3:
                            nome1 = partes[0].strip()
                            nome2 = partes[1].strip()
                            distancia_str = partes[2].lower().replace('km', '').strip()
                            distancia = float(distancia_str)
                            if not self.buscar_cidade(nome1):
                                self.cadastrar_cidade(nome1)
                            if not self.buscar_cidade(nome2):
                                self.cadastrar_cidade(nome2)
                            self.cadastrar_conexao(nome1, nome2, distancia)

    def salvar_dados(self,nome1,nome2,distancia):
        with open('dados.csv','a',encoding='utf-8') as arquivo:
            arquivo.write(f'{nome1},{nome2},{distancia}km\n')

    @staticmethod    
    def ordenar_nome(cidade):
        return cidade.nomeCidade
        
    def info_cidades(self):
        if not self.cidades:
            print('')
            print('Nenhuma cidade cadastrada')
            print('')
        for cidade in sorted(self.cidades, key=Grafo.ordenar_nome):
            cidade.info_vertice()


    def info_conexoes(self):
        for conexao in self.conexoes:
            print(conexao)

    def cadastrar_cidade(self, nomecidade):
        if self.buscar_cidade(nomecidade):
            print("Cidade já cadastrada!")
            return
        cidade = Vertice(nomecidade)
        self.cidades.append(cidade)

    def cadastrar_conexao(self, nome1, nome2, distancia,):
        cidade1 = self.buscar_cidade(nome1)
        cidade2 = self.buscar_cidade(nome2)
        if cidade1 and cidade2:
            for aresta in self.conexoes:
                if ({aresta.cidade1, aresta.cidade2} == {cidade1,cidade2}):
                    print("Conexão já existente")
                    return
            aresta = Aresta(cidade1, cidade2, distancia)
            self.conexoes.append(aresta)
            cidade1.cadastrar_vizinho(cidade2,distancia)
            cidade2.cadastrar_vizinho(cidade1,distancia)
            cidade1.cadastrar_conexao(aresta)
            cidade2.cadastrar_conexao(aresta)
        else:
            print("Uma ou ambas as cidades não existem!")

    def buscar_cidade(self, nome):
        for cidade in self.cidades:
            if cidade.nomeCidade == nome:
                return cidade
        return None

    def menu(self):
        while True:

            print('\n----Menu Principal----')
            print('1 - Cadastrar cidade')
            print('2 - Cadastrar conexão')
            print('3 - Listar cidades')
            print('4 - Listar conexões')
            print('5 - Listar cidades vizinhas')
            print('0 - Sair')
            print('\n----------------------')
            selecao = input('Escolha uma opção: ')    

            if selecao == '1':
                print('')
                nome = input("Digite o nome da cidade: ")
                self.cadastrar_cidade(nome)
                print('')
            elif selecao == '2':
                nome1 = input("Nome da primeira cidade: ")
                nome2 = input("Nome da segunda cidade: ")
                distancia = float(input("Distância entre elas: "))
                evitarduplicar = len(self.conexoes)
                self.cadastrar_conexao(nome1, nome2, distancia)
                if len(self.conexoes) > evitarduplicar:
                    self.salvar_dados(nome1,nome2,distancia)

            elif selecao == '3':
                self.info_cidades()
            elif selecao == '4':
                self.info_conexoes()
            elif selecao == '5':
                nome = input("Digite o nome da cidade: ")
                cidade = self.buscar_cidade(nome)
                if cidade:
                    cidade.info_vizinhos()
                else:
                    print("Cidade não encontrada.")
            elif selecao == '0':
                break
            else:
                print("Opção inválida.")

class Vertice:
    def __init__(self, nomeCidade: str):
        self.nomeCidade = nomeCidade
        self.vizinhanca = []
        self.conexoes = []

    def cadastrar_vizinho(self, vizinho, distancia):
        self.vizinhanca.append((vizinho, distancia))

    def cadastrar_conexao(self, aresta):
        self.conexoes.append(aresta)

    def info_vizinhos(self):
        print('')
        print(f"Vizinhos da cidade {self.nomeCidade}")
        print('')

        vizinhos_ordenacao = sorted(self.vizinhanca, key=lambda ordenacao: ordenacao[1])
        for vizinhos, distancia in vizinhos_ordenacao:
            print(f'Nome vizinho : {vizinhos.nomeCidade} \nDistancia : {distancia} km ')

    def info_conexoes(self):
        if not self.conexoes:
            print(f'\nCidade {self.nomeCidade} não possui conexões cadastradas.')
            return
        for conexao in self.conexoes:
            print(conexao)

    def info_vertice(self):
        print(f'\nCidade: {self.nomeCidade}')

class Aresta:
    def __init__(self, cidade1, cidade2, distancia: int):
        self.cidade1 = cidade1
        self.cidade2 = cidade2
        self.distancia = distancia

    def __str__(self):
        return f'Cidades: {self.cidade1.nomeCidade}, {self.cidade2.nomeCidade}  Distância: {self.distancia} km'

if __name__ == "__main__":
    grafo = Grafo()
    grafo.menu()
        