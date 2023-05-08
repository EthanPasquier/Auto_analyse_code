import streamlit as st

def affichage(dirname,nb_def,number_of_lines,number_mots,number_lettres,file_names,explication,diagrame,bar_chart,lt_fonct,lib):
    print("\033[1;34mPage Fonctionnel")
    titre = ("Analyse du code de " + dirname)
    st.markdown("<h1 style='color: red;'>"+titre+"</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: red;'>\nNombre de fonction : "+str(nb_def)+"</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='white: purple;'> - Nombre de lignes total = "+str(number_of_lines)+"</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='white: purple;'> - Nombre de mots total = "+str(number_mots)+"</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='white: purple;'> - Nombre de lettres total = "+str(number_lettres)+"</h4>", unsafe_allow_html=True)
    st.markdown("<h2 style='white: red;'>Les libraries :</h2>", unsafe_allow_html=True)
    st.code(lib, language='python')
    st.title("les grandes lignes de "+dirname)
    st.markdown("<h2 style='white: red;'>Explication du projet :</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: green;'>les fichier present dans le repo : \n"+str(file_names)+"\n</p>", unsafe_allow_html=True)
    st.write(explication)
    st.markdown("<h2 style='white: red;'>Diagrame de fonctionnement :</h2>", unsafe_allow_html=True)
    st.code(diagrame, language='python')
    st.markdown("<h2 style='white: red;'>Comparatifs de lignes par fichiers :</h2>", unsafe_allow_html=True)
    st.altair_chart(bar_chart, use_container_width=True)
    st.markdown("<h2 style='white: red;'> Explication par fichier : </h2>", unsafe_allow_html=True)
    for func in lt_fonct:
        st.markdown("<h4 style='white: red;'>"+func+"\n</h4>", unsafe_allow_html=True)
