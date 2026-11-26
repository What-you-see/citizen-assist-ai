from assistente import Assistente


def main():
    assistente = Assistente("Citizen Assist AI")

    while True:
        print(f"\n=== {assistente.nome} ===")
        print("[1] Fazer uma pergunta")
        print("[2] Navegar por categorias")
        print("[3] Relatório de uso")
        print("[4] Exportar relatório CSV")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.relatorio()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            print("Encerrando o assistente. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
