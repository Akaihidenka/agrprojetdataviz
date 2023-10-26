import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.image("./logoProject.jpeg", width=100)
st.markdown("<h1 style='text-align: center; sfont-size: 32px;'>Impacte environnemental de la production alimentaire Française sur l'eau  </h1>", unsafe_allow_html=True)


url = "https://koumoul.com/data-fair/api/v1/datasets/agribalyse-31-synthese/raw"
df = pd.read_csv(url)

# Supprimer les colonnes non nécessaires
colonnes_a_conserver = ['Code AGB', 
                        "Groupe d'aliment",
                        "Sous-groupe d'aliment",
                        'Nom du Produit en Français',
                        'Acidification terrestre et eaux douces',
                        'Eutrophisation eaux douces',
                        'Épuisement des ressources eau'
]

df = df[colonnes_a_conserver]

# Supprimer les doublons
df.drop_duplicates(inplace=True)


# Navigation bar
st.sidebar.image("./StephanieHead.jpeg", width=150, use_column_width='auto')  # Photo
# st.sidebar.markdown("## LI Stephanie M1BIA2")  # Nom Prénom
# st.sidebar.markdown("[Lien vers mon LinkedIn](https://www.linkedin.com/in/stephanie-li-5868031b6)")  # Lien
st.sidebar.markdown("<h1 style='text-align: center; font-size: 32px;'> LI Stephanie M1BIA2 </h1>", 
                    unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; font-size: 32px;'> #dataanalyst2023 </h1>", 
                    unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; font-size: 32px;'><a href='https://www.linkedin.com/in/stephanie-li-5868031b6'> Lien vers mon LinkedIn </a></h1>", 
                    unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; font-size: 32px;'><a href='https://github.com/Akaihidenka'> Lien vers mon GitHub </a></h1>", 
                    unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white; font-size: 32px;'> Analyse de produits </h1>", unsafe_allow_html=True)

# Visualisation de la consommation d'eau par type de produit
st.markdown("<h1 style='text-align: center; font-size: 25px;'>Consommation d'eau par type de produit </h1>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df, 
            x="Groupe d'aliment", 
            y='Épuisement des ressources eau', 
            ax=ax)
plt.xticks(rotation=-45, ha="left")
st.pyplot(fig)

# Filtrer les données pour éliminer les valeurs extrêmes
lower_bound = df['Épuisement des ressources eau'].quantile(0.05)
upper_bound = df['Épuisement des ressources eau'].quantile(0.95)
df = df[(df['Épuisement des ressources eau'] >= lower_bound) 
                & (df['Épuisement des ressources eau'] <= upper_bound)]

st.markdown("""<h1 style='text-align: center; font-size: 25px;'>Consommation moyenne d'eau par groupe d'aliment </h1>""", unsafe_allow_html=True)

# Boxplot pour la consommation d'eau par groupe d'aliment, sans valeurs aberrantes
fig2 = plt.figure(figsize=(12, 6))
sns.boxplot(x="Groupe d'aliment", y='Épuisement des ressources eau', 
            data=df,
            showfliers=False)
plt.title("Consommation moyenne d'eau par groupe d'aliment")
plt.xlabel("Groupe d'aliment")
plt.ylabel("Consommation moyenne d'eau en m3/kg")
plt.xticks(rotation=-45, ha="left")
st.pyplot(fig2)


# 30 premiers produits
top_eau = df.sort_values(by='Épuisement des ressources eau', 
                        ascending=False).head(30)

st.markdown("<h1 style='text-align: center; font-size: 25px;'>Top 30 des produits avec la plus grande consommation d'eau </h1>", unsafe_allow_html=True)

top_30 = [f"{str(nom)} :  {str(score)}"  for nom, score in zip(top_eau['Nom du Produit en Français'].tolist(), top_eau['Épuisement des ressources eau'].to_list())]

for i in range(30):
    st.write(f"{i + 1} {top_30[i]} m3/kg")



st.markdown("<h1 style='text-align: center; font-size: 25px;'>Analyse des groupes d'aliments et leur impact environnemental </h1>", unsafe_allow_html=True)

# Sélection du groupe d'aliment via une liste déroulante
groupes_aliment = df["Groupe d'aliment"].unique()
groupe = st.selectbox('Choisis un groupe d\'aliment', groupes_aliment)

data_subset = df[df["Groupe d'aliment"] == groupe]

sum_data = data_subset.groupby("Sous-groupe d'aliment")[['Épuisement des ressources eau', 
                                                        'Acidification terrestre et eaux douces', 
                                                        'Eutrophisation eaux douces']].sum()

st.markdown("<h1 style='text-align: center; font-size: 25px;'>Répartition pour le groupe d'aliment </h1>", unsafe_allow_html=True)


# Graphique pour 'Épuisement des ressources eau'
fig1, ax1 = plt.subplots(figsize=(12, 6))
sum_data['Épuisement des ressources eau'].plot(kind='bar', ax=ax1, color='blue')
plt.ylabel('Valeur')
plt.xlabel("Sous-groupe d'aliment")
plt.title("Épuisement des ressources eau")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# Graphique pour 'Acidification terrestre et eaux douces'
fig2, ax2 = plt.subplots(figsize=(12, 6))
sum_data['Acidification terrestre et eaux douces'].plot(kind='bar', ax=ax2, color='green')
plt.ylabel('Valeur')
plt.xlabel("Sous-groupe d'aliment")
plt.title("Acidification terrestre et eaux douces")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

# Graphique pour 'Eutrophisation eaux douces'
fig3, ax3 = plt.subplots(figsize=(12, 6))
sum_data['Eutrophisation eaux douces'].plot(kind='bar', ax=ax3, color='red')
plt.ylabel('Valeur')
plt.xlabel("Sous-groupe d'aliment")
plt.title("Eutrophisation eaux douces")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig3)

