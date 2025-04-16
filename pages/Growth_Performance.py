import streamlit as st
import pandas as pd
import os

GROWTH_PATH = "data/growth_performance.csv"

st.set_page_config(page_title="Growth Performance Entry", layout="wide")
st.title("📈 Growth Performance Entry")

# ========== 实验基本信息 ==========
st.subheader("📌 Experiment Metadata")

experiment_id = st.text_input("Experiment ID")
group_id = st.text_input("Group ID")
cage_id = st.text_input("Cage ID")

start_day = st.number_input("Start Day", step=1)
end_day = st.number_input("End Day", step=1)

# ========== 生长性能数据 ==========
st.subheader("📊 Growth Performance Inputs")

feed_intake = st.number_input("Total Feed Intake (g)", step=1.0)
bwg = st.number_input("Body Weight Gain (g)", step=1.0)

# 自动计算
days = max(end_day - start_day + 1, 1)
adfi = feed_intake / days if feed_intake else 0
fcr = feed_intake / bwg if bwg else 0

st.markdown(f"**📌 ADFI (Average Daily Feed Intake)**: `{adfi:.2f} g/day`")
st.markdown(f"**📌 FCR (Feed Conversion Ratio)**: `{fcr:.3f}`")

# ========== 保存 ==========
if st.button("✅ Save Record"):
    record = {
        "Experiment_ID": experiment_id,
        "Group_ID": group_id,
        "Cage_ID": cage_id,
        "Start_Day": start_day,
        "End_Day": end_day,
        "Feed_Intake_g": feed_intake,
        "BWG_g": bwg,
        "ADFI_g_per_day": round(adfi, 3),
        "FCR": round(fcr, 3)
    }

    df = pd.DataFrame([record])
    if os.path.exists(GROWTH_PATH):
        df.to_csv(GROWTH_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(GROWTH_PATH, index=False)

    st.success("Growth performance record saved successfully.")

# ========== 历史记录 ==========
st.subheader("📂 Saved Growth Records")
if os.path.exists(GROWTH_PATH):
    df_prev = pd.read_csv(GROWTH_PATH)
    st.dataframe(df_prev)
else:
    st.info("No records found.")

# ========== 删除功能 ==========
st.subheader("🗑️ Delete Growth Performance Record")

if os.path.exists(GROWTH_PATH):
    df_prev = pd.read_csv(GROWTH_PATH)

    if not df_prev.empty:
        df_prev["Preview"] = (
                "Exp:" + df_prev["Experiment_ID"].astype(str) +
                ", Cage:" + df_prev["Cage_ID"].astype(str) +
                ", Days:" + df_prev["Start_Day"].astype(str) + "-" + df_prev["End_Day"].astype(str)
        )
        selected_idx = st.selectbox("Select a record to delete", df_prev["Preview"].tolist())

        if st.button("❌ Delete Selected Record"):
            index_to_drop = df_prev[df_prev["Preview"] == selected_idx].index[0]
            df_prev = df_prev.drop(index_to_drop).drop(columns=["Preview"])
            df_prev.to_csv(GROWTH_PATH, index=False)
            st.success("Record deleted. Please refresh.")

