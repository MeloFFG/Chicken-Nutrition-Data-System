import streamlit as st
import pandas as pd
import os

GENE_PATH = "data/gene_expression.csv"

st.set_page_config(page_title="Gene Expression Entry", layout="wide")
st.title("🧬 Gene Expression Entry (Flexible)")

# ========== 实验基础信息 ==========
st.subheader("📌 Experiment Metadata")

experiment_id = st.text_input("Experiment ID")
group_id = st.text_input("Group ID")
cage_id = st.text_input("Cage ID")
day = st.number_input("Day of Sampling", step=1)

# ========== 添加表达记录 ==========
st.subheader("🧬 Add Gene Expression Record")

if "gene_records" not in st.session_state:
    st.session_state["gene_records"] = []

with st.form("add_gene_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        gene = st.text_input("Gene Name")
    with col2:
        tissue = st.text_input("Tissue (e.g., Liver, Breast)")
    with col3:
        expr = st.number_input("Expression Level", format="%.6f", step=0.001)

    submitted = st.form_submit_button("Add Record")
    if submitted and gene and tissue:
        st.session_state["gene_records"].append({
            "Experiment_ID": experiment_id,
            "Group_ID": group_id,
            "Cage_ID": cage_id,
            "Day": day,
            "Gene": gene,
            "Tissue": tissue,
            "Expression": expr
        })
        st.success(f"Added: {gene} in {tissue} - {expr}")

# ========== 预览所有添加记录 ==========
st.subheader("🧾 Current Session Records")
if st.session_state["gene_records"]:
    st.dataframe(pd.DataFrame(st.session_state["gene_records"]))

# ========== 保存到文件 ==========
if st.button("✅ Save All to File"):
    df_new = pd.DataFrame(st.session_state["gene_records"])
    if os.path.exists(GENE_PATH):
        df_old = pd.read_csv(GENE_PATH)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(GENE_PATH, index=False)
    st.success("All gene expression records saved.")
    st.session_state["gene_records"] = []

# ========== 查看已保存记录 ==========
st.subheader("📂 All Saved Gene Expression Data")
if os.path.exists(GENE_PATH):
    df_prev = pd.read_csv(GENE_PATH)
    st.dataframe(df_prev)
else:
    st.info("No records saved yet.")


# 删除记录
st.subheader("🗑️ Delete Gene Expression Record")

if os.path.exists(GENE_PATH):
    df_prev = pd.read_csv(GENE_PATH)

    if not df_prev.empty:
        df_prev["Preview"] = (
                df_prev["Experiment_ID"].astype(str) +
                " | " +
                df_prev["Cage_ID"].astype(str) +
                " | " +
                df_prev["Gene"].astype(str)
        )
        target = st.selectbox("Select a record to delete", df_prev["Preview"].tolist())
        if st.button("❌ Delete Selected"):
            df_prev = df_prev[df_prev["Preview"] != target].drop(columns=["Preview"])
            df_prev.to_csv(GENE_PATH, index=False)
            st.success("Deleted. Please refresh.")

