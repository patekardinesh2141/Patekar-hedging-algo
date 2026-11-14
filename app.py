    current_pnl = pos.get("last_pnl", 0.0)

    x, y, z = st.columns(3)

    x.metric("Current Paper P&L", f"₹{current_pnl:,.2f}")
    y.metric("Maximum Estimated Loss", f"₹{pos['max_loss']:,.2f}")
    z.metric("Target", f"₹{pos['target']:,.2f}")

    if st.button("CLOSE PAPER POSITION", type="primary"):
        close_position("Manual Exit", current_pnl)
        st.rerun()

# ---------- HISTORY ----------
st.divider()
st.subheader("📈 Trade History")

if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    wins = sum(1 for t in st.session_state.history if t["P&L"] > 0)
    total = len(st.session_state.history)

    st.metric("Winning Trades", f"{wins}/{total}")
    st.metric("Win Rate", f"{wins / total * 100:.1f}%")
else:
    st.info("No completed paper trades yet.")

st.caption(
    "Developed by Prof. Dinesh Patekar | "
    "Manual-premium Paper Simulator | No Real Orders"
)
