
import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# PATEKAR HEDGING ALGO v2.0
# IRON CONDOR - PAPER TRADING
# ==========================================

st.set_page_config(
    page_title="PATEKAR HEDGING ALGO",
    page_icon="📊",
    layout="wide"
)

# ---------- SESSION STORAGE ----------

if "position" not in st.session_state:
    st.session_state.position = None

if "history" not in st.session_state:
    st.session_state.history = []

if "running" not in st.session_state:
    st.session_state.running = False


# ---------- P&L ENGINE ----------

def calculate_pnl(pos, marks, qty):

    return round(
        (pos["sp_entry"] - marks["sp"]) * qty
        + (marks["lp"] - pos["lp_entry"]) * qty
        + (pos["sc_entry"] - marks["sc"]) * qty
        + (marks["lc"] - pos["lc_entry"]) * qty,
        2
    )


def calculate_max_profit(pos):

    credit = (
        pos["sp_entry"] + pos["sc_entry"]
        - pos["lp_entry"] - pos["lc_entry"]
    )

    return round(credit * pos["qty"], 2)


def calculate_max_loss(pos):

    put_width = pos["sp_strike"] - pos["lp_strike"]
    call_width = pos["lc_strike"] - pos["sc_strike"]

    credit = (
        pos["sp_entry"] + pos["sc_entry"]
        - pos["lp_entry"] - pos["lc_entry"]
    )

    return round(
        max(0, max(put_width, call_width) - credit)
        * pos["qty"],
        2
    )


def trade_status(pnl, target, stop):

    if pnl >= target:
        return "TARGET HIT"

    if pnl <= -stop:
        return "STOP LOSS HIT"

    return "POSITION ACTIVE"


def close_trade(reason, pnl):

    pos = st.session_state.position

    if pos:
        st.session_state.history.append({
            "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Market": pos["market"],
            "Strategy": "IRON CONDOR",
            "Quantity": pos["qty"],
            "P&L": round(pnl, 2),
            "Exit Reason": reason
        })

        st.session_state.position = None


# ---------- HEADER ----------

st.title("📊 PATEKAR HEDGING ALGO")
st.caption("Professional Options Hedging | Iron Condor | Paper Trading")

st.warning(
    "PAPER TRADING ONLY — No real broker orders are placed. "
    "Option premiums are entered manually."
)

# ---------- SIDEBAR ----------

st.sidebar.title("⚙️ ALGO SETTINGS")

market = st.sidebar.selectbox(
    "Select Market",
    ["NIFTY", "BANKNIFTY"]
)

capital = st.sidebar.number_input(
    "Capital (₹)",
    min_value=1000,
    value=50000,
    step=5000
)

risk_limit = st.sidebar.number_input(
    "Maximum Risk Limit (₹)",
    min_value=100,
    value=750,
    step=100
)

target = st.sidebar.number_input(
    "Target Profit (₹)",
    min_value=100,
    value=1000,
    step=100
)

stop_loss = st.sidebar.number_input(
    "Stop Loss (₹)",
    min_value=100,
    value=750,
    step=100
)

lot_size = st.sidebar.number_input(
    "Quantity Per Lot",
    min_value=1,
    value=65,
    step=1
)

lots = st.sidebar.number_input(
    "Number of Lots",
    min_value=1,
    value=1,
    step=1
)

quantity = int(lot_size * lots)

st.sidebar.divider()

st.sidebar.write("Strategy: IRON CONDOR")
st.sidebar.write("Execution: PAPER ONLY")
st.sidebar.write("Broker: Not connected")

if st.sidebar.button("START ALGO", use_container_width=True):
    st.session_state.running = True

if st.sidebar.button("STOP ALGO", use_container_width=True):
    st.session_state.running = False

if st.session_state.running:
    st.sidebar.success("ALGO RUNNING")
else:
    st.sidebar.info("ALGO STOPPED")


# ---------- DASHBOARD ----------

pos = st.session_state.position

