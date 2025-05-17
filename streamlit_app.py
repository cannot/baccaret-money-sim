import streamlit as st import pandas as pd

st.title("จำลองการเดินเงินบาคาร่าแบบ 4 ไม้ (เพิ่มรอบได้)")

base_unit = st.number_input("กรอกจำนวนเงินเริ่มต้น (บาท)", min_value=1, value=100)

เก็บผลแต่ละรอบไว้ใน session_state

if "round_results" not in st.session_state: st.session_state.round_results = []

strategies = { "Fibonacci": [1, 2, 4, 8], "Martingale": [1, 2, 4, 8], "Paroli": [1, 2, 4, 0], "Labouchere": [1, 2, 3, 4], "Oscar's Grind": [1, 1, 2, 2] }

st.subheader("📥 กรอกผลรอบนี้ (0 = แพ้ทั้งหมด, 1–4 = ชนะไม้ที่)") current_result = st.number_input("ผลรอบนี้", min_value=0, max_value=4, value=1, step=1)

if st.button("➕ เพิ่มรอบใหม่"): st.session_state.round_results.append(current_result)

if st.button("🗑 ล้างข้อมูลทั้งหมด"): st.session_state.round_results.clear()

แสดงผลแต่ละสูตร

summary_data = [] tabs = st.tabs(list(strategies.keys()))

for strat_name, pattern in strategies.items(): data = [] for idx, win_at in enumerate(st.session_state.round_results): bets = [base_unit * x for x in pattern] if win_at == 0 or win_at > 4: total = sum(bets) profit = -total label = "แพ้ทั้งหมด" else: total = sum(bets[:win_at]) profit = bets[win_at - 1] label = f"ชนะไม้ {win_at}" data.append({ "รอบ": idx + 1, "ผลรอบ": label, "เดิมพันรวม": total, "กำไร/ขาดทุน": profit }) summary_data.append({ "สูตร": strat_name, "รอบ": idx + 1, "กำไร": profit })

df = pd.DataFrame(data)
if not df.empty:
    df.loc["รวม"] = ["", "", df["เดิมพันรวม"].sum(), df["กำไร/ขาดทุน"].sum()]
with tabs[list(strategies.keys()).index(strat_name)]:
    st.dataframe(df, use_container_width=True)

สรุปรวมทุกสูตร

if summary_data: st.subheader("📊 สรุปเปรียบเทียบกำไรแต่ละสูตร") df_summary = pd.DataFrame(summary_data) df_summary = df_summary.groupby("สูตร").agg({"กำไร": ["count", "sum", "mean"]}).reset_index() df_summary.columns = ["สูตร", "จำนวนรอบ", "กำไรรวม", "กำไรเฉลี่ย"] st.dataframe(df_summary, use_container_width=True) else: st.info("กรุณากรอกผลรอบแรกและกดเพิ่มรอบใหม่")

