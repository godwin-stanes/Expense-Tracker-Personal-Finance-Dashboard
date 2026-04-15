import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"


def add_update_tab():
    # ── Section header ──
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                    color:#e8e8f0;margin-bottom:4px;">Log Expenses</div>
        <div style="font-size:0.78rem;color:#555577;letter-spacing:0.06em;">
            Select a date and fill in up to 5 expense entries
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Date picker row ──
    col_date, col_spacer = st.columns([1, 3])
    with col_date:
        st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
                    'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:4px;">Date</div>',
                    unsafe_allow_html=True)
        selected_date = st.date_input("Date", datetime(2024, 8, 1), label_visibility="collapsed")

    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # ── Category color map for badges ──
    CAT_COLORS = {
        "Rent":          ("#6c63ff", "#6c63ff22"),
        "Food":          ("#10b981", "#10b98122"),
        "Shopping":      ("#f59e0b", "#f59e0b22"),
        "Entertainment": ("#e040fb", "#e040fb22"),
        "Other":         ("#64748b", "#64748b22"),
    }

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    with st.form(key="expense_form"):
        # Column headers
        c1, c2, c3 = st.columns([2, 2, 3])
        with c1:
            st.markdown('<div class="col-label">Amount (₹)</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="col-label">Category</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="col-label">Notes</div>', unsafe_allow_html=True)

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount   = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes    = existing_expenses[i]['notes']
            else:
                amount   = 0.0
                category = "Shopping"
                notes    = ""

            col1, col2, col3 = st.columns([2, 2, 3])

            with col1:
                amount_input = st.number_input(
                    label="Amount", min_value=0.0, step=1.0, value=amount,
                    key=f"amount_{i}", label_visibility="collapsed"
                )

            with col2:
                # ✅ FIXED LINE (SAFE INDEX)
                safe_index = categories.index(category) if category in categories else 0

                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=safe_index,
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )

            with col3:
                notes_input = st.text_input(
                    label="Notes", value=notes,
                    key=f"notes_{i}", label_visibility="collapsed",
                    placeholder="Optional note…"
                )

            expenses.append({
                'amount':   amount_input,
                'category': category_input,
                'notes':    notes_input
            })

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        col_btn, col_hint = st.columns([1, 3])
        with col_btn:
            submit_button = st.form_submit_button("Save Expenses")
        with col_hint:
            st.markdown(
                '<div style="font-size:0.75rem;color:#333355;padding-top:0.65rem;">'
                'Rows with ₹0 amount are ignored</div>',
                unsafe_allow_html=True
            )

        if submit_button:
            filtered_expenses = [e for e in expenses if e['amount'] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success(f"✓  {len(filtered_expenses)} expense(s) saved for {selected_date}")
            else:
                st.error("Failed to update expenses. Check your connection.")

    # ── Live preview of current entries ──
    filled = [e for e in expenses if e['amount'] > 0] if 'expenses' in dir() else []
    if filled:
        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:\'Syne\',sans-serif;font-size:0.7rem;font-weight:700;'
            'text-transform:uppercase;letter-spacing:0.12em;color:#555577;margin-bottom:0.8rem;">'
            'Preview</div>',
            unsafe_allow_html=True
        )

        total = sum(e['amount'] for e in filled)
        cols = st.columns(min(len(filled), 5))

        for idx, (col, exp) in enumerate(zip(cols, filled)):
            fg, bg = CAT_COLORS.get(exp['category'], ("#e8e8f0", "#1e1e2e"))
            with col:
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {fg}33;border-radius:10px;
                            padding:0.75rem 1rem;text-align:center;">
                  <div style="font-size:0.65rem;color:{fg};font-weight:700;
                              text-transform:uppercase;letter-spacing:0.1em;
                              margin-bottom:4px;">{exp['category']}</div>
                  <div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                              font-weight:800;color:#e8e8f0;">₹{exp['amount']:,.0f}</div>
                  {f'<div style="font-size:0.7rem;color:#555577;margin-top:3px;">{exp["notes"]}</div>' if exp['notes'] else ''}
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:0.8rem;text-align:right;
                    font-family:'Syne',sans-serif;font-size:0.85rem;color:#555577;">
            Total &nbsp;
            <span style="font-size:1.1rem;font-weight:800;
                         background:linear-gradient(135deg,#6c63ff,#e040fb);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text;">₹{total:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)