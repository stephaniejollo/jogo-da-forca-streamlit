import streamlit as st
import random
import unicodedata

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Dicionário de palavras e suas dicas
palavras_dicas = {
    "oração": "Ato de se comunicar com o divino.",
    "público": "Conjunto de pessoas em um evento.",
    "solução": "Resposta para um problema.",
    "coração": "Órgão vital.",
    "informação": "Aquilo que comunica conhecimento.",
    "difícil": "Oposto de fácil.",
    "rápido": "Muito veloz.",
    "caminhão": "Veículo de carga.",
    "pão": "Alimento feito de farinha.",
    "televisão": "Aparelho de entretenimento.",
    "saúde": "Estado de completo bem-estar.",
    "café": "Bebida energética popular.",
    "emoção": "Sentimento intenso.",
    "herói": "Pessoa admirável por coragem.",
    "abacaxi": "Fruta tropical com coroa.",
    "açúcar": "Ingrediente doce.",
    "pássaro": "Animal que voa.",
    "avião": "Meio de transporte aéreo.",
    "caçador": "Quem busca caçar.",
    "esforço": "Ato de se empenhar.",
    "leão": "Rei da selva.",
    "computação": "Área da ciência de dados.",
    "ação": "Iniciativa prática.",
    "solidão": "Estado de estar só.",
    "alegria": "Felicidade intensa.",
    "educação": "Processo de aprendizagem.",
    "país": "Nação com território.",
    "fácil": "Sem dificuldade.",
    "líder": "Pessoa que guia outras.",
    "organização": "Estrutura sistematizada.",
    "prêmio": "Reconhecimento por conquista.",
    "vitória": "Ato de vencer.",
    "desafio": "Tarefa difícil.",
    "professor": "Quem ensina.",
    "violão": "Instrumento musical.",
    "ônibus": "Transporte coletivo urbano.",
    "parabéns": "Expressão de congratulação.",
    "razão": "Capacidade de raciocínio.",
    "visão": "Sentido de enxergar.",
    "missão": "Tarefa a ser cumprida.",
    "colégio": "Instituição de ensino.",
    "sugestão": "Ideia proposta.",
    "explicação": "Ato de tornar algo claro.",
    "inspiração": "Fonte de motivação.",
    "matéria": "Conteúdo de estudo.",
    "visita": "Ato de ir a algum lugar.",
    "bênção": "Ato de abençoar.",
    "vitamina": "Nutriente essencial.",
    "mudança": "Transformação.",
    "trabalho": "Atividade laboral.",
    "esperança": "Expectativa positiva.",
    "júri": "Grupo que decide um veredito.",
    "céu": "Onde estão as nuvens.",
    "lâmpada": "Objeto que ilumina.",
    "fênix": "Ave mitológica que renasce.",
    "álbum": "Coleção organizada de itens.",
    "árvore": "Planta com tronco e galhos.",
    "ônix": "Tipo de pedra preciosa.",
    "ícone": "Símbolo representativo.",
    "índio": "Habitante originário do Brasil.",
    "fórum": "Espaço de debate público.",
    "júbilo": "Alegria intensa.",
    "tênis": "Calçado ou esporte com raquete.",
    "cúmplice": "Pessoa que colabora em segredo.",
    "mágico": "Relacionado à magia.",
    "ímpar": "Número que não é divisível por 2."
}

# Etapa 1: Escolher se quer jogar com ou sem dica
if "modo_escolhido" not in st.session_state:
    st.session_state.modo_escolhido = False

if not st.session_state.modo_escolhido:
    st.title("🎯 Jogo da Forca Premium")
    st.subheader("Escolha o modo de jogo:")
    usar_dica = st.radio("Deseja jogar com dica?", ["Sim", "Não"], key="modo_dica")
    if st.button("Iniciar Jogo"):
        st.session_state.usar_dica = usar_dica == "Sim"
        st.session_state.palavra, st.session_state.dica = random.choice(list(palavras_dicas.items()))
        st.session_state.tabuleiro = ["_" for _ in st.session_state.palavra]
        st.session_state.letras_tentadas = []
        st.session_state.chances = len(st.session_state.palavra)
        st.session_state.mensagem = ""
        st.session_state.modo_escolhido = True
        st.rerun()  # <-- força a interface a atualizar imediatamente
    st.stop()

st.title("🎯 Jogo da Forca Premium")
if st.session_state.usar_dica:
    st.write(f"Dica: *{st.session_state.dica}*")

# Mostrar palavra com tratamento de acento
palavra_display = " ".join([
    letra if remover_acentos(letra.lower()) in st.session_state.letras_tentadas else "_"
    for letra in st.session_state.palavra
])
st.write(f"Palavra: {palavra_display}")

# Função que processa a letra automaticamente
def processar_letra():
    letra = st.session_state.input_letra
    st.session_state.input_letra = ""  # limpa o campo após a tentativa

    letra = remover_acentos(letra.lower())

    if not letra.isalpha():
        st.session_state.mensagem = "⚠️ Digite apenas letras."
        return
    if letra in st.session_state.letras_tentadas:
        st.session_state.mensagem = "ℹ️ Você já tentou essa letra."
        return

    st.session_state.letras_tentadas.append(letra)

    if letra in [remover_acentos(l.lower()) for l in st.session_state.palavra]:
        for i, l in enumerate(st.session_state.palavra):
            if remover_acentos(l.lower()) == letra:
                st.session_state.tabuleiro[i] = l
        st.session_state.mensagem = "✅ Letra correta!"
    else:
        st.session_state.chances -= 1
        st.session_state.mensagem = "❌ Letra incorreta!"

# Entrada da letra com on_change
st.text_input("Digite uma letra", max_chars=1, key="input_letra", on_change=processar_letra)


# Mostra letras tentadas e mensagem
st.write("Letras tentadas:", ", ".join(st.session_state.letras_tentadas))
st.write(st.session_state.mensagem)

# Verifica vitória ou derrota
if "_" not in st.session_state.tabuleiro:
    st.success(f"Parabéns! Você acertou: {st.session_state.palavra}")
    if st.button("Jogar novamente"):
        st.session_state.clear()
        st.rerun()
elif st.session_state.chances == 0:
    st.error(f"Você perdeu! A palavra era: {st.session_state.palavra}")
    if st.button("Tentar de novo"):
        st.session_state.clear()
        st.rerun()
else:
    st.write(f"Tentativas restantes: {st.session_state.chances}")