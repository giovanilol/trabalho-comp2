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
        "Tamanho do sólido em X (-X a +X)",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5
    )

    ymax = st.number_input(
        "Tamanho do sólido em Y (-Y a +Y)",
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

        def __init__(self, func_z, func_t, xmax, ymax):
            # Substitui ^ por ** para evitar erro de sintaxe matemática
            self.func_z = func_z.replace("^", "**")
            self.func_t = func_t.replace("^", "**")
            self.xmax = xmax
            self.ymax = ymax

        def plotar(self):
            x = []
            y = []
            z = []
            temperatura = []

            # Ambiente com funções matemáticas diretas (sem precisar digitar math.)
            ambiente_math = {
                "math": math,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "exp": math.exp,
                "log": math.log,
                "abs": abs,
                "pi": math.pi,
                "e": math.e
            }

            for i in range(1000):
                for j in range(1000):
                    # Varia de -xmax até +xmax (para ver o sólido inteiro)
                    xi = -self.xmax + (2 * self.xmax * i / 999)
                    yi = -self.ymax + (2 * self.ymax * j / 999)

                    try:
                        # Atualiza x e y no dicionário
                        ambiente_math["x"] = xi
                        ambiente_math["y"] = yi

                        zi = eval(self.func_z, {"__builtins__": {}}, ambiente_math)

                        # Ignora se o resultado for complexo (ex: raiz de negativo com **) ou infinito
                        if isinstance(zi, complex) or math.isnan(zi) or math.isinf(zi):
                            continue

                        ambiente_math["z"] = zi
                        ti = eval(self.func_t, {"__builtins__": {}}, ambiente_math)

                        if isinstance(ti, complex) or math.isnan(ti) or math.isinf(ti):
                            continue

                        x.append(float(xi))
                        y.append(float(yi))
                        z.append(float(zi))
                        temperatura.append(float(ti))

                    except (ValueError, ZeroDivisionError, OverflowError):
                        # Pula pontos fora do domínio (ex: divisão por zero ou log de negativo)
                        continue
                    except Exception as erro:
                        st.error(f"Erro na expressão digitada: {erro}")
                        return

            if not x:
                st.warning("Nenhum ponto válido foi gerado nesse intervalo. Verifique o domínio da função.")
                return

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

            fig.update_layout(
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z"
                )
            )

            st.plotly_chart(fig, use_container_width=True)

    meu_solido = Solido(funcao_solido, funcao_temperatura, xmax, ymax)
    meu_solido.plotar()