# Filtres personnalisés
st.markdown("<h1 style='text-align: center; color: white; font-size: 45px;'> Filtres personnalisés </h1>", unsafe_allow_html=True)
sous_groupe = st.selectbox("Choisis un sous-groupe d'aliment", df["Sous-groupe d'aliment"].unique())
df_sous_groupe = df[df["Sous-groupe d'aliment"] == sous_groupe]
produit = st.selectbox('Choisis un produit', df_sous_groupe['Nom du Produit en Français'].unique())

eau_produit = df_sous_groupe[df_sous_groupe['Nom du Produit en Français'] == produit]['Épuisement des ressources eau'].values[0]
text_block = f'''<p style="font-size: 25px;">Consommation d'eau de {produit}: {eau_produit} en m3/kg de produit</p>'''
st.write(text_block, unsafe_allow_html=True)

seuil = 2  
if eau_produit > seuil:
    alternative = df_sous_groupe[df_sous_groupe['Épuisement des ressources eau'] < eau_produit].sort_values(by='Épuisement des ressources eau').head(1)['Nom du Produit en Français'].values[0]
    text_block=f'''<p style="font-size: 25px;">Pour économiser de l'eau, tu pourrais envisager de consommer {alternative} à la place de {produit}!</p>'''
    st.write(text_block, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white; font-size: 45px;'> Comparer </h1>", unsafe_allow_html=True)


groupe = st.selectbox("Choisis un groupe d aliment", 
                    df["Groupe d'aliment"].unique())

# Filtrage du dataframe selon le groupe choisi
df_groupe = df[df["Groupe d'aliment"] == groupe]

produit1 = st.selectbox('Choisis le premier produit',
                        df_groupe['Nom du Produit en Français'].unique())
produit2 = st.selectbox('Choisis le second produit', 
                        df_groupe[df_groupe['Nom du Produit en Français'] != produit1]['Nom du Produit en Français'].unique())

titles = ['Épuisement des ressources eau', 
        'Acidification terrestre et eaux douces', 
        'Eutrophisation eaux douces']

dimensions = [" en m3/kg",
            " en mol H+/kg",
            " en P/kg"]

phrases = ["A titre de comparaison kilo de riz utilise 3 m3 d'eau.",
        "Trop d'ions H+ peu entrainer une acidification du sol. Ce qui peut être toxique",
        "Trop de phosphore peut entrainer l'eutrophisation des cours d'eau, ce qui est néfaste pour les éco-systèmes aquatique."]

data_produit1 = df_groupe[df_groupe['Nom du Produit en Français'] == produit1][titles].values[0]
data_produit2 = df_groupe[df_groupe['Nom du Produit en Français'] == produit2][titles].values[0]

info_to_compare = {
    produit1: [round(val, 4) for val in data_produit1],
    produit2: [round(val, 4) for val in data_produit2]
}

width = 0.15  
positions = [0.3, 0.7]  

for i, title in enumerate(titles):
    fig, ax = plt.subplots()
    
    bar1 = ax.bar(positions[0], info_to_compare[produit1][i], width, label=produit1)
    bar2 = ax.bar(positions[1], info_to_compare[produit2][i], width, label=produit2)
    
   
    ax.set_ylabel(dimensions[i])
    ax.set_title(title)
    ax.set_xticks(positions)
    ax.set_xticklabels([produit1, produit2])
    ax.legend()
    
    max_limit_y = max(info_to_compare[produit1][i], info_to_compare[produit2][i]) * 1.1
    ax.set_ylim(0, max_limit_y)
    
    ax.bar_label(bar1, padding=3)
    ax.bar_label(bar2, padding=3)
    
    st.pyplot(fig)
    st.write(phrases[i], '\n ')
