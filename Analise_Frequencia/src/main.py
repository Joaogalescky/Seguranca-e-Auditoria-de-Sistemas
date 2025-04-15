import streamlit as st
import os
import string
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

def limpar_texto(texto):
    # Remove pontuações e números
    texto = texto.translate(str.maketrans('', '', string.punctuation + string.digits))
    # Remove acentuações
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    # Remove espaços extras e converte para minúsculas
    return texto.lower().replace(' ', '')

def analisar_freq(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        texto = file.read()
    texto_limpo = limpar_texto(texto)
    frequencia = Counter(texto_limpo)
    total_chars = sum(frequencia.values())
    
    # Porcentagem
    freq_percent = {char: (count/total_chars)*100 for char, count in frequencia.items()}
    return freq_percent

def plot_freq(data, language):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Frequência (%)'])
    df.sort_values(by='Frequência (%)', ascending=False, inplace=True)
    
    fig, ax = plt.subplots()
    df.plot(kind='bar', ax=ax)
    ax.set_title(f'Frequência de Caracteres - {language}')
    ax.set_ylabel('Frequência (%)')
    st.pyplot(fig)
    return df

def main():
    st.title('Análise de Frequência de Caracteres')
    
    # Caminho relativo
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, 'database')
    
    # Caminho dos arquivos
    ptbr_file = os.path.join(db_dir, 'portugues.txt')
    en_file = os.path.join(db_dir, 'ingles.txt')
    
    if not os.path.exists(ptbr_file) or not os.path.exists(en_file):
        st.error("Arquivos não encontrados na pasta 'database'")
        return
    
    # Análise
    ptbr_freq = analisar_freq(ptbr_file)
    en_freq = analisar_freq(en_file)
    
    # Resultados
    st.header('a. Tabela e Gráfico de Frequência')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Português')
        ptbr_df = plot_freq(ptbr_freq, 'Português')
        st.dataframe(ptbr_df.style.format({'Frequência (%)': '{:.2f}%'}))
    
    with col2:
        st.subheader('Inglês')
        en_df = plot_freq(en_freq, 'Inglês')
        st.dataframe(en_df.style.format({'Frequência (%)': '{:.2f}%'}))
    
    st.header('b. Letras mais frequentes')
    
    ptbr_top = ptbr_df.head(3).index.tolist()
    en_top = en_df.head(3).index.tolist()
    
    st.write(f"Português (Top 3): {', '.join(ptbr_top)}")
    st.write(f"Inglês (Top 3): {', '.join(en_top)}")

if __name__ == '__main__':
    main()