import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://koumoul.com/data-fair/api/v1/datasets/agribalyse-31-synthese/raw"
st.title("Visualisation initiale du dataset Agribalyse_Synthese")
df = pd.read_csv(url)

# Supprimer les colonnes non nécessaires
colonnes_a_conserver = [
    'Code AGB', 'Groupe d\'aliment','Sous-groupe d\'aliment',
    'Nom du Produit en Français','Acidification terrestre et eaux douces','Eutrophisation eaux douces','Épuisement des ressources eau'
]
df = df[colonnes_a_conserver]

# Supprimer les doublons
df.drop_duplicates(inplace=True)

# Visualisation de la consommation d'eau par type de produit
st.title("Consommation d'eau par type de produit")
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df, x='Groupe d\'aliment', y='Épuisement des ressources eau', ax=ax)
st.pyplot(fig)

# Filtrer les données pour éliminer les valeurs extrêmes
lower_bound = df['Épuisement des ressources eau'].quantile(0.05)
upper_bound = df['Épuisement des ressources eau'].quantile(0.95)
filtered_data = df[(df['Épuisement des ressources eau'] >= lower_bound) & (df['Épuisement des ressources eau'] <= upper_bound)]

# Tracer l'histogramme
plt.figure(figsize=(8, 6))
sns.histplot(filtered_data['Épuisement des ressources eau'], kde=True)
plt.title("Distribution zoomée de la consommation d'eau")
plt.xlabel("Consommation d'eau")
plt.ylabel("Nombre de produits")
plt.show()

# Boxplot pour la consommation d'eau par groupe d'aliment, sans valeurs aberrantes
plt.figure(figsize=(12, 6))
sns.boxplot(x='Groupe d\'aliment', y='Épuisement des ressources eau', data=df, showfliers=False)
plt.title("Consommation moyenne d'eau par groupe d'aliment")
plt.xlabel("Groupe d'aliment")
plt.ylabel("Consommation moyenne d'eau")
plt.xticks(rotation=45)
plt.show()

# ... (les autres visualisations et analyses)

# Tri du DataFrame en fonction de l'épuisement des ressources d'eau et prise des 30 premiers produits
top_eau = df.sort_values(by='Épuisement des ressources eau', ascending=False).head(30)

# Affichage des 'Nom du Produit en Français' de ces produits
st.title("Top 30 des produits avec la plus grande consommation d'eau")
st.write(top_eau['Nom du Produit en Français'].tolist())



#2. Filtres personnalisés


# Widget pour choisir un sous-groupe d'aliment
sous_groupe = st.selectbox('Choisis un sous-groupe d\'aliment', df2['Sous-groupe d\'aliment'].unique())

# Filtrage du dataframe selon le sous-groupe choisi
df_sous_groupe = df2[df2['Sous-groupe d\'aliment'] == sous_groupe]

# Widget pour choisir un 'nom de produit en français'
produit = st.selectbox('Choisis un produit', df_sous_groupe['Nom du Produit en Français'].unique())

# Affichage de la consommation d'eau du produit choisi
eau_produit = df_sous_groupe[df_sous_groupe['Nom du Produit en Français'] == produit]['Épuisement des ressources eau'].values[0]
st.write(f"Consommation d'eau de {produit}: {eau_produit}")

# Si le produit choisi utilise trop d'eau (ici, je prends un seuil arbitraire, tu peux le changer)
seuil = 100  # Remplace cette valeur par le seuil que tu juges approprié
if eau_produit > seuil:
    # Trouver un autre produit du même sous-groupe qui utilise moins d'eau
    alternative = df_sous_groupe[df_sous_groupe['Épuisement des ressources eau'] < eau_produit].sort_values(by='Épuisement des ressources eau').head(1)['Nom du Produit en Français'].values[0]
    st.write(f"Pour économiser de l'eau, tu pourrais envisager de consommer {alternative} à la place de {produit}!")


#comparer 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Widget pour choisir un groupe d'aliment
groupe = st.selectbox('Choisis un groupe d\'aliment', df2['Groupe d\'aliment'].unique())

# Filtrage du dataframe selon le groupe choisi
df_groupe = df2[df2['Groupe d\'aliment'] == groupe]

# Widgets pour choisir deux produits
produit1 = st.selectbox('Choisis le premier produit', df_groupe['Nom du Produit en Français'].unique())
produit2 = st.selectbox('Choisis le second produit', df_groupe[df_groupe['Nom du Produit en Français'] != produit1]['Nom du Produit en Français'].unique())

# Extraction des données des produits choisis
data_produit1 = df_groupe[df_groupe['Nom du Produit en Français'] == produit1][['Épuisement des ressources eau', 'Acidification terrestre et eaux douces', 'Eutrophisation eaux douces']].values[0]
data_produit2 = df_groupe[df_groupe['Nom du Produit en Français'] == produit2][['Épuisement des ressources eau', 'Acidification terrestre et eaux douces', 'Eutrophisation eaux douces']].values[0]

# Affichage des comparaisons
labels = ['Épuisement des ressources eau', 'Acidification terrestre et eaux douces', 'Eutrophisation eaux douces']

x = range(len(labels))
plt.bar(x, data_produit1, width=0.4, label=produit1, color='b', align='center')
plt.bar(x, data_produit2, width=0.4, label=produit2, color='r', bottom=data_produit1, align='edge')

plt.xlabel('Critères')
plt.ylabel('Valeur')
plt.title('Comparaison des produits')
plt.xticks(x, labels)
plt.legend()
plt.tight_layout()
st.pyplot()

# Conseil sur le produit qui utilise moins d'eau
if data_produit1[0] < data_produit2[0]:
    st.write(f"{produit1} utilise moins d'eau que {produit2}.")
else:
    st.write(f"{produit2} utilise moins d'eau que {produit1}.")
