import streamlit as st

st.set_page_config(
    page_title="Patekar Hedging Algo",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 PATEKAR HEDGING ALGO")
st.caption("Version 1.0 | Paper Trading Dashboard")

st.sidebar.header("Strategy Settings")

market = st.sidebar.selectbox(
    "Market",
    ["NIFTY", "BANKNIFTY"]
)

capital = st.sidebar.number_input(
    "Capital (₹)",
    value=50000
)

risk = st.sidebar.number_input(
    "Maximum Risk Per Trade (₹)",
    value=750
)

strategy = st.sidebar.selectbox(
    "Hedging Strategy",
    ["Iron Condor", "Bull Call Spread",
     "Bear Put Spread", "Custom Hedge"]
)

st.subheader("Account Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Capital", f"₹{capital:,.0f}")
c2.metric("Risk Per Trade", f"₹{risk:,.0f}")
c3.metric("Trading Mode", "PAPER")

st.divider()

st.subheader("Strategy Configuration")

expiry = st.selectbox(
    "Expiry",
    ["Current Weekly", "Next Weekly", "Monthly"]
)

lots = st.number_input(
    "Lots",
    min_value=1,
    max_value=10,
    value=1
)

st.write("Selected Market:", market)
st.write("Selected Strategy:", strategy)
st.write("Selected Expiry:", expiry)
st.write("Selected Lots:", lots)

st.warning(
    "Paper Trading Only. No real orders will be placed."
)

if st.button("START PAPER TRADING"):
    st.success("Paper Trading Configuration Started!")

if st.button("STOP STRATEGY"):
    st.info("Strategy stopped.")

st.divider()

st.subheader("P&L Monitor")

st.metric("Paper P&L", "₹0.00")
st.metric("Open Positions", "0")

st.caption("Developed by Prof. Dinesh Patekar")
