import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Carregar dados
data = pd.read_excel('TESTE PYTHON.xlsm')

# 1.2 Darkmode function
def toggle_dark_mode():
    # Adiciona o botão ao lado do título
    button_clicked = st.button("🌙 Toggle Dark Mode")

    if button_clicked:
        st.session_state.dark_mode = not st.session_state.get("dark_mode", False)

    return st.session_state.get("dark_mode", False)

# Setting the button (dark/light)
dark_mode = toggle_dark_mode()
if dark_mode:
    st.markdown(
        """
        <style>
            body {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            .stApp {
                filter: invert(1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Converter 'Tempo decorrido' para timedelta
data['Tempo decorrido'] = pd.to_timedelta(data['Tempo decorrido'].astype(str))

# Renomear colunas para facilitar o acesso (verifique se a planilha possui exatamente estas colunas)
data.columns = ['Classificação', 'Código', 'Nome do Atleta', 'Categoria', 'Sexo', 'Tempo decorrido', 'Modalidade']

st.title("Trinavy - Simulado de Natação")

# Filtros no sidebar
st.sidebar.image("logobg.png.png")
modalidade = st.sidebar.selectbox("Modalidade", ["Todos"] + list(data['Modalidade'].unique()))
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

# Classificar por tempo decorrido
filtered_data = filtered_data.sort_values('Tempo decorrido')
def gerar_certificado(nome, tempo, categoria_pos, geral_pos, ritmo, modalidade):
    # Carregar imagem de fundo do certificado
    img = Image.open('certificado_base.jpg.jpeg')
    draw = ImageDraw.Draw(img)
    
    # Definir fontes
    font_title = ImageFont.truetype('arial.ttf', 40)
    font_text = ImageFont.truetype('arial.ttf', 20)
    
    # Adicionar texto ao certificado
    draw.text((150, 200), nome, fill="yellow", font=font_title)
    draw.text((150, 250), modalidade, fill="yellow", font=font_text)
    draw.text((150, 300), f"Tempo: {tempo}", fill="yellow", font=font_text)
    draw.text((150, 350), f"Posição na Categoria: {categoria_pos}", fill="yellow", font=font_text)
    draw.text((150, 400), f"Posição Geral: {geral_pos}", fill="yellow", font=font_text)
    draw.text((150, 450), f"Ritmo Médio: {ritmo}", fill="yellow", font=font_text)
    
    # Salvar certificado em um buffer
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    
    return buffer

# Selecionar participante para gerar certificado
nome = st.sidebar.selectbox("Selecione o participante para o certificado", filtered_data['Nome do Atleta'].unique())

# Botão para gerar certificado
if st.sidebar.button("Gerar Certificado"):
    participante = filtered_data[filtered_data['Nome do Atleta'] == nome].iloc[0]
    tempo_formatado = str(participante['Tempo decorrido']).split()[-1] if pd.notna(participante['Tempo decorrido']) else "Tempo inválido"
    buffer = gerar_certificado(participante['Nome do Atleta'], tempo_formatado, participante['Classificação'], "66/200", "1:58/100m", modalidade)
    
    # Simular navegação para uma nova página com parâmetros
    st.experimental_set_query_params(certificado=True, nome=nome)
    
    st.success(f"Certificado gerado para {nome}!")
    st.image(buffer, caption=f"Certificado de {nome}")

# Exibir certificado se o parâmetro estiver presente
query_params = st.experimental_get_query_params()
if "certificado" in query_params:
    nome = query_params["nome"][0]
    participante = filtered_data[filtered_data['Nome do Atleta'] == nome].iloc[0]
    tempo_formatado = str(participante['Tempo decorrido']).split()[-1] if pd.notna(participante['Tempo decorrido']) else "Tempo inválido"
    buffer = gerar_certificado(participante['Nome do Atleta'], tempo_formatado, participante['Classificação'], "66/200", "1:58/100m", modalidade)
    
    st.download_button(label="Baixar Certificado", data=buffer, file_name=f'{nome}_certificado.jpg', mime='image/jpeg')

# Estilizar a página
st.markdown("""
    <style>
    .stApp {
        background-color: #15354a;
        color: #fffff;
    }
    .css-1d391kg {
        background-color: #ffcd21;
    }
    .css-1lcbmhc {
        color: #fffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Mostrar tabela com classificação em formato de cards
st.subheader("Classificação")
card_style = """
    <style>
    .card {
        border: 1px solid #666;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        color: #ffffff;
        width: auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .card h4 {
        color: #ffcd21;
    }
    .card-container {
        display: flex;
        flex-wrap: wrap;
        height: 100vdh;
    }
    </style>
    """
st.markdown(card_style, unsafe_allow_html=True)

st.markdown('<div class="card-container">', unsafe_allow_html=True)
for index, row in filtered_data.iterrows():
    tempo_formatado = str(row['Tempo decorrido']).split()[-1] if pd.notna(row['Tempo decorrido']) else "Tempo inválido"
    st.markdown(f"""
    <div class="card">
        <h4>Nome: {row['Nome do Atleta']}</h4>
        <p><strong>Classificação:</strong> {row['Classificação']}</p>
        <p><strong>Categoria:</strong> {row['Categoria']}</p>
        <p><strong>Sexo:</strong> {row['Sexo']}</p>
        <p><strong>Tempo decorrido:</strong> {tempo_formatado}</p>
        <p><strong>Modalidade:</strong> {row['Modalidade']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

