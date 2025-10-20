import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos desde el archivo Excel


@st.cache_data
def cargar_datos():
    df = pd.read_excel("1house_prices_spain.xlsx")

    # Normalizar nombres de columnas
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Convertir columnas binarias a booleanas
    for col in ['garaje', 'ascensor']:
        df[col] = df[col].fillna(0).astype(bool)

    # Energía renovable: convertir a booleano si tiene valor
    df['energía_renovable'] = df['energía_renovable'].notna()

    return df


df = cargar_datos()

# Título principal
st.header("🏡 Escoge la vivienda a tu comodidad")

# Entradas del usuario
habitaciones = st.number_input(
    "Cantidad de habitaciones", min_value=1, max_value=10, value=3)
baños = st.number_input("Cantidad de baños", min_value=1, max_value=5, value=2)
ascensor = st.checkbox("¿Desea ascensor?")
garaje = st.checkbox("¿Desea garaje?")
energia_renovable = st.checkbox("¿Desea energía renovable?")

# Gráfico de dispersión de precios
df['rango_precio'] = pd.cut(df['precio_(eur)'],
                            bins=[0, 50000, 100000, 150000, 200000,
                                  250000, 300000, 400000, 500000],
                            labels=["<=50k", "<=100k", "<=150k", "<=200k", "<=250k", "<=300k", "<=400k", ">400k"])

fig_dispersion = px.scatter(df, x="superficie_(m2)", y="precio_(eur)", color="rango_precio",
                            title="📈 Precio vs Superficie", labels={"superficie_(m2)": "Metros cuadrados", "precio_(eur)": "Precio (€)"})
st.plotly_chart(fig_dispersion)

# Botón para mostrar histograma
if st.button("Mostrar histograma de precios"):
    fig_hist = px.histogram(df, x="precio_(eur)", nbins=30,
                            title="📊 Distribución de precios")
    st.write("Histograma de precios")
    st.plotly_chart(fig_hist)

# Botón para mostrar resultados filtrados
if st.button("Mostrar viviendas filtradas"):
    filtro = (
        (df['habitaciones'] == habitaciones) &
        (df['baños'] == baños) &
        (df['ascensor'] == ascensor) &
        (df['garaje'] == garaje) &
        (df['energía_renovable'] == energia_renovable)
    )
    df_filtrado = df[filtro]

    st.write("🏷️ Resultados filtrados según tus preferencias:")
    st.dataframe(df_filtrado)

    st.write(
        f"🔎 Se encontraron {len(df_filtrado)} viviendas que cumplen con tus criterios.")
else:
    st.write("🛠️ La aplicación está en construcción. Ajusta los filtros y haz clic en los botones para explorar.")
