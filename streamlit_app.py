import streamlit as st
import requests
import flask
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import pickle as p
import plotly.express as px 
import altair as alt
from plotly.subplots import make_subplots

# Page setting
st.set_page_config(layout="wide")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

X_test = p.load(open("X_test", 'rb'))
best_thresh = p.load(open("best_thresh", 'rb'))
data_thresh = p.load(open("data_thresh", 'rb'))

# Title 
st.title('Bienvenue sur Prêt à dépenser :smile:')

# Row A
#ID_client = st.selectbox('Séléctionner votre numéro client : ',pd.unique(X_test["SK_ID_CURR"]),label_visibility  = "collapsed")
ID_client = st.multiselect('Veuillez entrer votre numéro client: ',pd.unique(X_test["SK_ID_CURR"]), max_selections = 1)


if ID_client :
    # Data client
    ID_client = ID_client[0]
    data_client = X_test[X_test["SK_ID_CURR"] == ID_client]
    df = data_thresh[data_thresh["SK_ID_CURR"] == ID_client]
    thresh_client = df["thresh"].values[0]

    #Row B
    st.markdown('Voici quelques informations vous concernant :', unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    if data_client["CODE_GENDER"].values[0] == 0:
        kpi1.metric(label="Genre :man:", value = str("Homme"))
    if data_client["CODE_GENDER"].values[0] == 1:
        kpi1.metric(label="Genre :woman:", value = str("Femme"))
    
    if data_client["FLAG_OWN_CAR"].values[0] == 0:
        kpi2.metric(label="Genre :car:", value = str("Oui"))
    if data_client["FLAG_OWN_CAR"].values[0] == 1:
        kpi2.metric(label="Genre :car:", value = str("Non"))

    kpi3.metric(label ="Nombre d'enfant :family:", value = int(data_client["CNT_CHILDREN"].values[0]))

    kpi4.metric(label ="Revenu annuel :heavy_dollar_sign:", value = int(data_client["AMT_ANNUITY"].values[0]))


    # Row C 
    col1, col2 = st.columns(2)
    with col1:
        plot_bgcolor = "lightgrey"
        quadrant_colors = [plot_bgcolor, "#f25829", "#f2a529", "#85e043", "#2bad4e"] 
        quadrant_text = ["", "<b>Très bas</b>", "<b>bas</b>", "<b>Elevé</b>", "<b>Très élevé</b>"]
        n_quadrants = len(quadrant_colors) - 1

        min_value = 0
        max_value = 1
        hand_length = np.sqrt(2) / 4
        hand_angle = np.pi * (1 - (max(min_value, min(max_value, thresh_client)) - min_value) / (max_value - min_value))

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
                        text=f"<b>Votre score de crédit :</b><br>{thresh_client}",
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


    with col2:
        if thresh_client <= best_thresh:
            st.subheader("D'après les informations que nous disposons, votre situation vous autorise un crédit :white_check_mark:.")
        
        if thresh_client > best_thresh:
            st.subheader("D'après les informations que nous disposons, votre situation ne vous autorise pas de crédit :x:.")
            st.subheader("Ci-dessous sont affichés les paramètres pour lequels le crédit est refusé.")

#Last row
    if st.checkbox("Vous avez besoin de plus de précisions ?") :
            options1 = st.multiselect('Veuillez séléctionner les informations qui vous intéressent :',
                ['INCOME_PER_PERSON', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_GOODS_PRICE'])
            if options1:
                fig2 = px.box(X_test[options1], notched = True, width=450, points =None)
                fig3 = px.scatter(data_client[options1])
                fig4 = go.Figure(data=fig2.data + fig3.data)
                fig4.update_yaxes(type='log')
                st.plotly_chart(fig4)



