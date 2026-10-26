import pandas as pd
import plotly.express as px
from django.shortcuts import render

from casos.models import Caso

INK = "#101828"


def _html(fig, primeiro=False):
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=10, r=10, t=50, b=10), font=dict(color=INK))
    return fig.to_html(full_html=False, include_plotlyjs="cdn" if primeiro else False)


def painel(request):
    qs = Caso.objects.filter(aprovado=True).values(
        "cidade", "status", "idade", "data_desaparecimento", "data_encontrado")
    df = pd.DataFrame(list(qs))
    if df.empty:
        return render(request, "analises/painel.html", {"total": 0})

    total = len(df)
    achados = df[df["status"] == "encontrado"]

    por_cidade = (df.groupby("cidade").size().reset_index(name="casos")
                    .sort_values("casos", ascending=False).head(10))
    g_cidade = px.bar(por_cidade, x="cidade", y="casos", title="Casos por cidade",
                      color_discrete_sequence=[INK])

    df["mes"] = pd.to_datetime(df["data_desaparecimento"]).dt.to_period("M").astype(str)
    por_mes = df.groupby("mes").size().reset_index(name="casos")
    g_mes = px.line(por_mes, x="mes", y="casos", markers=True, title="Casos por mês",
                    color_discrete_sequence=[INK])

    faixas = pd.cut(df["idade"], bins=[-1, 12, 17, 29, 59, 200],
                    labels=["0 a 12", "13 a 17", "18 a 29", "30 a 59", "60 ou mais"])
    por_faixa = faixas.value_counts(sort=False).reset_index()
    por_faixa.columns = ["faixa", "casos"]
    g_faixa = px.bar(por_faixa, x="faixa", y="casos", title="Casos por faixa etária",
                     color_discrete_sequence=[INK])

    tempo = None
    com_data = achados.dropna(subset=["data_encontrado"])
    if not com_data.empty:
        dias = (pd.to_datetime(com_data["data_encontrado"]) - pd.to_datetime(com_data["data_desaparecimento"])).dt.days
        tempo = round(float(dias.mean()), 1)

    return render(request, "analises/painel.html", {
        "total": total, "encontrados": len(achados),
        "taxa": round(len(achados) / total * 100, 1), "tempo": tempo,
        "g_cidade": _html(g_cidade, primeiro=True), "g_mes": _html(g_mes), "g_faixa": _html(g_faixa),
    })
