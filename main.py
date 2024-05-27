import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Carregar dados
data = pd.read_excel('Arquivo.xlsm')

# Converter 'Tempo decorrido' para timedelta
data['Tempo decorrido'] = pd.to_timedelta(data['Tempo decorrido'].astype(str))

# Renomear colunas para facilitar o acesso (verifique se a planilha possui exatamente estas colunas)
data.columns = ['Classificação', 'Código', 'Nome do Atleta', 'Categoria', 'Sexo', 'Tempo decorrido', 'Modalidade', 'Imagem do Atleta']

st.title("Trinavy - Simulado de Natação")

# Filtros no sidebar
st.sidebar.image("logobg.png")
modalidade = st.sidebar.selectbox("Modalidade", list(data['Modalidade'].unique()))
categoria = st.sidebar.selectbox("Categoria", ["Todos"] + list(data['Categoria'].unique()))
sexo = st.sidebar.selectbox("Sexo", ["Todos"] + list(data['Sexo'].unique()))

# Aplicar filtros
filtered_data = data.copy()
if modalidade:
    filtered_data = filtered_data[filtered_data['Modalidade'] == modalidade]
if categoria != "Todos":
    filtered_data = filtered_data[filtered_data['Categoria'] == categoria]
if sexo != "Todos":
    filtered_data = filtered_data[filtered_data['Sexo'] == sexo]

# Classificar por tempo decorrido
filtered_data = filtered_data.sort_values('Tempo decorrido')

def gerar_certificado(nome, tempo, categoria_pos, geral_pos, ritmo, modalidade):
    # Carregar imagem de fundo do certificado
    img = Image.open('certificado_base.jpg')
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
        color: #ffffff;
    }
    .css-1d391kg {
        background-color: #ffcd21;
    }
    .css-1lcbmhc {
        color: #ffffff;
    }
    .css-1d391kg {
        width: 350px;
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
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    .card img {
        border-radius: 50%;
        margin-right: 10px;
    }
    .card h4 {
        color: #ffcd21;
    }
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 10px;
    }
    @media (max-width: 600px) {
        .card {
            flex-direction: column;
            align-items: flex-start;
        }
        .card img {
            margin-bottom: 10px;
        }
    }
    </style>
    """
st.markdown(card_style, unsafe_allow_html=True)

st.markdown('<div class="card-container">', unsafe_allow_html=True)
for index, row in filtered_data.iterrows():
    tempo_formatado = str(row['Tempo decorrido']).split()[-1] if pd.notna(row['Tempo decorrido']) else "Tempo inválido"
    image_path = row['Imagem do Atleta']  # Use the image path from the column
    st.markdown(f"""
    <div class="card">
        <img src="{"logobg.png"}" alt="Imagem de {row['Imagem do Atleta']}" width="100" height="100">
        <div>
            <h4>Nome: {row['Nome do Atleta']}</h4>
            <p><strong>Classificação:</strong> {row['Classificação']}</p>
            <p><strong>Categoria:</strong> {row['Categoria']}</p>
            <p><strong>Sexo:</strong> {row['Sexo']}</p>
            <p><strong>Tempo decorrido:</strong> {tempo_formatado}</p>
            <p><strong>Modalidade:</strong> {row['Modalidade']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
