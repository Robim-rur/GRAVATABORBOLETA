import streamlit as st
import yfinance as yf
import pandas as pd

# Configuração inicial da página do Streamlit
st.set_page_config(
    page_title="Scanner Bow Tie - Buy Side",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏹 Scanner Automático de Estratégia: Bow Tie (Gravata Borboleta)")
st.markdown("---")

# Caixa de texto explicativa sobre o setup de compra
st.info(
    "**Regra de Operação (Buy Side):**\n\n"
    "A entrada se dará quando houver o rompimento do candle de sinal no primeiro candle após o "
    "cruzamento entre a MMA10 x MME20 x MME30 e o STOP na mínima do candle que deu o sinal, "
    "sendo que a saída (GAIN) será quando houver um fechamento abaixo da MME20."
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

# Área de exibição/configuração na barra lateral
st.sidebar.header("Configurações do Rastreamento")
st.sidebar.markdown(f"Total de ativos configurados: **{len(ativos_padrao)}**")

lista_ativos = st.sidebar.text_area(
    "Lista de Monitoramento do Scanner:",
    value=", ".join(ativos_padrao),
    height=300
)

# Processando a string de texto para transformar em lista de tickers limpa
tickers = [t.strip().upper() for t in lista_ativos.split(",") if t.strip()]

def verificar_bow_tie(df):
    """
    Função interna que analisa as médias e identifica se o padrão Bow Tie aconteceu
    no último candle fechado usando puramente funções nativas do pandas.
    """
    if len(df) < 40:
        return False, None, None
    
    # Cálculo exato das Médias Móveis usando apenas Pandas nativo
    df['MMA10'] = df['Close'].rolling(window=10).mean()
    df['MME20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['MME30'] = df['Close'].ewm(span=30, adjust=False).mean()
    
    # Condição 1: Alinhamento de Alta Atual (MMA10 > MME20 > MME30)
    condicao_atual = (df['MMA10'].iloc[-1] > df['MME20'].iloc[-1]) and (df['MME20'].iloc[-1] > df['MME30'].iloc[-1])
    
    # Condição 2: Memória de Baixa Recente (Procura nos últimos candles se estavam invertidas)
    veio_de_baixa = False
    for i in range(-7, -1):
        if (df['MME30'].iloc[i] > df['MME20'].iloc[i]) and (df['MME20'].iloc[i] > df['MMA10'].iloc[i]):
            veio_de_baixa = True
            break
            
    # Condição 3: Gatilho do Cruzamento Recente
    cruzou_agora = (df['MMA10'].iloc[-2] <= df['MME20'].iloc[-2] or df['MMA10'].iloc[-2] <= df['MME30'].iloc[-2])
    
    if condicao_atual and veio_de_baixa and cruzou_agora:
        preco_gatilho = df['High'].iloc[-1]  # Rompimento da máxima do candle de sinal
        stop_loss = df['Low'].iloc[-1]      # Mínima do candle de sinal
        return True, preco_gatilho, stop_loss
        
    return False, None, None

# Botão principal na tela para acionar o scanner de mercado
if st.button("🚀 Executar Scanner Bow Tie", type="primary"):
    st.write(f"🔍 Buscando dados e escaneando {len(tickers)} ativos... Aguarde.")
    
    resultados = []
    progresso = st.progress(0)
    total_tickers = len(tickers)
    
    for idx, ticker in enumerate(tickers):
        progresso.progress((idx + 1) / total_tickers)
        
        try:
            # Coleta o histórico diário direto da API do Yahoo Finance
            dados = yf.download(ticker, period="6mo", interval="1d", progress=False, group_by='ticker', auto_adjust=True)
            
            if dados.empty:
                continue
            
            # Limpeza caso o DataFrame venha com colunas multi-indexadas
            if isinstance(dados.columns, pd.MultiIndex):
                dados.columns = dados.columns.get_level_values(-1)
                
            sinal, gatilho, stop = verificar_bow_tie(dados)
            
            if sinal:
                preco_atual = dados['Close'].iloc[-1]
                mme20_atual = dados['MME20'].iloc[-1]
                
                resultados.append({
                    "Ativo": ticker.replace(".SA", ""), 
                    "Preço Atual (R$)": round(float(preco_atual), 2),
                    "Gatilho (Rompimento da Máxima)": round(float(gatilho), 2),
                    "Stop Inicial (Mínima do Sinal)": round(float(stop), 2),
                    "MME20 de Saída (Alvo Dinâmico)": round(float(mme20_atual), 2)
                })
                
        except Exception:
            continue
            
    progresso.empty()
    
    st.subheader("📋 Painel Consolidador de Sinais (Apenas Buy Side)")
    
    if resultados:
        df_resultados = pd.DataFrame(resultados)
        st.success(f"🔥 Scanner concluído! Encontrado(s) {len(resultados)} ativo(s) configurando a Gravata Borboleta.")
        st.dataframe(df_resultados.set_index("Ativo"), use_container_width=True)
    else:
        st.info("Varredura completa realizada. Nenhum ativo da sua lista fechou gerando o sinal exato do Bow Tie.")