if pos:
    marks = pos["marks"]
    pnl = calculate_pnl(pos, marks, pos["qty"])
    status = trade_status(pnl, pos["target"], pos["stop"])

    total_trades = len(st.session_state.history)
    open_count = 1
else:
    pnl = 0
    status = "WAITING FOR TRADE"
    total_trades = len(st.session_state.history)
    open_count = 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Capital", f"₹{capital:,.0f}")
c2.metric("Current P&L", f"₹{pnl:,.2f}")
c3.metric("Open Positions", open_count)
c4.metric("Closed Trades", total_trades)

st.divider()

# ---------- LIVE POSITION ----------

st.subheader("📈 OPEN POSITION")

if pos:

    st.write(f"Market: {pos['market']}")
    st.write(f"Strategy: IRON CONDOR")
    st.write(f"Quantity: {pos['qty']}")

    a, b, c = st.columns(3)

    a.metric("Maximum Profit", f"₹{calculate_max_profit(pos):,.2f}")
    b.metric("Maximum Risk", f"₹{calculate_max_loss(pos):,.2f}")
    c.metric("Trade Status", status)

    st.markdown("### Four Legs")

    legs = pd.DataFrame([
        ["BUY", "LONG PUT", pos["lp_strike"], pos["lp_entry"], marks["lp"]],
        ["SELL", "SHORT PUT", pos["sp_strike"], pos["sp_entry"], marks["sp"]],
        ["SELL", "SHORT CALL", pos["sc_strike"], pos["sc_entry"], marks["sc"]],
        ["BUY", "LONG CALL", pos["lc_strike"], pos["lc_entry"], marks["lc"]]
    ], columns=["Side", "Leg", "Strike", "Entry Premium", "Current Premium"])

    st.dataframe(legs, use_container_width=True, hide_index=True)

    st.markdown("### Update Option Premiums")

    with st.form("update_marks"):

        x1, x2 = st.columns(2)

        with x1:
            new_sp = st.number_input(
                "Short Put Premium",
                min_value=0.0,
                value=float(marks["sp"]),
                key="mark_sp"
            )

            new_lp = st.number_input(
                "Long Put Premium",
                min_value=0.0,
                value=float(marks["lp"]),
                key="mark_lp"
            )

        with x2:
            new_sc = st.number_input(
                "Short Call Premium",
                min_value=0.0,
                value=float(marks["sc"]),
                key="mark_sc"
            )

            new_lc = st.number_input(
                "Long Call Premium",
                min_value=0.0,
                value=float(marks["lc"]),
                key="mark_lc"
            )

        update = st.form_submit_button(
            "UPDATE P&L",
            use_container_width=True
        )

    if update:

        pos["marks"] = {
            "sp": new_sp,
            "lp": new_lp,
            "sc": new_sc,
            "lc": new_lc
        }

        st.rerun()

    st.markdown("### Risk Monitor")

    progress = max(
        0.0,
        min(1.0, pnl / target)
    ) if target > 0 else 0.0

    st.progress(progress)

    st.write(f"Target: ₹{pos['target']:,.0f}")
    st.write(f"Stop Loss: ₹{pos['stop']:,.0f}")

    if status == "TARGET HIT":
        st.success("TARGET REACHED — Review and close position")

    elif status == "STOP LOSS HIT":
        st.error("STOP LOSS REACHED — Review and close position")

    else:
        st.info("Position Active — Monitoring paper P&L")

    if st.button("CLOSE POSITION", type="primary",
                 use_container_width=True):

        close_trade("MANUAL EXIT", pnl)
        st.rerun()

else:

    st.info("No Open Position. Create a new Iron Condor below.")


# ---------- NEW TRADE ----------

st.divider()
st.subheader("➕ CREATE NEW IRON CONDOR")

