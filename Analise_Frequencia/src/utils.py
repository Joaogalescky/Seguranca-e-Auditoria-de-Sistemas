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