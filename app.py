python
import streamlit as st
import yfinance as yf
import pandas as pd

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Scanner Bow Tie Profissional",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏹 Scanner Bow Tie Profissional")
st.markdown("---")

st.info(
    """
    ✅ FILTRO PRINCIPAL: GRÁFICO SEMANAL
    
    O ativo somente será considerado se:
    
    MMA10 > MME20 > MME30 no SEMANAL
    
    ✅ GATILHO: GRÁFICO DIÁRIO
    
    Depois disso, o scanner procura o cruzamento recente no gráfico diário.
    """
)

# SUA LISTA EXATA DE ATIVOS
ativos_padrao = [
    # Suas Ações Iniciais
    "BPAC11.SA", "PRIO3.SA", "USIM5.SA", "ITUB4.SA", "B3SA3.SA", 
    "ITSA4.SA", "TAEE11.SA", "PETR3.SA", "EQTL3.SA", "MULT3.SA",

    # Novas ações encontradas nas listas adicionais
    "PETR4.SA","VALE3.SA","BBDC4.SA","BBAS3.SA","ABEV3.SA",
    "JBSS3.SA","ELET3.SA","WEGE3.SA","RENT3.SA","HAPV3.SA",
    "GGBR4.SA","SUZB3.SA","CSAN3.SA","RDOR3.SA","RAIL3.SA",
    "VIBR3.SA","UGPA3.SA","SBSP3.SA","ASAI3.SA","CCRO3.SA",
    "RADL3.SA","CMIG4.SA","CPLE6.SA","TOTS3.SA","CPFE3.SA",
    "ENEV3.SA","EMBR3.SA","BRFS3.SA","CRFB3.SA","CSNA3.SA",
    "GOAU4.SA","HYPE3.SA","FLRY3.SA","EGIE3.SA","TRPL4.SA",
    "KLBN11.SA","SANB11.SA","PSSA3.SA","BBSE3.SA","MRVE3.SA",
    "CYRE3.SA","EZTC3.SA","DIRR3.SA","ALPA4.SA","YDUQ3.SA",
    "COGN3.SA","AZUL4.SA","GOLL4.SA","CVCB3.SA","TIMS3.SA",
    "VIVT3.SA","BRAP4.SA","CMIN3.SA","CSMG3.SA","SAPR11.SA",
    "ALUP11.SA","SMTO3.SA","SLCE3.SA","BEEF3.SA","MRFG3.SA",
    "MDIA3.SA","STBP3.SA","ARZZ3.SA","VIVA3.SA","SOMA3.SA",
    "GMAT3.SA","LWSA3.SA","CASH3.SA","POSI3.SA","INTB3.SA",
    "RECV3.SA","BRKM5.SA","DXCO3.SA","POMO4.SA","TUPY3.SA",
    "KEPL3.SA","RANI3.SA","UNIP6.SA","ELET6.SA","CXSE3.SA",
    "BRSR6.SA","JHSF3.SA","MOVI3.SA","PETZ3.SA","NTCO3.SA",
    "RRRP3.SA","ENAT3.SA","ORVR3.SA","ALOS3.SA","ODPV3.SA",
    "SAPR4.SA","ENGI11.SA","RAIZ4.SA","BHIA3.SA","IFCM3.SA",
    "PLAS3.SA","RAPT4.SA","TEND3.SA",
    
    # Seus BDRs
    "AAPL34.SA", "AMZO34.SA", "GOGL34.SA", "MSFT34.SA", "TSLA34.SA", "META34.SA",
    "NFLX34.SA", "NVDC34.SA", "MELI34.SA", "BABA34.SA", "DISB34.SA", "PYPL34.SA",
    "JNJB34.SA", "PGCO34.SA", "KOCH34.SA", "VISA34.SA", "WMTB34.SA", "NIKE34.SA",
    "ADBE34.SA", "AVGO34.SA", "CSCO34.SA", "COST34.SA", "CVSH34.SA", "GECO34.SA",
    "GSGI34.SA", "HDCO34.SA", "INTC34.SA", "JPMC34.SA", "MAEL34.SA", "MCDP34.SA",
    "MDLZ34.SA", "MRCK34.SA", "ORCL34.SA", "PEP334.SA", "PFIZ34.SA", "PMIC34.SA",
    "QCOM34.SA", "SBUX34.SA", "TGTB34.SA", "TMOS34.SA", "TXN34.SA", "UNHH34.SA",
    "UPSB34.SA", "VZUA34.SA", "ABTT34.SA", "AMGN34.SA", "AXPB34.SA", "BAOO34.SA",
    "C2OL34.SA", "HONB34.SA", "BICE34.SA", "BERK34.SA", "GOGL35.SA","CATP34.SA",
    
    # Seus ETFs / FIIs
    "BOVA11.SA",  "IVVB11.SA", "SMAL11.SA", "HASH11.SA", "GOLD11.SA", "DIVO11.SA",
    "NDIV11.SA", "SPUB11.SA", "VWRA11.SA", "GARE11.SA", "UTLL11.SA", "GGRC11.SA", 
    "HGLG11.SA","XPLG11.SA","VISC11.SA","MXRF11.SA","KNRI11.SA","KNCR11.SA","KNIP11.SA",
    "CPTS11.SA","IRDM11.SA","TRXF11.SA","TGAR11.SA","HGRU11.SA","ALZR11.SA","AUVP11.SA",
    "IEEX11.SA","VILG11.SA","BRCO11.SA","BTLG11.SA","XPML11.SA","HSML11.SA","MALL11.SA",
    "JSRE11.SA","PVBI11.SA","HGRE11.SA",
]

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Configurações")

