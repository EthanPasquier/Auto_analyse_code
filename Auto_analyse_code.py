import sys
from pycparser import c_parser, parse_file, c_ast
import os
import openai
import streamlit as st
import re
import altair as alt
import pandas as pd


# Récupérer le nom du dossier actuel
dirname = os.path.basename(os.getcwd())

openai.api_key = "API_KEY"

def get_imported_libraries(content):
    final = ""
    for line in content.split("\n"):
        if line.startswith("#include") or line.startswith("# include") or line.startswith("import") or line.startswith("from"):
            print(line)
            final += line + "\n"
    return final

def ask_gpt_turbo(question,nb_tokens=500):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=nb_tokens, 
        messages=[
            {"role": "user", "content": question},
            ]
        )
    return response.choices[0].message.content


def ia_de_num(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text

file_names = []
file_contents = []
file_nbline = []
number_of_lines = 0
number_mots = 0
number_lettres = 0
lt_fonct = []
nb_def = 0
satisfaction = 0
lib = ""
explication = ""

for filename in os.listdir("."):
    if os.path.isfile(filename):
        if filename == "Auto_analyse_code":
            continue
        file_names.append(filename)
        with open(filename, 'r') as f:
            contents = f.read()
        file_contents.append(contents)
        number_of_lines += contents.count('\n') + 1
        file_nbline.append(contents.count('\n') + 1)
        number_mots += contents.count(' ') + 1
        number_lettres += len(contents) + 1
        # Compter les fonctions Python
        if filename.endswith('.py'):
            function_pattern = r'^\s*def\s+\w+\s*\('
        # Compter les fonctions JavaScript
        elif filename.endswith('.js'):
            function_pattern = r'^\s*function\s+\w+\s*\('
        # Compter les fonctions C
        elif filename.endswith('.c'):
            function_pattern = r'^\w+\s+\w+\s*\([^)]*\)\s*\{'
        # Compter les fonctions PHP
        elif filename.endswith('.php'):
            function_pattern = r'^\s*function\s+\w+\s*\('
        # Compter les fonctions SQL (ne compte que les fonctions définies avec 'CREATE FUNCTION')
        elif filename.endswith('.sql'):
            function_pattern = r'^\s*CREATE\s+FUNCTION\s+\w+'
        functions = re.findall(function_pattern, contents, re.MULTILINE)
        nb_def += len(functions)
        list_lib = get_imported_libraries(contents)
        question = "explique en une ligne le fonctionnement du code suivant["+filename+"]:\n"+contents
        resume = ask_gpt_turbo(question)
        explication = explication+"\n"+resume
        resume = filename+" : "+resume
        lt_fonct.append(resume)
        # st.markdown("<h3 style='color: green;'>fonctionnement de "+filename+" :</h3>", unsafe_allow_html=True)
        # st.write(resume)
        if(list_lib in lib):
            continue
        else:
            lib = lib+list_lib

print(file_names)     

data = {'Name files': file_names, 'Lines count': file_nbline}
df = pd.DataFrame(data)

# Créer un graphique à colonnes avec Altair
bar_chart = alt.Chart(df).mark_bar().encode(
    y='Name files',
    x='Lines count',
)

# explication = ask_gpt_turbo(question)
# question = "resume le text en diagrame ascii vertical :\n"+explication

question = "resume le text en diagrame ascii vertical :\n"+explication
diagrame = ask_gpt_turbo(question)

question = "a quoi sert le code ? :\n"+explication
explication = ia_de_num(question)

def main():
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

if __name__ == "__main__":
    main()
