import streamlit as st
import pandas as pd
import os

BLOOD_PATH = "data/blood_biomarkers.csv"

st.set_page_config(page_title="Blood Biomarker Entry", layout="wide")
st.title("🩸 Blood Biomarkers Entry")

# ========== 实验基础信息 ==========
st.subheader("📌 Experiment Metadata")

experiment_id = st.text_input("Experiment ID")
group_id = st.text_input("Group ID")
cage_id = st.text_input("Cage ID")
day = st.number_input("Day of Sampling", step=1)

# ========== 添加血液指标 ==========
st.subheader("🩸 Add Blood Marker Record")

if "blood_records" not in st.session_state:
    st.session_state["blood_records"] = []

with st.form("add_blood_form"):
    col1, col2 = st.columns(2)
    with col1:
        marker = st.text_input("Marker Name (e.g., ALT, GLU, TG)")
    with col2:
        value = st.number_input("Value", format="%.6f", step=0.001)

    submitted = st.form_submit_button("Add Marker")
    if submitted and marker:
        st.session_state["blood_records"].append({
            "Experiment_ID": experiment_id,
            "Group_ID": group_id,
            "Cage_ID": cage_id,
            "Day": day,
            "Marker": marker,
            "Value": value
        })
        st.success(f"Added: {marker} - {value}")

# ========== 预览当前添加记录 ==========
st.subheader("🧾 Current Session Records")
if st.session_state["blood_records"]:
    st.dataframe(pd.DataFrame(st.session_state["blood_records"]))

# ========== 保存数据 ==========
if st.button("✅ Save All to File"):
    df_new = pd.DataFrame(st.session_state["blood_records"])
    if os.path.exists(BLOOD_PATH):
        df_old = pd.read_csv(BLOOD_PATH)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(BLOOD_PATH, index=False)
    st.success("All blood biomarker records saved.")
    st.session_state["blood_records"] = []

# ========== 展示已保存数据 ==========
st.subheader("📂 All Saved Blood Biomarkers")
if os.path.exists(BLOOD_PATH):
    df_prev = pd.read_csv(BLOOD_PATH)
    st.dataframe(df_prev)
else:
    st.info("No records saved yet.")


# 删除记录
st.subheader("🗑️ Delete Blood Biomarker Record")

if os.path.exists(BLOOD_PATH):
    df_prev = pd.read_csv(BLOOD_PATH)

    if not df_prev.empty:
        df_prev["Preview"] = (
                df_prev["Experiment_ID"].astype(str) +
                " | " +
                df_prev["Cage_ID"].astype(str) +
                " | " +
                df_prev["Marker"].astype(str)
        )
        target = st.selectbox("Select a record to delete", df_prev["Preview"].tolist())
        if st.button("❌ Delete Selected"):
            df_prev = df_prev[df_prev["Preview"] != target].drop(columns=["Preview"])
            df_prev.to_csv(BLOOD_PATH, index=False)
            st.success("Deleted. Please refresh.")