lista_ativos = st.sidebar.text_area(
    "Lista de Ativos",
    value=", ".join(ativos_padrao),
    height=300
)

tickers = [t.strip().upper() for t in lista_ativos.split(",") if t.strip()]

# ==========================================
# FUNÇÃO DAS MÉDIAS
# ==========================================

def calcular_medias(df):

    df["MMA10"] = df["Close"].rolling(window=10).mean()

    df["MME20"] = df["Close"].ewm(
        span=20,
        adjust=False
    ).mean()

    df["MME30"] = df["Close"].ewm(
        span=30,
        adjust=False
    ).mean()

    return df

# ==========================================
# FILTRO SEMANAL
# ==========================================

def filtro_semanal(df):

    if len(df) < 40:
        return False

    df = calcular_medias(df)

    alinhado = (
        df["MMA10"].iloc[-1] > df["MME20"].iloc[-1]
        and
        df["MME20"].iloc[-1] > df["MME30"].iloc[-1]
    )

    return alinhado

# ==========================================
# GATILHO DIÁRIO
# ==========================================

def gatilho_diario(df):

    if len(df) < 40:
        return False, None, None

    df = calcular_medias(df)

    # --------------------------------------
    # CONDIÇÃO ATUAL
    # --------------------------------------

    condicao_atual = (
        df["MMA10"].iloc[-1] > df["MME20"].iloc[-1]
        and
        df["MME20"].iloc[-1] > df["MME30"].iloc[-1]
    )

    # --------------------------------------
    # VEIO DE BAIXA
    # --------------------------------------

    veio_de_baixa = False

    for i in range(-7, -1):

        if (
            df["MME30"].iloc[i] > df["MME20"].iloc[i]
            and
            df["MME20"].iloc[i] > df["MMA10"].iloc[i]
        ):

            veio_de_baixa = True
            break

    # --------------------------------------
    # CRUZAMENTO RECENTE
    # --------------------------------------

    cruzou_agora = (

        df["MMA10"].iloc[-2] <= df["MME20"].iloc[-2]

        or

        df["MMA10"].iloc[-2] <= df["MME30"].iloc[-2]

    )

    # --------------------------------------
    # SINAL FINAL
    # --------------------------------------

    if condicao_atual and veio_de_baixa and cruzou_agora:

        preco_gatilho = df["High"].iloc[-1]

        stop_loss = df["Low"].iloc[-1]

        return True, preco_gatilho, stop_loss

    return False, None, None

# ==========================================
# BOTÃO PRINCIPAL
# ==========================================

if st.button("🚀 Executar Scanner", type="primary"):

    resultados = []

    progresso = st.progress(0)

    total = len(tickers)

    st.write(f"🔍 Escaneando {total} ativos...")

    # ======================================
    # LOOP PRINCIPAL
    # ======================================

    for idx, ticker in enumerate(tickers):

        progresso.progress((idx + 1) / total)

        try:

            # ==================================
            # DADOS SEMANAIS
            # ==================================

            dados_semanal = yf.download(
                ticker,
                period="2y",
                interval="1wk",
                progress=False,
                auto_adjust=True
            )

            # ==================================
            # DADOS DIÁRIOS
            # ==================================

            dados_diario = yf.download(
                ticker,
                period="6mo",
                interval="1d",
                progress=False,
                auto_adjust=True
            )

            # ==================================
            # VALIDAÇÕES
            # ==================================

            if dados_semanal.empty:
                continue

            if dados_diario.empty:
                continue

            # ==================================
            # MULTI INDEX
            # ==================================

            if isinstance(dados_semanal.columns, pd.MultiIndex):

                dados_semanal.columns = (
                    dados_semanal.columns.get_level_values(-1)
                )

            if isinstance(dados_diario.columns, pd.MultiIndex):

                dados_diario.columns = (
                    dados_diario.columns.get_level_values(-1)
                )

            # ==================================
            # FILTRO SEMANAL
            # ==================================

            semanal_ok = filtro_semanal(dados_semanal)

            if not semanal_ok:
                continue

            # ==================================
            # GATILHO DIÁRIO
            # ==================================

            sinal, gatilho, stop = gatilho_diario(dados_diario)

            if sinal:

                dados_diario = calcular_medias(dados_diario)

                preco_atual = dados_diario["Close"].iloc[-1]

                mme20 = dados_diario["MME20"].iloc[-1]

                resultados.append({

                    "Ativo": ticker.replace(".SA", ""),

                    "Preço Atual": round(float(preco_atual), 2),

                    "Gatilho": round(float(gatilho), 2),

                    "Stop": round(float(stop), 2),

                    "MME20 Saída": round(float(mme20), 2),

                })

        except Exception:
            continue

    progresso.empty()

    # ======================================
    # RESULTADOS
    # ======================================

    st.subheader("📋 Resultado do Scanner")

    if resultados:

        df_resultados = pd.DataFrame(resultados)

        st.success(
            f"✅ Encontrado(s) {len(resultados)} ativo(s) "
            f"com alinhamento semanal + gatilho diário."
        )

        st.dataframe(
            df_resultados.set_index("Ativo"),
            use_container_width=True
        )

    else:

        st.warning(
            "Nenhum ativo encontrado com "
            "alinhamento semanal + gatilho diário."
        )

