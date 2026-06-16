import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Sismos por Década")

df = pd.read_csv("sismos.csv", delimiter=";")

df["AÑO"] = pd.to_datetime(df["FECHA_UTC"].astype(str), format="%Y%m%d", errors="coerce").dt.year
df["DECADA"] = (df["AÑO"] // 10 * 10)

por_decada = df.groupby("DECADA").size().reset_index(name="Cantidad")
por_decada["Década"] = por_decada["DECADA"].astype(str) + "s"

st.subheader("Sismos por década")
st.dataframe(por_decada[["Década", "Cantidad"]])

st.subheader("Grafico de barras")
fig, ax = plt.subplots()
ax.bar(por_decada["Década"], por_decada["Cantidad"])
ax.set_xlabel("Década")
ax.set_ylabel("Número de sismos")
ax.set_title("Sismos por Década")
plt.xticks(rotation=45)

st.pyplot(fig)