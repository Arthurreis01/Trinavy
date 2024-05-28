import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Carregar dados
data = pd.read_excel('TESTE PYTHON.xlsm')

# Converter 'Tempo decorrido' para timedelta
data['Tempo decorrido'] = pd.to_timedelta(data['Tempo decorrido'].astype(str))

# Renomear colunas para facilitar o acesso (verifique se a planilha possui exatamente estas colunas)
data.columns = ['Classificação', 'Código', 'Nome do Atleta', 'Categoria', 'Sexo', 'Tempo decorrido', 'Modalidade']

st.title("Trinavy - Seu Destino é a Glória!")
st.markdown("Classificação - Simulado de Natação")
# Dica para a sidebar
st.markdown("""
    <style>
    .sidebar-tooltip {
        position: fixed;
        top: 50px;
        left: 10px;
        padding: 10px;
        background-color: #ffcd21;
        border-radius: 5px;
        z-index: 1000;
        font-size: 18px;
        color: black;
    }
    </style>
    <div class="sidebar-tooltip">Clique na seta para filtrar os resultados</div>
""", unsafe_allow_html=True)

# Filtros no sidebar
st.sidebar.image("logobg.png.png")
modalidade = st.sidebar.selectbox("Modalidade", list(data['Modalidade'].unique()))
categoria = st.sidebar.selectbox("Categoria", ["Todos"] + list(data['Categoria'].unique()))
sexo = st.sidebar.selectbox("Sexo", ["Todos"] + list(data['Sexo'].unique()))

# Aplicar filtros
filtered_data = data.copy()
if modalidade != "Todos":
    filtered_data = filtered_data[filtered_data['Modalidade'] == modalidade]
if categoria != "Todos":
    filtered_data = filtered_data[filtered_data['Categoria'] == categoria]
if sexo != "Todos":
    filtered_data = filtered_data[filtered_data['Sexo'] == sexo]

# Reclassificar por tempo decorrido
filtered_data = filtered_data.sort_values('Tempo decorrido').reset_index(drop=True)
filtered_data['Classificação'] = filtered_data.index + 1


# CSS para definir estilos que funcionam em ambos os modos
css = """
<style>
.card {
    border: 1px solid #666;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    color: black;  /* cor do texto padrão */
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-between;
    background-color: white; /* cor de fundo padrão */
}
.card h4 {
    color: #333333;  /* cor do texto do título */
}
@media (prefers-color-scheme: dark) {
    .card {
        color: white;  /* cor do texto no modo escuro */
        background-color: #333333;  /* cor de fundo no modo escuro */
    }
    .card h4 {
        color: #ffcd21;  /* cor do título no modo escuro */
    }
    #classificação {
        color: #ffcd21;  
    }
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Mostrar tabela com classificação em formato de cards
st.subheader("Classificação")
for index, row in filtered_data.iterrows():
    tempo_formatado = str(row['Tempo decorrido']).split()[-1] if pd.notna(row['Tempo decorrido']) else "Tempo inválido"
    st.markdown(f"""
    <div class="card">
        <h4>Atleta: {row['Nome do Atleta']}</h4>
        <p id="classificação"><strong>Classificação:</strong> {row['Classificação']}</p>
        <p><strong>Categoria:</strong> {row['Categoria']}</p>
        <p><strong>Sexo:</strong> {row['Sexo']}</p>
        <p><strong>Tempo decorrido:</strong> {tempo_formatado}</p>
        <p><strong>Modalidade:</strong> {row['Modalidade']}</p>
    </div>
    """, unsafe_allow_html=True)
