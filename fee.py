import streamlit as st
import math

st.title("📈 Future Trading PnL Calculator")
st.write("Made your crypto trading calculations easy!")

# Input Section
with st.sidebar:
    st.header("📥 Input Parameters")
    trade_type = st.selectbox("Future Trading Type", ["Long", "Short"])
    entry_price = st.number_input("Entry Price ($)", min_value=0.0, format="%.8f")
    capital = st.number_input("Capital ($)", min_value=0.0)
    leverage = st.number_input("Leverage", min_value=1)
    funding_rate = st.number_input("Funding Rate (%)", format="%.6f") / 100  # Convert % to decimal
    holding_hours = st.number_input("Holding Hours", min_value=0)
    exit_price = st.number_input("Exit Price ($)", min_value=0.0, format="%.8f")
    order_type = st.selectbox("Order Type", ["Market", "Limit"])
    
    # Optional Inputs
    st.subheader("Optional Parameters")
    take_profit = st.number_input("Take Profit ($)", min_value=0.0, format="%.8f", value=0.0)
    stop_loss = st.number_input("Stop Loss ($)", min_value=0.0, format="%.8f", value=0.0)
    trailing = st.number_input("Trailing Stop ($)", min_value=0.0, format="%.8f", value=0.0)

# Calculations
position_size = capital * leverage
quantity = position_size / entry_price if entry_price != 0 else 0

# Fee Rates
maker_fee = 0.0002  # 0.02%
taker_fee = 0.0004  # 0.04%
fee_rate = taker_fee if order_type == "Market" else maker_fee

# Entry & Exit Fees
entry_fee = position_size * fee_rate
exit_fee = (quantity * exit_price) * fee_rate
total_fees = entry_fee + exit_fee

# Funding Fee Calculation
funding_intervals = math.ceil(holding_hours / 8) if holding_hours > 0 else 0
funding_fee = position_size * (funding_rate / 100) * funding_intervals  # Funding Rate as %

# Profit/Loss
if trade_type == "Long":
    profit = (exit_price - entry_price) * quantity
else:  # Short
    profit = (entry_price - exit_price) * quantity

# Net PnL
net_pnl = profit - total_fees - funding_fee

# Realized vs Unrealized PnL (Assume position closed)
realized_pnl = net_pnl
unrealized_pnl = "N/A (Position Closed)"  # Change if position open

# Display Results
st.header("📊 Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("Position Size", f"${position_size:,.2f}")
    st.metric("Quantity", f"{quantity:.6f}")
    st.metric("Gross Profit/Loss", f"${profit:,.2f}")
    
with col2:
    st.metric("Total Fees", f"${total_fees:,.4f}")
    st.metric("Funding Fee", f"${funding_fee:,.4f}")
    st.metric("Net Realized PnL", f"${net_pnl:,.2f}", delta_color="inverse")

# Optional Parameters Check
if take_profit > 0 or stop_loss > 0 or trailing > 0:
    st.subheader("🚦 Triggers Check")
    if take_profit > 0:
        st.write(f"Take Profit {'✅ Hit' if (exit_price >= take_profit and trade_type == 'Long') or (exit_price <= take_profit and trade_type == 'Short') else '❌ Not Hit'}")
    if stop_loss > 0:
        st.write(f"Stop Loss {'🔴 Hit' if (exit_price <= stop_loss and trade_type == 'Long') or (exit_price >= stop_loss and trade_type == 'Short') else '🟢 Not Hit'}")