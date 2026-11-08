import streamlit as st import pandas as pd
st.set_page_config( page_title="Patekar Smart Hedging Algo", page_icon="📈", layout="wide" )
st.title("🚀 PATEKAR SMART HEDGING ALGO") st.caption("Version 2.0 | NIFTY Iron Condor | PAPER TRADING")
Risk settings
st.sidebar.header("⚙️ Risk Management")
capital = st.sidebar.number_input( "Trading Capital (₹)", value=50000, min_value=1000 ) risk = st.sidebar.number_input( "Maximum Risk Per Trade (₹)", value=750, min_value=1 ) daily_limit = st.sidebar.number_input( "Daily Maximum Loss (₹)", value=2000, min_value=1 ) lot_size = st.sidebar.number_input( "Lot Size", value=65, min_value=1 ) lots = st.sidebar.number_input( "Number of Lots", value=1, min_value=1 )
st.sidebar.warning("Paper trading only. No live orders.")
Session state
if "running" not in st.session_state: st.session_state.running = False
if "trades" not in st.session_state: st.session_state.trades = []
if "daily_pnl" not in st.session_state: st.session_state.daily_pnl = 0.0
st.subheader("📊 Account Overview")
a, b, c, d = st.columns(4) a.metric("Capital", f"₹{capital:,.0f}") b.metric("Risk / Trade", f"₹{risk:,.0f}") c.metric("Daily Loss Limit", f"₹{daily_limit:,.0f}") d.metric("Mode", "PAPER")
st.divider() st.subheader("🧩 NIFTY Iron Condor — Four Legs")
st.info( "Enter simulated option premiums. " "Choose strikes from your market research; this app does not fetch live prices." )
col1, col2 = st.columns(2)
with col1: sell_ce_strike = st.number_input("Sell CE Strike", value=26000) sell_ce = st.number_input("Sell CE Entry Premium", value=100.0) buy_ce_strike = st.number_input("Buy CE Hedge Strike", value=26100) buy_ce = st.number_input("Buy CE Entry Premium", value=50.0)
with col2: sell_pe_strike = st.number_input("Sell PE Strike", value=25500) sell_pe = st.number_input("Sell PE Entry Premium", value=100.0) buy_pe_strike = st.number_input("Buy PE Hedge Strike", value=25400) buy_pe = st.number_input("Buy PE Entry Premium", value=50.0)
total_qty = lot_size * lots
credit = (sell_ce + sell_pe - buy_ce - buy_pe) * total_qty
Basic theoretical expiry risk for a same-expiry,
correctly paired, defined-risk iron condor.
valid = ( buy_ce_strike > sell_ce_strike and buy_pe_strike < sell_pe_strike )
if valid: call_width = buy_ce_strike - sell_ce_strike put_width = sell_pe_strike - buy_pe_strike max_loss = max(call_width, put_width) * total_qty - credit max_loss = max(0, max_loss) else: max_loss = None
st.subheader("💰 Strategy Risk Preview") x, y = st.columns(2) x.metric("Net Credit (₹)", f"₹{credit:,.2f}")
if valid: y.metric("Estimated Max Expiry Loss (₹)", f"₹{max_loss:,.2f}") else: y.error("Invalid strikes: Buy CE must be above Sell CE and Buy PE below Sell PE.")
st.caption( "Expiry-risk estimate assumes all four legs fill at entered premiums " "and are held to the same expiry. Brokerage, taxes, slippage and execution " "risk are not included." )
st.divider() st.subheader("🎯 Paper Trade Controls")
can_start = valid and credit > 0 and max_loss <= risk
if not can_start: st.warning( "Entry disabled: check strikes, premiums and risk. " "Estimated maximum expiry loss must be within your per-trade limit." )
if st.button("▶️ START PAPER STRATEGY", disabled=not can_start): st.session_state.running = True st.success("Paper strategy configuration activated.")
if st.button("⏹ STOP STRATEGY"): st.session_state.running = False st.info("Paper strategy stopped.")
st.write( "Strategy Status:", "🟢 PAPER CONFIGURATION ACTIVE" if st.session_state.running else "🔴 STOPPED" )
st.divider() st.subheader("📈 Simulated Exit & P&L")
st.caption( "Enter the premiums at which all four legs could hypothetically be exited. " "This does not execute or verify market orders." )
e1, e2 = st.columns(2)
with e1: exit_sell_ce = st.number_input("Sell CE Exit Premium", value=100.0) exit_buy_ce = st.number_input("Buy CE Exit Premium", value=50.0)
with e2: exit_sell_pe = st.number_input("Sell PE Exit Premium", value=100.0) exit_buy_pe = st.number_input("Buy PE Exit Premium", value=50.0)
Credit spread P&L:
