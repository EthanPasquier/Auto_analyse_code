from affichage import affichage
import altair as alt
import sys
from pycparser import c_parser, parse_file, c_ast
import os
import openai
import re
import pandas as pd

os.system("clear")
print(" █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ \n██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██╔════╝██╔══██╗\n███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗█████╗  ██████╔╝\n██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██╔══╝  ██╔══██╗\n██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║███████╗██║  ██║\n╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝")

print("\033[1;34m    -   Lancement du Programme    -\033[1;37m")

# Récupérer le nom du dossier actuel
dirname = os.path.basename(os.getcwd())

openai.api_key = "API_KEY"

def get_imported_libraries(content):
    final = ""
    for line in content.split("\n"):
        if line.startswith("#include") or line.startswith("# include") or line.startswith("import") or line.startswith("from"):
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


def ia_de_num(prompt,nb_tokens=500):
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
        print("traitement de \033[1;31m"+filename+"\033[1;37m est finit")
        if(list_lib in lib):
            continue
        else:
            lib = lib+list_lib

print("Tout les fichiers sont traité")

data = {'Name files': file_names, 'Lines count': file_nbline}
df = pd.DataFrame(data)

# Créer un graphique à colonnes avec Altair
bar_chart = alt.Chart(df).mark_bar().encode(
    y='Name files',
    x='Lines count',
)

question = "resume le text en diagrame simple ascii vertical visuel :\n"+explication
diagrame = ask_gpt_turbo(question)

print("Resumer du contenue en creation")


print("page disponible sur :\033[1;34m http://localhost:8501/")
affichage(dirname,nb_def,number_of_lines,number_mots,number_lettres,file_names,explication,diagrame,bar_chart,lt_fonct,lib)