class Torre:
    def __init__(self, id, nome, endereco):
        self.id = id
        self.nome = nome
        self.endereco = endereco

class Apartamento:
    def __init__(self, id, numero_apartamento, torre):
        self.id = id
        self.numero_apartamento = numero_apartamento
        self.numero_vaga_garagem = None
        self.torre = torre

    def __repr__(self):
        return f"Apartamento {self.numero_apartamento} na torre {self.torre.nome} (Vaga: {self.numero_vaga_garagem})"

class FilaDeEspera:
    def __init__(self):
        self.fila = []

    def adicionar_apartamento(self, apartamento):
        self.fila.append(apartamento)

    def retirar_apartamento(self, numero_vaga):
        for apartamento in self.fila:
            if apartamento.numero_vaga_garagem == numero_vaga:
                self.fila.remove(apartamento)
                return apartamento
        return None

    def imprimir_fila(self):
        if not self.fila:
            print("A fila de espera está vazia.")
        else:
            print("Fila de espera:")
            for apartamento in self.fila:
                print(apartamento)

class ListaApartamentosComVaga:
    def __init__(self):
        self.apartamentos = []

    def adicionar_apartamento(self, apartamento):
        self.apartamentos.append(apartamento)
        self.apartamentos.sort(key=lambda x: x.numero_vaga_garagem)

    def liberar_vaga(self, numero_vaga):
        for i, apartamento in enumerate(self.apartamentos):
            if apartamento.numero_vaga_garagem == numero_vaga:
                return self.apartamentos.pop(i)
        return None

    def imprimir_lista(self):
        if not self.apartamentos:
            print("Não há apartamentos com vaga de garagem.")
        else:
            print("Apartamentos com vaga de garagem:")
            for apartamento in self.apartamentos:
                print(apartamento)

class Condominio:
    def __init__(self, max_vagas=10):
        self.torres = []
        self.lista_vagas = ListaApartamentosComVaga()
        self.fila_espera = FilaDeEspera()
        self.max_vagas = max_vagas

    def adicionar_torre(self, torre):
        self.torres.append(torre)

    def cadastrar_apartamento(self, apartamento):
        if len(self.lista_vagas.apartamentos) < self.max_vagas:
            apartamento.numero_vaga_garagem = len(self.lista_vagas.apartamentos) + 1
            self.lista_vagas.adicionar_apartamento(apartamento)
        else:
            self.fila_espera.adicionar_apartamento(apartamento)

    def liberar_vaga(self, numero_vaga):
        apto_liberado = self.lista_vagas.liberar_vaga(numero_vaga)
        if apto_liberado:
            apto_liberado.numero_vaga_garagem = None
            self.fila_espera.adicionar_apartamento(apto_liberado)

            apto_da_fila = self.fila_espera.retirar_apartamento(numero_vaga)
            if apto_da_fila:
                self.lista_vagas.adicionar_apartamento(apto_da_fila)
            else:
                print("Vaga não encontrada.")

    def imprimir_lista_vagas(self):
        self.lista_vagas.imprimir_lista()

    def imprimir_fila_espera(self):
        self.fila_espera.imprimir_fila()

def carregar_dados_iniciais(filepath='dados_iniciais.json'):
    try:
        with open(filepath, 'r') as file:
            dados = json.load(file)

        condominio = Condominio()
        torres_dict = {}

        # Adicionar torres
        for torre_data in dados["torres"]:
            torre = Torre(torre_data["id"], torre_data["nome"], torre_data["endereco"])
            condominio.adicionar_torre(torre)
            torres_dict[torre.id] = torre

        # Cadastrar apartamentos
        for apt_data in dados["apartamentos"]:
            torre = torres_dict[apt_data["torre_id"]]
            apartamento = Apartamento(apt_data["id"], apt_data["numero_apartamento"], torre)
            condominio.cadastrar_apartamento(apartamento)

        return condominio

    except FileNotFoundError:
        print(f"Arquivo {filepath} não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo {filepath}. Verifique se o JSON está formatado corretamente.")
        return None

def menu():
    condominio = carregar_dados_iniciais()

    if not condominio:
        print("Erro ao carregar os dados iniciais. Encerrando o programa.")
        return

    while True:
        print("\nMenu de Opções:")
        print("1. Adicionar torre")
        print("2. Cadastrar apartamento")
        print("3. Liberar vaga")
        print("4. Imprimir lista de apartamentos com vaga")
        print("5. Imprimir fila de espera")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            id = input("ID da torre: ")
            nome = input("Nome da torre: ")
            endereco = input("Endereço da torre: ")
            torre = Torre(id, nome, endereco)
            condominio.adicionar_torre(torre)

        elif opcao == '2':
            if not condominio.torres:
                print("Primeiro, adicione uma torre.")
                continue
            id = input("ID do apartamento: ")
            numero_apartamento = input("Número do apartamento: ")
            print("Torres disponíveis:")
            for i, torre in enumerate(condominio.torres):
                print(f"{i + 1}. {torre.nome} ({torre.endereco})")
            indice_torre = int(input("Escolha a torre: ")) - 1
            torre = condominio.torres[indice_torre]
            apartamento = Apartamento(id, numero_apartamento, torre)
            condominio.cadastrar_apartamento(apartamento)

        elif opcao == '3':
            numero_vaga = int(input("Número da vaga a ser liberada: "))
            condominio.liberar_vaga(numero_vaga)

        elif opcao == '4':
            condominio.imprimir_lista_vagas()

        elif opcao == '5':
            condominio.imprimir_fila_espera()

        elif opcao == '6':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
