import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

CAT_COLORS = {
    "Rent":          "#6c63ff",
    "Food":          "#10b981",
    "Shopping":      "#f59e0b",
    "Entertainment": "#e040fb",
    "Other":         "#64748b",
}


def analytics_category_tab():
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                    color:#e8e8f0;margin-bottom:4px;">Spending by Category</div>
        <div style="font-size:0.78rem;color:#555577;letter-spacing:0.06em;">
            Break down your expenses across a date range
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                    'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:4px;">From</div>',
                    unsafe_allow_html=True)
        start_date = st.date_input("Start Date", datetime(2024, 8, 1), label_visibility="collapsed")

    with col2:
        st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                    'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:4px;">To</div>',
                    unsafe_allow_html=True)
        end_date = st.date_input("End Date", datetime(2024, 8, 5), label_visibility="collapsed")

    with col3:
        st.markdown('<div style="height:1.45rem"></div>', unsafe_allow_html=True)
        run = st.button("Analyze →")

    if run:
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date":   end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response = response.json()

        data = {
            "Category":   list(response.keys()),
            "Total":      [response[c]["total"]      for c in response],
            "Percentage": [response[c]["percentage"] for c in response],
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        # ── KPI strip ──
        grand_total = df_sorted["Total"].sum()
        top_cat     = df_sorted.iloc[0]["Category"] if not df_sorted.empty else "—"
        top_pct     = df_sorted.iloc[0]["Percentage"] if not df_sorted.empty else 0

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        for col, label, value, sub in [
            (k1, "Total Spent",     f"₹{grand_total:,.2f}", f"{start_date} → {end_date}"),
            (k2, "Top Category",   top_cat,                f"{top_pct:.1f}% of spending"),
            (k3, "Categories",     str(len(df_sorted)),    "with recorded spend"),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:#10101a;border:1px solid #1e1e2e;border-radius:14px;
                            padding:1rem 1.3rem;">
                  <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                              letter-spacing:0.12em;color:#555577;margin-bottom:6px;">{label}</div>
                  <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
                              background:linear-gradient(135deg,#c4b5fd,#e040fb);
                              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                              background-clip:text;">{value}</div>
                  <div style="font-size:0.72rem;color:#333355;margin-top:3px;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        # ── Bar chart ──
        st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                    'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:0.6rem;">'
                    'Distribution (%)</div>', unsafe_allow_html=True)

        chart_df = df_sorted.set_index("Category")[["Percentage"]]
        st.bar_chart(chart_df, use_container_width=True, height=260)

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

        # ── Breakdown cards ──
        st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                    'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:0.8rem;">'
                    'Breakdown</div>', unsafe_allow_html=True)

        for _, row in df_sorted.iterrows():
            cat   = row["Category"]
            total = row["Total"]
            pct   = row["Percentage"]
            color = CAT_COLORS.get(cat, "#64748b")
            bar_w = max(pct, 2)

            st.markdown(f"""
            <div style="background:#10101a;border:1px solid #1e1e2e;border-radius:12px;
                        padding:0.85rem 1.2rem;margin-bottom:0.6rem;
                        display:flex;align-items:center;gap:1rem;">
              <div style="width:36px;height:36px;border-radius:9px;
                          background:{color}22;border:1px solid {color}44;
                          display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="font-size:1rem;">
                  {"🏠" if cat=="Rent" else "🍔" if cat=="Food" else "🛍️" if cat=="Shopping" else "🎬" if cat=="Entertainment" else "📦"}
                </span>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                  <span style="font-family:'Syne',sans-serif;font-size:0.85rem;
                               font-weight:700;color:#e8e8f0;">{cat}</span>
                  <span style="font-size:0.85rem;color:#c8c8d8;">
                    ₹{total:,.2f} &nbsp;
                    <span style="color:{color};font-weight:600;">{pct:.1f}%</span>
                  </span>
                </div>
                <div style="height:4px;background:#1e1e2e;border-radius:999px;">
                  <div style="height:100%;width:{bar_w}%;background:linear-gradient(90deg,{color},{color}88);
                               border-radius:999px;transition:width 0.4s ease;"></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
