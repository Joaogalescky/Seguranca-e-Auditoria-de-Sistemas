import streamlit as st
import os
import string
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

def limpar_texto(texto):
    texto = texto.translate(str.maketrans('', '', string.punctuation + string.digits))
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    return texto.lower().replace(' ', '')

def analisar_freq(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        texto = file.read()
    texto_limpo = limpar_texto(texto)
    frequencia = Counter(texto_limpo)
    total_chars = sum(frequencia.values())
    freq_percent = {char: (count/total_chars)*100 for char, count in frequencia.items()}
    return freq_percent

def analisar_quant(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        texto = file.read()
    texto_limpo = limpar_texto(texto)
    quantidade = Counter(texto_limpo)
    return quantidade

def plot_freq(data, language):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Frequência (%)'])
    df.sort_values(by='Frequência (%)', ascending=False, inplace=True)
    fig, ax = plt.subplots()
    df.plot(kind='bar', ax=ax)
    ax.set_title(f'Frequência de Caracteres - {language}')
    ax.set_ylabel('Frequência (%)')
    st.pyplot(fig)
    return df

def plot_quant(data, language):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Quantidade'])
    df.sort_values(by='Quantidade', ascending=False, inplace=True)
    fig, ax = plt.subplots()
    df.plot(kind='bar', ax=ax)
    ax.set_title(f'Quantidade de Caracteres - {language}')
    ax.set_ylabel('Quantidade')
    st.pyplot(fig)
    return df

def main():
    st.title('Análise de Frequência de Caracteres')
    
    st.write('Essa página destina-se a análise da frequência de caracteres de um ou mais idiomas, comparando em porcentagem e quantidade as 5 maiores presenças de letras de uma linguagem em sua escrita.')

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, 'database')

    ptbr_file = os.path.join(db_dir, 'portugues.txt')
    en_file = os.path.join(db_dir, 'ingles.txt')
    de_file = os.path.join(db_dir, 'alemao.txt')
    jp_file = os.path.join(db_dir, 'japones.txt')

    if not all(os.path.exists(f) for f in [ptbr_file, en_file, de_file, jp_file]):
        st.error("Arquivos não encontrados na pasta 'database'")
        return

    ptbr_freq = analisar_freq(ptbr_file)
    en_freq = analisar_freq(en_file)
    de_freq = analisar_freq(de_file)
    jp_freq = analisar_freq(jp_file)

    ptbr_quant = analisar_quant(ptbr_file)
    en_quant = analisar_quant(en_file)
    de_quant = analisar_quant(de_file)
    jp_quant = analisar_quant(jp_file)

    st.header('A) Tabela e Gráfico de Frequência')

    idiomas = {
        'Português': (ptbr_freq, ptbr_quant),
        'Inglês': (en_freq, en_quant),
        'Alemão': (de_freq, de_quant),
        'Japonês': (jp_freq, jp_quant)
    }

    tabs = st.tabs(list(idiomas.keys()))

    for tab, (idioma, (freq, quant)) in zip(tabs, idiomas.items()):
        with tab:
            df_freq = pd.DataFrame.from_dict(freq, orient='index', columns=['Frequência (%)'])
            df_quant = pd.DataFrame.from_dict(quant, orient='index', columns=['Quantidade'])
            df_combined = pd.concat([df_freq, df_quant], axis=1)
            df_combined.sort_values(by='Frequência (%)', ascending=False, inplace=True)

            st.subheader(f'{idioma}')
            st.dataframe(df_combined.style.format({
                'Frequência (%)': '{:.2f}%',
                'Quantidade': '{}'
            }))

            st.subheader('Gráfico de Frequência (%)')
            plot_freq(freq, idioma)

            st.subheader('Gráfico de Quantidade')
            plot_quant(quant, idioma)

    st.header('B) Letras mais frequentes - 5 letras mais utilizadas em cada idioma')

    for idioma, (freq, _) in idiomas.items():
        df_freq = pd.DataFrame.from_dict(freq, orient='index', columns=['Frequência (%)'])
        df_freq.sort_values(by='Frequência (%)', ascending=False, inplace=True)
        top_chars = df_freq.head(5)
        
        st.markdown(f"### Frequência de caracteres - **{idioma}**")
        st.dataframe(top_chars.style.format({'Frequência (%)': '{:.2f}'}).set_properties(**{
            'font-size': '16px',
            'text-align': 'center'
        }))

if __name__ == '__main__':
    main()
