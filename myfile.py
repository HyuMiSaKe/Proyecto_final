import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Sismos en Perú")
df = pd.read_csv("sismos.csv", delimiter=";")

df["AÑO"] = pd.to_datetime(
    df["FECHA_UTC"].astype(str),
    format="%Y%m%d",
    errors="coerce"
).dt.year

df["DECADA"] = (df["AÑO"] // 10) * 10

def preparar_mapa(dataframe):
    return dataframe[["LATITUD", "LONGITUD"]].dropna().rename(
        columns={"LATITUD": "lat", "LONGITUD": "lon"}
    )

# --- Diccionarios de rangos reutilizables ---
RANGOS_MAG = {
    "[0, 2)":  lambda d: d[d["MAGNITUD"] < 2],
    "[2, 3)":  lambda d: d[(d["MAGNITUD"] >= 2) & (d["MAGNITUD"] < 3)],
    "[3, 4)":  lambda d: d[(d["MAGNITUD"] >= 3) & (d["MAGNITUD"] < 4)],
    "[4, 5)":  lambda d: d[(d["MAGNITUD"] >= 4) & (d["MAGNITUD"] < 5)],
    "[5, 6)":  lambda d: d[(d["MAGNITUD"] >= 5) & (d["MAGNITUD"] < 6)],
    "[6, >)":  lambda d: d[d["MAGNITUD"] >= 6],
}

RANGOS_PROF = {
    "[0, 200)":   lambda d: d[d["PROFUNDIDAD"] < 200],
    "[200, 300)": lambda d: d[(d["PROFUNDIDAD"] >= 200) & (d["PROFUNDIDAD"] < 300)],
    "[300, 400)": lambda d: d[(d["PROFUNDIDAD"] >= 300) & (d["PROFUNDIDAD"] < 400)],
    "[400, >)":   lambda d: d[d["PROFUNDIDAD"] >= 400],
}


tab_todos, tab_richter, tab_prof, tab_decada, tab_richypro = st.tabs([
    "Todos los sismos",
    "Según la Escala de Richter",
    "Según la Profundidad",
    "Según la Década",
    "Richter y Profundidad"
])

with tab_todos:
    st.subheader("Todos los sismos registrados")
    st.caption(f"Total: {len(df):,} sismos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sismos por década**")
        por_decada = df.groupby("DECADA").size().reset_index(name="Cantidad")
        por_decada["Década"] = por_decada["DECADA"].astype(int).astype(str) + "s"
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(por_decada["Década"], por_decada["Cantidad"], marker="o", color="#E63946", linewidth=2)
        ax.set_xlabel("Décadas")
        ax.set_ylabel("Cantidad")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        st.pyplot(fig)

    with col2:
        st.markdown("**Mapa de sismos**")
        st.map(preparar_mapa(df), zoom=3)


with tab_richter:
    st.subheader("Filtrar por Escala de Richter")

    intervalo = st.selectbox(
        "Selecciona un rango de magnitud:",
        list(RANGOS_MAG.keys()),
        key="richter"
    )

    df_r = RANGOS_MAG[intervalo](df)
    st.caption(f"{len(df_r):,} sismos en el rango {intervalo}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sismos por década**")
        por_decada = df_r.groupby("DECADA").size().reset_index(name="Cantidad")
        por_decada["Década"] = por_decada["DECADA"].astype(int).astype(str) + "s"
        if not por_decada.empty:
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(por_decada["Década"], por_decada["Cantidad"], marker="o", color="#457B9D", linewidth=2)
            ax.set_xlabel("Décadas")
            ax.set_ylabel("Cantidad")
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            st.pyplot(fig)
        else:
            st.warning("Sin datos para este rango.")

    with col2:
        st.markdown("**Mapa de sismos**")
        mapa = preparar_mapa(df_r)
        if not mapa.empty:
            st.map(mapa, zoom=3)
        else:
            st.warning("Sin coordenadas para mostrar.")


with tab_prof:
    st.subheader("Filtrar por Profundidad")

    profundidad = st.selectbox(
        "Selecciona un rango de profundidad (km):",
        list(RANGOS_PROF.keys()),
        key="profundidad"
    )

    df_p = RANGOS_PROF[profundidad](df)
    st.caption(f"{len(df_p):,} sismos con profundidad {profundidad} km")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sismos por década**")
        por_decada = df_p.groupby("DECADA").size().reset_index(name="Cantidad")
        por_decada["Década"] = por_decada["DECADA"].astype(int).astype(str) + "s"
        if not por_decada.empty:
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(por_decada["Década"], por_decada["Cantidad"], marker="o", color="#2A9D8F", linewidth=2)
            ax.set_xlabel("Décadas")
            ax.set_ylabel("Cantidad")
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            st.pyplot(fig)
        else:
            st.warning("Sin datos para este rango.")

    with col2:
        st.markdown("**Mapa de sismos**")
        mapa = preparar_mapa(df_p)
        if not mapa.empty:
            st.map(mapa, zoom=3)
        else:
            st.warning("Sin coordenadas para mostrar.")


with tab_decada:
    st.subheader("Filtrar por Década")

    decadas_disponibles = sorted(df["DECADA"].dropna().unique().astype(int))
    decada_sel = st.selectbox(
        "Selecciona una década:",
        [str(d) + "s" for d in decadas_disponibles],
        key="decada"
    )

    dec_num = int(decada_sel.replace("s", ""))
    df_d = df[df["DECADA"] == dec_num]

    st.caption(f"{len(df_d):,} sismos en la década {decada_sel}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sismos por magnitud**")
        bins = [0, 2, 3, 4, 5, 6, 10]
        labels = ["[0,2)", "[2,3)", "[3,4)", "[4,5)", "[5,6)", "[6,>)"]
        df_d = df_d.copy()
        df_d["RANGO_MAG"] = pd.cut(df_d["MAGNITUD"], bins=bins, labels=labels, right=False)
        por_mag = df_d["RANGO_MAG"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(por_mag.index.astype(str), por_mag.values, color="#E9C46A")
        ax.set_xlabel("Magnitud")
        ax.set_ylabel("Cantidad")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        st.pyplot(fig)

    with col2:
        st.markdown("**Mapa de sismos**")
        mapa = preparar_mapa(df_d)
        if not mapa.empty:
            st.map(mapa, zoom=3)
        else:
            st.warning("Sin coordenadas para mostrar.")


with tab_richypro:
    st.subheader("Filtrar por Richter y Profundidad")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        mag_sel = st.multiselect(
            "Rango de magnitud:",
            list(RANGOS_MAG.keys()),
            default=list(RANGOS_MAG.keys())[:1],
            key="combo_mag"
        )

    with col_f2:
        prof_sel = st.multiselect(
            "Rango de profundidad (km):",
            list(RANGOS_PROF.keys()),
            default=list(RANGOS_PROF.keys())[:1],
            key="combo_prof"
        )

    if not mag_sel or not prof_sel:
        st.warning("Selecciona al menos un rango de magnitud y uno de profundidad.")
    else:
        df_mag = pd.concat(
            [RANGOS_MAG[m](df) for m in mag_sel]
        ).drop_duplicates()

        df_combo = pd.concat(
            [RANGOS_PROF[p](df_mag) for p in prof_sel]
        ).drop_duplicates()

        total = len(df_combo)
        mag_labels  = ", ".join(mag_sel)
        prof_labels = ", ".join(prof_sel)

        if total == 0:
            st.warning("No hay sismos que cumplan ambos criterios.")
        else:
            st.success(
                f"{total:,} sismos con magnitud [{mag_labels}] y profundidad [{prof_labels}]"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Sismos por década**")
                por_decada = df_combo.groupby("DECADA").size().reset_index(name="Cantidad")
                por_decada["Década"] = por_decada["DECADA"].astype(int).astype(str) + "s"

                if not por_decada.empty:
                    fig, ax = plt.subplots(figsize=(5, 3))
                    ax.plot(
                        por_decada["Década"],
                        por_decada["Cantidad"],
                        marker="o",
                        color="#86F461",
                        linewidth=2
                    )
                    ax.set_xlabel("Décadas")
                    ax.set_ylabel("Cantidad")
                    ax.tick_params(axis="x", rotation=45)
                    ax.grid(axis="y", linestyle="--", alpha=0.4)
                    st.pyplot(fig)
                else:
                    st.warning("Sin datos para graficar.")

            with col2:
                st.markdown("**Mapa de sismos**")
                mapa = preparar_mapa(df_combo)
                if not mapa.empty:
                    st.map(mapa, zoom=3)
                else:
                    st.warning("Sin coordenadas para mostrar.")

            st.markdown("---")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Total sismos", f"{total:,}")
            c2.metric("Magnitud promedio", f"{df_combo['MAGNITUD'].mean():.2f}")
            c3.metric("Profundidad promedio", f"{df_combo['PROFUNDIDAD'].mean():.1f} km")

            anio_max = (
                int(df_combo["AÑO"].max())
                if df_combo["AÑO"].notna().any()
                else "—"
            )
            c4.metric("Año más reciente", anio_max)