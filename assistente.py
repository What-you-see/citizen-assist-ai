import csv
from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(self, nome="Citizen Assist AI"):
        self.nome = nome
        self.base = BaseConhecimento()
        self.base.carregar()

    def _contem_dado_pessoal(self, texto):
        if "@" in texto:
            return True
        qtd_digitos = sum(1 for caractere in texto if caractere.isdigit())
        return qtd_digitos >= 8

    def _confirmar_sim_nao(self, mensagem):
        while True:
            resp = input(mensagem).strip().lower()
            if resp in ("s", "n"):
                return resp == "s"
            print("Entrada inválida. Digite 's' para sim ou 'n' para não.")

    def _ler_opcao_numerica(self, mensagem, maximo):
        while True:
            entrada = input(mensagem).strip()
            if entrada.isdigit():
                valor = int(entrada)
                if 0 <= valor <= maximo:
                    return valor
            print(f"Entrada inválida. Digite um número entre 0 e {maximo}.")

    def perguntar(self):
        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if not pergunta:
                print("Por favor, digite uma pergunta válida.")
                continue

            if self._contem_dado_pessoal(pergunta):
                print("Pergunta recusada por conter possível dado pessoal (8 ou mais dígitos ou '@').")
                continue

            resultados = self.base.buscar(pergunta)

            if not resultados:
                print("Não encontrei uma orientação confiável para essa dúvida.")
                if self._confirmar_sim_nao("Quer procurar pelas categorias? (s/n): "):
                    self.navegar(pergunta_origem=pergunta)
                return

            melhor_pontos, melhor_orientacao = resultados[0]
            confianca = "ALTA" if melhor_pontos >= 6 else "MÉDIA"
            print(f"\n[Confiança {confianca} - {melhor_pontos} pontos]")

            melhor_orientacao.exibir()
            melhor_orientacao.registrar_acesso()
            self.base.salvar()

            if self._confirmar_sim_nao("Essa orientação respondeu sua dúvida? (s/n): "):
                return

            print("Tudo bem! Vamos procurar nas categorias disponíveis.")
            if self._confirmar_sim_nao("Quer procurar pelas categorias? (s/n): "):
                self.navegar(pergunta_origem=pergunta)
            return

    def navegar(self, pergunta_origem=None):
        categorias = self.base.listar_categorias()
        if not categorias:
            print("Nenhuma categoria cadastrada.")
            return

        print()
        for idx, cat in enumerate(categorias, start=1):
            print(f"[{idx}] {cat}", end="  ")
        print()

        escolha_cat = self._ler_opcao_numerica("Escolha a categoria (0 para voltar): ", len(categorias))
        if escolha_cat == 0:
            return

        categoria_selecionada = categorias[escolha_cat - 1]
        orientacoes_cat = self.base.orientacoes_por_categoria(categoria_selecionada)

        for idx, ori in enumerate(orientacoes_cat, start=1):
            print(f"[{idx}] {ori.titulo}")

        escolha_ori = self._ler_opcao_numerica("Escolha a orientação (0 para voltar): ", len(orientacoes_cat))
        if escolha_ori == 0:
            return

        orientacao_escolhida = orientacoes_cat[escolha_ori - 1]
        orientacao_escolhida.exibir()
        orientacao_escolhida.registrar_acesso()
        self.base.salvar()

        if pergunta_origem:
            if self._confirmar_sim_nao("Essa orientação respondeu sua dúvida? (s/n): "):
                self.aprender(pergunta_origem, orientacao_escolhida)

    def aprender(self, pergunta, orientacao):
        candidatas = self.base.palavras_novas(pergunta, orientacao)
        if not candidatas:
            print("Nenhuma palavra nova elegível para aprendizado nesta pergunta.")
            return

        aprendidas = 0
        for palavra in candidatas:
            if self._confirmar_sim_nao(f"Aprender '{palavra}' para '{orientacao.titulo}'? (s/n): "):
                if orientacao.adicionar_palavra_chave(palavra):
                    aprendidas += 1

        if aprendidas > 0:
            self.base.salvar()
        print(f"{aprendidas} palavra(s)-chave aprendida(s).")

    def relatorio(self):
        mais_acessadas, nunca_acessadas, por_categoria = self.base.ranking()

        print("\n=== RELATÓRIO DE USO ===")
        print("\nTop 3 orientações mais acessadas:")
        for ori in mais_acessadas:
            print(f"- {ori.titulo} ({ori.categoria}): {ori.acessos} acesso(s)")

        print("\nOrientações nunca acessadas:")
        if not nunca_acessadas:
            print("- Nenhuma (todas já foram acessadas ao menos uma vez).")
        else:
            for ori in nunca_acessadas:
                print(f"- {ori.titulo} ({ori.categoria})")

        print("\nTotal de acessos por categoria:")
        for categoria, total in por_categoria.items():
            print(f"- {categoria}: {total}")

    def exportar_csv(self, caminho_csv="data/relatorio.csv"):
        campos = ["id", "categoria", "titulo", "acessos", "total de palavras-chave"]
        with open(caminho_csv, "w", newline="", encoding="utf-8") as arq_csv:
            escritor = csv.DictWriter(arq_csv, fieldnames=campos)
            escritor.writeheader()
            for ori in self.base.orientacoes:
                escritor.writerow({
                    "id": ori.id,
                    "categoria": ori.categoria,
                    "titulo": ori.titulo,
                    "acessos": ori.acessos,
                    "total de palavras-chave": len(ori.palavras_chave),
                })
        print(f"Relatório exportado com sucesso para '{caminho_csv}'.")
