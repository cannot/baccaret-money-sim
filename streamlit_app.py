import streamlit as st
import pandas as pd

st.title("จำลองการเดินเงินบาคาร่าแบบ 4 ไม้")

base_unit = st.number_input("กรอกจำนวนเงินเริ่มต้น (บาท)", min_value=1, value=100)
strategies = {
    "Fibonacci": [1, 2, 4, 8],
    "Martingale": [1, 2, 4, 8],
    "Paroli": [1, 2, 4, 0],
    "Labouchere": [1, 2, 3, 4],
    "Oscar's Grind": [1, 1, 2, 2]
}

st.subheader("📥 กรอกผลแต่ละรอบ (0 = แพ้ทั้งหมด, 1–4 = ชนะไม้ที่)")
results = []
cols = st.columns(5)
for i in range(10):
    with cols[i % 5]:
        val = st.number_input(f"รอบที่ {i+1}", min_value=0, max_value=4, value=1, step=1, key=f"input_{i}")
        results.append(val)

summary_data = []
tabs = st.tabs(list(strategies.keys()))

for strat_name, pattern in strategies.items():
    data = []
    for idx, win_at in enumerate(results):
        bets = [base_unit * x for x in pattern]
        if win_at == 0 or win_at > 4:
            total = sum(bets)
            profit = -total
            label = "แพ้ทั้งหมด"
        else:
            total = sum(bets[:win_at])
            profit = bets[win_at - 1]
            label = f"ชนะไม้ {win_at}"
        data.append({
            "รอบ": idx + 1,
            "ผลรอบ": label,
            "เดิมพันรวม": total,
            "กำไร/ขาดทุน": profit
        })
        summary_data.append({
            "สูตร": strat_name,
            "รอบ": idx + 1,
            "กำไร": profit
        })

    df = pd.DataFrame(data)
    df.loc["รวม"] = ["", "", df["เดิมพันรวม"].sum(), df["กำไร/ขาดทุน"].sum()]
    with tabs[list(strategies.keys()).index(strat_name)]:
        st.dataframe(df, use_container_width=True)

st.subheader("📊 สรุปเปรียบเทียบกำไรแต่ละสูตร")
df_summary = pd.DataFrame(summary_data)
df_summary = df_summary.groupby("สูตร").agg({"กำไร": ["count", "sum", "mean"]}).reset_index()
df_summary.columns = ["สูตร", "จำนวนรอบ", "กำไรรวม", "กำไรเฉลี่ย"]
st.dataframe(df_summary, use_container_width=True)
