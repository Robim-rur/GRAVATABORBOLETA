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
    
    # Seus BDRs
    "AAPL34.SA", "AMZO34.SA", "GOGL34.SA", "MSFT34.SA", "TSLA34.SA", "META34.SA",
    "NFLX34.SA", "NVDC34.SA", "MELI34.SA", "BABA34.SA", "DISB34.SA", "PYPL34.SA",
    "JNJB34.SA", "PGCO34.SA", "KOCH34.SA", "VISA34.SA", "WMTB34.SA", "NIKE34.SA",
    "ADBE34.SA", "AVGO34.SA", "CSCO34.SA", "COST34.SA", "CVSH34.SA", "GECO34.SA",
    "GSGI34.SA", "HDCO34.SA", "INTC34.SA", "JPMC34.SA", "MAEL34.SA", "MCDP34.SA",
    "MDLZ34.SA", "MRCK34.SA", "ORCL34.SA", "PEP334.SA", "PFIZ34.SA", "PMIC34.SA",
    "QCOM34.SA", "SBUX34.SA", "TGTB34.SA", "TMOS34.SA", "TXN34.SA", "UNHH34.SA",
    "UPSB34.SA", "VZUA34.SA", "ABTT34.SA", "AMGN34.SA", "AXPB34.SA", "BAOO34.SA",
    "C2OL34.SA", "HONB34.SA", "BICE34.SA", "BERK34.SA", "GOGL35.SA",
    
    # Seus ETFs / FIIs
    "BOVA11.SA", "IVVB11.SA", "SMAL11.SA", "HASH11.SA", "GOLD11.SA", "DIVO11.SA",
    "NDIV11.SA", "SPUB11.SA", "VWRA11.SA", "GARE11.SA", "UTLL11.SA", "GGRC11.SA"
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
    no último candle fechado.
    """
    if len(df) < 40:  # Evita erro se o histórico do ativo for muito curto
        return False, None, None
    
    # Cálculo exato dos indicadores utilizando pandas padrão para estabilidade
    df['MMA10'] = df['Close'].rolling(window=10).mean()
    df['MME20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['MME30'] = df['Close'].ewm(span=30, adjust=False).mean()
    
    # Condição 1: Alinhamento de Alta Atual (MMA10 > MME20 > MME30)
    condicao_atual = (df['MMA10'].iloc[-1] > df['MME20'].iloc[-1]) and (df['MME20'].iloc[-1] > df['MME30'].iloc[-1])
    
    # Condição 2: Memória de Baixa Recente (Procura nos últimos 6 candles se estavam na ordem invertida)
    veio_de_baixa = False
    for i in range(-7, -1):
        if (df['MME30'].iloc[i] > df['MME20'].iloc[i]) and (df['MME20'].iloc[i] > df['MMA10'].iloc[i]):
            veio_de_baixa = True
            break
            
    # Condição 3: Gatilho do Cruzamento (No candle imediatamente anterior, o cruzamento completo ainda não existia)
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
    
    # Barra de progresso visual do Streamlit
    progresso = st.progress(0)
    total_tickers = len(tickers)
    
    for idx, ticker in enumerate(tickers):
        progresso.progress((idx + 1) / total_tickers)
        
        try:
            # Coleta o histórico diário direto da API do Yahoo Finance
            # group_by='ticker' e auto_adjust ajudam a evitar quebras de colunas do yfinance
            dados = yf.download(ticker, period="6mo", interval="1d", progress=False, group_by='ticker', auto_adjust=True)
            
            if dados.empty:
                continue
            
            # Ajuste crucial para o yfinance atual: Se as colunas vierem multi-indexadas, nós limpamos
            if isinstance(dados.columns, pd.MultiIndex):
                dados.columns = dados.columns.get_level_values(-1)
                
            sinal, gatilho, stop = verificar_bow_tie(dados)
            
            # Se o ativo atender a TODOS os critérios do Bow Tie de compra, adiciona na tabela
            if sinal:
                preco_atual = dados['Close'].iloc[-1]
                mme20_atual = dados['MME20'].iloc[-1]
                
                resultados.append({
                    "Ativo": ticker.replace(".SA", ""), # Limpa o código para exibição estética
                    "Preço Atual (R$)": round(float(preco_atual), 2),
                    "Gatilho (Rompimento da Máxima)": round(float(gatilho), 2),
                    "Stop Inicial (Mínima do Sinal)": round(float(stop), 2),
                    "MME20 de Saída (Alvo Dinâmico)": round(float(mme20_atual), 2)
                })
                
        except Exception:
            continue
            
    # Remove a barra de progresso após finalizar
    progresso.empty()
    
    # Apresentação dos resultados consolidados
    st.subheader("📋 Painel Consolidador de Sinais (Apenas Buy Side)")
    
    if resultados:
        df_resultados = pd.DataFrame(resultados)
        st.success(f"🔥 Scanner concluído! Encontrado(s) {len(resultados)} ativo(s) configurando a Gravata Borboleta.")
        st.dataframe(df_resultados.set_index("Ativo"), use_container_width=True)
    else:
        st.info("Varredura completa realizada. Nenhum ativo da sua lista fechou gerando o sinal exato do Bow Tie.")vo da sua lista fechou gerando o sinal exato do Bow Tie.")
