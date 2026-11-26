import json
from orientacao import Orientacao

ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e", "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u", "ç": "c"
}

PALAVRAS_IGNORADAS = (
    "como", "onde", "quero", "preciso", "para", "qual", "quais",
    "quem", "quando", "porque", "por", "com", "sem", "uma", "uns",
    "umas", "meu", "minha", "meus", "minhas", "seu", "sua", "sobre",
    "fazer", "tirar", "pegar", "saber", "posso", "pode", "esta", "esse"
)


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho_base="data/base_conhecimento.json", caminho_sinonimos="data/sinonimos.json"):
        self.caminho_base = caminho_base
        self.caminho_sinonimos = caminho_sinonimos
        self.orientacoes = []
        self.sinonimos = {}

    def carregar(self):
        with open(self.caminho_base, "r", encoding="utf-8") as arq_base:
            dados_base = json.load(arq_base)
            self.orientacoes = [
                Orientacao(
                    id=item["id"],
                    categoria=item["categoria"],
                    titulo=item["titulo"],
                    palavras_chave=item["palavras_chave"],
                    resposta=item["resposta"],
                    fonte=item["fonte"],
                    acessos=item.get("acessos", 0),
                )
                for item in dados_base
            ]

        with open(self.caminho_sinonimos, "r", encoding="utf-8") as arq_sin:
            self.sinonimos = json.load(arq_sin)

    def salvar(self):
        dados_para_salvar = [orientacao.para_dict() for orientacao in self.orientacoes]
        with open(self.caminho_base, "w", encoding="utf-8") as arq_base:
            json.dump(dados_para_salvar, arq_base, ensure_ascii=False, indent=2)

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        palavras_pergunta = set(pergunta_norm.strip().split())
        titulo_norm = normalizar(orientacao.titulo)
        palavras_titulo = set(titulo_norm.strip().split())

        pontos = 0

        # +3 pontos por palavra-chave da orientação que aparece na pergunta
        for chave in orientacao.palavras_chave:
            chave_norm = normalizar(chave)
            if chave_norm in pergunta_norm:
                pontos += 3

        # +2 pontos por sinônimo que corresponda a uma palavra-chave da orientação
        for palavra in palavras_pergunta:
            if palavra in self.sinonimos:
                equivalentes = self.sinonimos[palavra]
                for eq in equivalentes:
                    if eq in orientacao.palavras_chave:
                        pontos += 2

        # +1 ponto por palavra da pergunta (4 letras ou mais) que aparece no título
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos >= 3:
                resultados.append((pontos, orientacao))

        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados

    def palavras_novas(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        palavras = pergunta_norm.strip().split()
        chaves_norm = [normalizar(c).strip() for c in orientacao.palavras_chave]

        candidatas = []
        for palavra in palavras:
            if (
                len(palavra) >= 4
                and palavra not in chaves_norm
                and palavra not in PALAVRAS_IGNORADAS
                and palavra not in candidatas
            ):
                candidatas.append(palavra)
            if len(candidatas) == 3:
                break

        return candidatas

    def listar_categorias(self):
        categorias = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in categorias:
                categorias.append(orientacao.categoria)
        return categorias

    def orientacoes_por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def ranking(self):
        ordenadas = sorted(self.orientacoes, key=lambda o: o.acessos, reverse=True)
        mais_acessadas = ordenadas[:3]
        nunca_acessadas = [o for o in self.orientacoes if o.acessos == 0]

        acessos_por_categoria = {}
        for o in self.orientacoes:
            acessos_por_categoria[o.categoria] = acessos_por_categoria.get(o.categoria, 0) + o.acessos

        return mais_acessadas, nunca_acessadas, acessos_por_categoria
