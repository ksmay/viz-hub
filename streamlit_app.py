import time

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
import yaml

########### login
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login("Login", "main")
print(name, authentication_status, username)

if authentication_status:
    #st.set_page_config(layout='wide')
    st.header("Rechnung Analyse")

    ## Data
    df = pd.read_csv("test.csv", sep=";")
    # st.dataframe(df)

    "---"
    fig = px.line(x=df["KW"], y=df["Rechnungen"], line_shape="spline")

    fig.add_bar(x=df["KW"], y=df["Ges. Umsatz"])
    fig.add_bar(x=df["KW"], y=df["Ges. RE-Betrag"])
    fig.add_bar(x=df["KW"], y=df["Ges. Erstattungsbetrag"])

    st.plotly_chart(fig)

    # with st.spinner("Report updated!"):
    #     time.sleep(1)

    authenticator.logout("Logout", "main")
    
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
