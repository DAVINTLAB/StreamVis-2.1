import streamlit as st
import pandas as pd
from detoxify import Detoxify
from tqdm import tqdm
from v2.utils.scream_index_calc import calc_scream_index
tqdm.pandas()

@st.cache_resource
def carregar_modelo():
    with st.spinner("Downloading Detoxify model... this can take a few seconds the first time."):
        return Detoxify("multilingual", device="cpu")

@st.cache_data
def classificar(texto, _modelo):
    predicoes = _modelo.predict(texto)
    return {rotulo: float(valor) for rotulo, valor in predicoes.items()}

def classification_page():
    st.title("Toxicity Detection with Detoxify and Scream Index")
    
    if "comments_file" not in st.session_state or not st.session_state.comments_file:
        st.warning('No data uploaded, please upload some data before checking this page')
        return

    #file_name = st.selectbox('Uploaded archives', st.session_state.comments_file.keys())
    dfComentarios = pd.DataFrame(st.session_state['comments_file'])

    # Remove colunas de toxicidade se já existirem
    cols_to_drop = ['toxicity', 'severe_toxicity', 'obscene', 'identity_attack',
                'insult', 'threat', 'sexual_explicit']
    dfComentarios = dfComentarios.drop(columns=[c for c in cols_to_drop if c in dfComentarios], errors="ignore")


    modelo = carregar_modelo() 
    if st.button("Run Classification"):
        with st.spinner("Analysing toxicity..."):
            seriePredicoes = dfComentarios["message"].progress_apply(lambda msg: classificar(msg, modelo))
            # Converte para DataFrame e concatena aos comentários originais
            dfPredicoes = pd.json_normalize(seriePredicoes)
            dfFinal = pd.concat([dfComentarios, dfPredicoes], axis=1)
            
            # Adiciona o scream index
            dfFinal['scream_index'] = dfFinal['message'].apply(calc_scream_index)
            st.success("Analysis finished!")

        json_resultado = dfFinal.to_json(orient="records", force_ascii=False, indent=2)
        st.session_state['comments_file'] = dfFinal.to_dict(orient="records")
        
        st.download_button(
            label="Download result as JSON",
            data=json_resultado,
            file_name="resultado_toxicidade.json",
            mime="application/json"
        )