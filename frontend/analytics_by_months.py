import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

MONTH_ICONS = {
    "January": "❄️", "February": "💘", "March": "🌱",
    "April": "🌸",   "May": "☀️",     "June": "🌊",
    "July": "🎆",    "August": "🌻",  "September": "🍂",
    "October": "🎃", "November": "🍁","December": "🎄",
}


def analytics_months_tab():
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                    color:#e8e8f0;margin-bottom:4px;">Monthly Overview</div>
        <div style="font-size:0.78rem;color:#555577;letter-spacing:0.06em;">
            Track your spending trends across months
        </div>
    </div>
    """, unsafe_allow_html=True)

    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name":    "Month Name",
        "total":         "Total"
    }, inplace=True)

    df_sorted = df.sort_values(by="Month Number", ascending=False)

    # ── KPI strip ──
    if not df_sorted.empty:
        grand   = df_sorted["Total"].sum()
        avg_mo  = df_sorted["Total"].mean()
        peak    = df_sorted.loc[df_sorted["Total"].idxmax(), "Month Name"]

        k1, k2, k3 = st.columns(3)
        for col, label, value, sub in [
            (k1, "Total (All Months)", f"₹{grand:,.2f}",   "across all tracked months"),
            (k2, "Monthly Average",    f"₹{avg_mo:,.2f}",  "per month"),
            (k3, "Peak Month",          peak,              "highest spending"),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:#10101a;border:1px solid #1e1e2e;border-radius:14px;
                            padding:1rem 1.3rem;margin-bottom:1rem;">
                  <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                              letter-spacing:0.12em;color:#555577;margin-bottom:6px;">{label}</div>
                  <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
                              background:linear-gradient(135deg,#6ee7b7,#6c63ff);
                              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                              background-clip:text;">{value}</div>
                  <div style="font-size:0.72rem;color:#333355;margin-top:3px;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Bar chart ──
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:0.6rem;">'
                'Monthly Trend</div>', unsafe_allow_html=True)

    chart_df = (
        df_sorted
        .sort_values("Month Number")
        .set_index("Month Name")[["Total"]]
    )
    st.bar_chart(chart_df, use_container_width=True, height=260)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Month cards ──
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:0.8rem;">'
                'Month-by-Month</div>', unsafe_allow_html=True)

    max_total = df_sorted["Total"].max() if not df_sorted.empty else 1

    for _, row in df_sorted.iterrows():
        month = row["Month Name"]
        total = row["Total"]
        mo_no = row["Month Number"]
        pct   = (total / max_total) * 100 if max_total else 0
        icon  = MONTH_ICONS.get(month, "📅")

        # gradient shift by month
        hue   = int((mo_no / 12) * 260)
        color = f"hsl({hue},70%,65%)"

        st.markdown(f"""
        <div style="background:#10101a;border:1px solid #1e1e2e;border-radius:12px;
                    padding:0.85rem 1.2rem;margin-bottom:0.5rem;
                    display:flex;align-items:center;gap:1rem;">
          <div style="width:38px;height:38px;border-radius:10px;
                      background:{color}22;border:1px solid {color}44;
                      display:flex;align-items:center;justify-content:center;
                      font-size:1.1rem;flex-shrink:0;">{icon}</div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
              <span style="font-family:'Syne',sans-serif;font-size:0.85rem;
                           font-weight:700;color:#e8e8f0;">{month}</span>
              <span style="font-size:0.85rem;color:#c8c8d8;font-weight:600;">₹{total:,.2f}</span>
            </div>
            <div style="height:4px;background:#1e1e2e;border-radius:999px;">
              <div style="height:100%;width:{pct:.1f}%;
                           background:linear-gradient(90deg,{color},{color}88);
                           border-radius:999px;"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
