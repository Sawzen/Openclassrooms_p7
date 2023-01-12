import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plost
import time
import pickle as p
from PIL import Image
import plotly.express as px 
import altair as alt


# Page setting
st.set_page_config(layout="wide")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

X_test = p.load(open("X_test", 'rb'))
ID_client_liste = list(X_test["SK_ID_CURR"])
best_tresh = 0.44

# Title 
st.title('Bienvenue sur Prêt à dépenser :smile:')

# Row A
ID_client = st.selectbox('Séléctionner votre numéro client : ',pd.unique(X_test["SK_ID_CURR"]),label_visibility  = "collapsed")

#Row B
st.markdown("""
<style>
.big-font {
    font-size:600;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">Voici quelques informations vous concernant :</p>', unsafe_allow_html=True)

# Data client
data_client = X_test[X_test["SK_ID_CURR"]== ID_client]

if data_client["CODE_GENDER"].values[0] == 0:
    data_client["Genre"] = "Homme"
if data_client["CODE_GENDER"].values[0] == 1:
    data_client["Genre"] = "Femme"

if data_client["FLAG_OWN_CAR"].values[0] == 0:
    data_client["Dispose d'une voiture"] = "Non"
if data_client["FLAG_OWN_CAR"].values[0] == 1:
    data_client["Dispose d'une voiture"] = "Oui"

if data_client["TARGET"].values[0] == 0:
    data_client["Réponse crédit"] = "Crédit refusé"
if data_client["TARGET"].values[0] == 1:
    data_client["Réponse crédit"] = "Crédit accordé"


# Row B
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
if data_client["Genre"].values[0] == 0:
    kpi1.metric(label="Genre :man:", value = str(data_client["Genre"].values[0]))
else :
    kpi1.metric(label="Genre :woman:", value = str(data_client["Genre"].values[0]))

#kpi2.metric(label = "Age :birthday: ", value = int(data_client["DAYS_BIRTH"].values[0] ))
kpi2.metric(label ="Dispose d'une voiture :car:", value = str(data_client["Dispose d'une voiture"].values[0]))
kpi3.metric(label ="Nombre d'enfant :family:", value = int(data_client["CNT_CHILDREN"].values[0]))
if data_client["Réponse crédit"].values[0] == 0:
    kpi4.metric(label ="Réponse crédit :white_check_mark:", value = str(data_client["Réponse crédit"].values[0]))
else :
    kpi4.metric(label ="Réponse crédit :x:", value = str(data_client["Réponse crédit"].values[0]))


# Row C 
plot_bgcolor = "lightgrey"
quadrant_colors = [plot_bgcolor, "#f25829", "#f2a529", "#85e043", "#2bad4e"] 
quadrant_text = ["", "<b>Très bas</b>", "<b>bas</b>", "<b>Elevé</b>", "<b>Très élevé</b>"]
n_quadrants = len(quadrant_colors) - 1

min_value = 0
max_value = 1
hand_length = np.sqrt(2) / 4
hand_angle = np.pi * (1 - (max(min_value, min(max_value, best_tresh)) - min_value) / (max_value - min_value))

fig1 = go.Figure(
    data=[
        go.Pie(
            values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
            rotation=90,
            hole=0.5,
            marker_colors=quadrant_colors,
            text=quadrant_text,
            textinfo="text",
            hoverinfo="skip",
        ),
    ],
    layout=go.Layout(
        showlegend=False,
        margin=dict(b=0,t=10,l=10,r=10),
        width=450,
        height=450,
        paper_bgcolor=plot_bgcolor,
        annotations=[
            go.layout.Annotation(
                text=f"<b>Votre score de crédit :</b><br>{best_tresh}",
                x=0.5, xanchor="center", xref="paper", 
                y=0.25, yanchor="bottom", yref="paper", 
                showarrow=False, 
            )
        ],
        shapes=[
            go.layout.Shape(
                type="circle",
                x0=0.48, x1=0.52,
                y0=0.48, y1=0.52,
                fillcolor="#333",
                line_color="#333",
            ),
            go.layout.Shape(
                type="line",
                x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                line=dict(color="#333", width=4)
            )
        ]
    )
)
st.plotly_chart(fig1)

#if st.checkbox("Vous avez besoin de plus de précisions ?") :
options = st.multiselect('Veuillez séléctionner les informations qui vous intéressent :',
    ['INCOME_PER_PERSON', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_GOODS_PRICE', 'INCOME_CREDIT_PERC', 
    'EXT_SOURCE_2', 'CNT_FAM_MEMBERS'])
#if options :
fig2 = px.box(options)
fig2.update_yaxes(type='log')
st.plotly_chart(fig2)