if st.session_state.position is None:

    with st.form("new_trade"):

        st.markdown("#### Strike Selection")

        x1, x2 = st.columns(2)

        with x1:

            lp_strike = st.number_input(
                "Long Put Strike",
                min_value=1.0,
                value=25000.0
            )

            sp_strike = st.number_input(
                "Short Put Strike",
                min_value=1.0,
                value=25100.0
            )

        with x2:

            sc_strike = st.number_input(
                "Short Call Strike",
                min_value=1.0,
                value=25300.0
            )

            lc_strike = st.number_input(
                "Long Call Strike",
                min_value=1.0,
                value=25400.0
            )

        st.markdown("#### Entry Premiums")

        x1, x2 = st.columns(2)

        with x1:

            lp_entry = st.number_input(
                "Long Put Buy Premium",
                min_value=0.0,
                value=30.0
            )

            sp_entry = st.number_input(
                "Short Put Sell Premium",
                min_value=0.0,
                value=80.0
            )

        with x2:

            sc_entry = st.number_input(
                "Short Call Sell Premium",
                min_value=0.0,
                value=80.0
            )

            lc_entry = st.number_input(
                "Long Call Buy Premium",
                min_value=0.0,
                value=30.0
            )

        override = st.checkbox(
            "Allow paper simulation even if estimated max loss exceeds risk limit"
        )

        create = st.form_submit_button(
            "CREATE PAPER TRADE",
            use_container_width=True
        )

    if create:

        if not (
            lp_strike < sp_strike
            < sc_strike < lc_strike
        ):
            st.error("Invalid strikes. Required: LP < SP < SC < LC")

        elif min(lp_entry, sp_entry, sc_entry, lc_entry) < 0:
            st.error("Premium cannot be negative.")

        else:

            credit = (
                sp_entry + sc_entry
                - lp_entry - lc_entry
            )

            if credit <= 0:
                st.error("Iron Condor must have positive net credit.")

            else:

                new_pos = {
                    "market": market,
                    "lp_strike": lp_strike,
                    "sp_strike": sp_strike,
                    "sc_strike": sc_strike,
                    "lc_strike": lc_strike,

                    "lp_entry": lp_entry,
                    "sp_entry": sp_entry,
                    "sc_entry": sc_entry,
                    "lc_entry": lc_entry,

                    "qty": quantity,
                    "target": target,
                    "stop": stop_loss,

                    "marks": {
                        "sp": sp_entry,
                        "lp": lp_entry,
                        "sc": sc_entry,
                        "lc": lc_entry
                    },

                    "created": datetime.now().strftime(
                        "%d-%m-%Y %H:%M"
                    )
                }

                max_risk = calculate_max_loss(new_pos)

                if max_risk > risk_limit and not override:

                    st.error(
                        f"Trade blocked! Estimated maximum loss "
                        f"₹{max_risk:,.2f} exceeds risk limit "
                        f"₹{risk_limit:,.2f}. Review strikes, quantity "
                        f"or risk settings."
                    )

                else:

                    st.session_state.position = new_pos
                    st.success("Paper position created!")
                    st.rerun()

else:

    st.warning("Close the existing position before creating another.")


# ---------- TRADE HISTORY ----------

st.divider()
st.subheader("📋 TRADE HISTORY")

if st.session_state.history:

    df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    total_pnl = df["P&L"].sum()

    wins = (df["P&L"] > 0).sum()
    total = len(df)

    win_rate = (wins / total * 100) if total else 0

    a, b, c = st.columns(3)

    a.metric("Total Realized P&L", f"₹{total_pnl:,.2f}")
    b.metric("Winning Trades", wins)
    c.metric("Win Rate", f"{win_rate:.1f}%")

    st.download_button(
        "DOWNLOAD TRADE HISTORY CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="patekar_trade_history.csv",
        mime="text/csv"
    )

else:

    st.info("No closed trades yet.")


# ---------- FOOTER ----------

st.divider()

st.caption(
    "PATEKAR HEDGING ALGO v2.0 | "
    "Paper Trading | Manual Premium Input | "
    "No Real Orders | Session-based History"
)
