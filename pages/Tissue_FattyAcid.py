import streamlit as st
import pandas as pd
import os

FA_PATH = "data/tissue_fatty_acid.csv"

st.set_page_config(page_title="Tissue Fatty Acid Entry", layout="wide")
st.title("🧈 Tissue Fatty Acid Entry")

# ========== 实验基础信息 ==========
st.subheader("📌 Experiment Metadata")

experiment_id = st.text_input("Experiment ID")
group_id = st.text_input("Group ID")
cage_id = st.text_input("Cage ID")
day = st.number_input("Day of Sampling", step=1)
tissue = st.text_input("Tissue Type (e.g., Breast, Thigh, Liver)")

# ========== 添加脂肪酸条目 ==========
st.subheader("🧪 Add Fatty Acid Record")

if "fa_records" not in st.session_state:
    st.session_state["fa_records"] = []

with st.form("add_fa_form"):
    col1, col2 = st.columns(2)
    with col1:
        fa_name = st.text_input("Fatty Acid Name (e.g., C16:0, C18:1, DHA)")
    with col2:
        fa_value = st.number_input("Fatty Acid Value (%)", format="%.6f", step=0.001)

    submitted = st.form_submit_button("Add FA Record")
    if submitted and fa_name:
        st.session_state["fa_records"].append({
            "Experiment_ID": experiment_id,
            "Group_ID": group_id,
            "Cage_ID": cage_id,
            "Day": day,
            "Tissue": tissue,
            "FA_Name": fa_name,
            "FA_Value": fa_value
        })
        st.success(f"Added: {fa_name} - {fa_value}%")

# ========== 预览本次录入 ==========
st.subheader("🧾 Current Session Records")
if st.session_state["fa_records"]:
    st.dataframe(pd.DataFrame(st.session_state["fa_records"]))

# ========== 保存数据 ==========
if st.button("✅ Save All to File"):
    df_new = pd.DataFrame(st.session_state["fa_records"])
    if os.path.exists(FA_PATH):
        df_old = pd.read_csv(FA_PATH)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(FA_PATH, index=False)
    st.success("All tissue fatty acid records saved.")
    st.session_state["fa_records"] = []

# ========== 查看所有记录 ==========
st.subheader("📂 All Saved Tissue FA Records")
if os.path.exists(FA_PATH):
    df_prev = pd.read_csv(FA_PATH)
    st.dataframe(df_prev)
else:
    st.info("No records saved yet.")

# 删除记录
st.subheader("🗑️ Delete Fatty Acid Record")

if os.path.exists(FA_PATH):
    df_prev = pd.read_csv(FA_PATH)

    if not df_prev.empty:
        df_prev["Preview"] = (
                df_prev["Experiment_ID"].astype(str) +
                " | " +
                df_prev["Cage_ID"].astype(str) +
                " | " +
                df_prev["FA_Name"].astype(str)
        )
        target = st.selectbox("Select a record to delete", df_prev["Preview"].tolist())
        if st.button("❌ Delete Selected"):
            df_prev = df_prev[df_prev["Preview"] != target].drop(columns=["Preview"])
            df_prev.to_csv(FA_PATH, index=False)
            st.success("Deleted. Please refresh.")


