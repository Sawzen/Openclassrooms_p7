import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plost
import pickle as p
from PIL import Image

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Data
X_test = p.load(open("X_test", 'rb'))

# Row A
a1 = st.columns(1)
a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
