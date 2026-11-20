
import math
import plotly.graph_objects as go
import streamlit as st

st.title("Simulação de distribuição de temperatura")

dimensao = st.radio(
    "Escolha o ambiente:",
    ["ℝ²", "ℝ³"],
    horizontal=True
)

if dimensao == "ℝ³":

    xmax = st.number_input(
        "Tamanho do sólido em X",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5
    )

    ymax = st.number_input(
        "Tamanho do sólido em Y",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5
    )

    col1, col2 = st.columns(2)

    with col1:
        funcao_solido = st.text_input(
            "Função do sólido (Z)",
            value="x**2 + y**2"
        )

    with col2:
        funcao_temperatura = st.text_input(
            "Função de temperatura (T)",
            value="30 + 5*z"
        )

    class Solido:

        def __init__(self, funcao, xmax, ymax):
            self.funcao = funcao
            self.xmax = xmax
            self.ymax = ymax

        def plotar(self):

            x = []
            y = []
            z = []
            temperatura = []

            for i in range(100):
                for j in range(100):

                    xi = i * self.xmax / 99
                    yi = j * self.ymax / 99

                    zi = eval(
                        self.funcao,
                        {"x": xi, "y": yi, "math": math}
                    )

                    ti = eval(
                        funcao_temperatura,
                        {"x": xi, "y": yi, "z": zi, "math": math}
                    )

                    x.append(xi)
                    y.append(yi)
                    z.append(zi)
                    temperatura.append(ti)

            fig = go.Figure(
                data=[go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode="markers",
                    marker=dict(
                        size=3,
                        color=temperatura,
                        colorscale="Jet",
                        colorbar=dict(title="Temperatura (°C)")
                    )
                )]
            )

            st.plotly_chart(fig, use_container_width=True)

    solido = Solido(funcao_solido, xmax, ymax)

    solido.plotar()
