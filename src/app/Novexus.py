import pandas as pd
import numpy as np
import streamlit as st
import requests
import pickle

# image_head = "data/interim/images/Logo (5).png"
# st.image(image_head)  
model_dir = 'models/model_random_forest_novexus_churn.pkl'
scaler_dir = 'models/scaler_random_forest_novexus_churn.pkl'

with open(model_dir, 'rb') as f:
    model = pickle.load(f)

with open(scaler_dir, 'rb') as f:
    scaler = pickle.load(f)

# Título com emoji
# st.title( "📞Previsão de Churn📞")

# Configurando o layout para centralizar conteúdo
st.write("""
    <div style="display: flex; justify-content: center;">
        <h1>📞Previsão de Churn📞</h1>
    </div>
""", unsafe_allow_html=True)

# Aqui você pode adicionar o restante do seu conteúdo


with st.form("my_form"):
# Adicione widgets para os campos de entrada
    contrato_ativo = int(st.number_input("Contrato Ativo (em meses): ", min_value=0))
    valor_mensal = st.number_input("Valor Mensal: ", min_value=0.0)
    valor_total = st.number_input("Valor Total: ", min_value=0.0)
    idoso = st.radio("Maior de 65 anos:", ["Sim", "Não"], horizontal=True)
    genero = st.radio("Selecione o sexo:", ["Masculino", "Feminino"], horizontal=True)
    conjuge = st.radio("Possui conjugue:", ["Sim", "Não"], horizontal=True)
    dependentes = st.radio("Possui dependentes:", ["Sim", "Não"], horizontal=True)
    servico_telefone = st.radio("Possui serviço telefonico:", ["Sim", "Não"], horizontal=True)
    mult_linhas = st.radio("Possui mais de uma linha:", ["Sim", "Não"], horizontal=True)
    fibra_otica = st.radio("Possui fibra Otica:", ["Sim", "Não"], horizontal=True)
    internet = st.radio("Possui internet:", ["Sim", "Não"], horizontal=True)
    security_online = st.radio("Possui segurança online:", ["Sim", "Não"], horizontal=True)
    backup = st.radio("Possui backup:", ["Sim", "Não"], horizontal=True)
    protecao_disp = st.radio("Possui proteção dispositivo:", ["Sim", "Não"], horizontal=True)
    suporte = st.radio("Possui suporte tecnico:", ["Sim", "Não"], horizontal=True)
    streamTV = st.radio("Possui stream TV:", ["Sim", "Não"], horizontal=True)
    stream_filmes = st.radio("Possui stream Filmes:", ["Sim", "Não"], horizontal=True)
    contrato = st.radio("Escolha o tipo de contrato:", ["Contrato de Dois Anos", "Contrato Mensal"], horizontal=True)
    tipo_fatura = st.radio('Qual o tipo de Fatura:',
                            ['Fatura Online', 'Boleto', 'Eletronico', 'Transferência Automatica'], horizontal=True)


    # Atribua 1 ou 0 com base na escolha do contrato
    if contrato == "Contrato de Dois Anos":
        Contrato_Dois = 1
        Contrato_Mensal = 0
    else:
        Contrato_Dois = 0
        Contrato_Mensal = 1

    if tipo_fatura == 'Fatura Online':
        fatura_online = 1
        forma_pagamento_correio = 0
        pagamento_eletronico = 0
        transferencia_aut = 0

    if tipo_fatura == 'Boleto':
        fatura_online = 0
        forma_pagamento_correio = 1
        pagamento_eletronico = 0
        transferencia_aut = 0

    if tipo_fatura == 'Eletronico':
        fatura_online = 0
        forma_pagamento_correio = 0
        pagamento_eletronico = 1
        transferencia_aut = 0

    if tipo_fatura == 'Transferência Automatica':
        fatura_online = 0
        forma_pagamento_correio = 0
        pagamento_eletronico = 0
        transferencia_aut = 1


    # Botão para fazer a previsão
    submitted = st.form_submit_button("Obter Previsão")
    if  submitted:
        # Processar os valores dos campos de entrada (você pode mapear "Sim" para 1 e "Não" para 0)
        idoso_encoded = 1 if idoso == "Sim" else 0
        conjuge_encoded = 1 if conjuge == "Sim" else 0
        dependentes_encoded = 1 if dependentes == "Sim" else 0
        genero_encoded = 1 if genero == 'Feminio' else 0
        servico_telefone_encoded = 1 if servico_telefone == "Sim" else 0
        mult_linhas_encoded = 1 if mult_linhas == "Sim" else 0
        fibra_otica_encoded = 1 if fibra_otica == "Sim" else 0
        internet_encoded = 1 if internet == "Sim" else 0
        security_online_encoded = 1 if security_online == "Sim" else 0
        backup_encoded = 1 if backup == "Sim" else 0
        protecao_disp_encoded = 1 if protecao_disp == "Sim" else 0
        suporte_encoded = 1 if suporte == "Sim" else 0
        streamTV_encoded = 1 if streamTV == "Sim" else 0
        stream_filmes_encoded = 1 if stream_filmes == "Sim" else 0
        # tipo_fatura_encoded = 1 if tipo_fatura == 'Fatura Online' else 0
        

        input_data = np.array([[idoso_encoded, contrato_ativo, valor_mensal, valor_total, genero_encoded, conjuge_encoded, 
                                dependentes_encoded, servico_telefone_encoded, mult_linhas_encoded, fibra_otica_encoded,
                                internet_encoded, security_online_encoded, backup_encoded, protecao_disp_encoded,
                                suporte_encoded, streamTV_encoded, stream_filmes_encoded, Contrato_Dois, Contrato_Mensal,
                                fatura_online, forma_pagamento_correio,pagamento_eletronico, transferencia_aut]])


        input_scaled = scaler.transform(input_data, )
        prediction = model.predict(input_data)

        # Exibir o resultado da previsão
        if prediction == 0:
            result = "Cliente provavelmente NÃO vai cancelar o serviço."
        else:
            result = "Cliente provavelmente vai CANCELAR o serviço."

        st.subheader("Resultado da Previsão:")
        if prediction == 0:
            st.markdown(f"<p style='color:green;'>{result}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:red;'>{result}</p>", unsafe_allow_html=True)

