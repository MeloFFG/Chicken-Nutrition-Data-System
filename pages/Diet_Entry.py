import streamlit as st
import pandas as pd
import os

# 保存路径
DIET_PATH = "data/diet_records.csv"
INGREDIENT_DB = "data/ingredient_db.csv"

# 页面设置
st.set_page_config(page_title="Diet Entry", layout="wide")
st.title("📝 Diet Composition Entry")

# ========== 实验基础信息 ==========
st.subheader("📌 Experiment Metadata")

experiment_id = st.text_input("Experiment ID")
group_id = st.text_input("Group ID (e.g. G1, T1)")
start_day = st.number_input("Start Day", min_value=0, step=1)
end_day = st.number_input("End Day", min_value=0, step=1)

# ========== 原料选择 ==========
st.subheader("🍽️ Select Ingredients and Amounts")

if os.path.exists(INGREDIENT_DB):
    ingredient_df = pd.read_csv(INGREDIENT_DB)
    ingredient_list = ingredient_df["Name"].dropna().unique().tolist()
else:
    st.warning("Ingredient database not found.")
    ingredient_list = []

selected_ingredients = st.multiselect("Select Ingredients", ingredient_list)
ingredient_amounts = {}

for ing in selected_ingredients:
    amount = st.number_input(f"{ing} (g/kg)", step=0.1, key=f"amt_{ing}")
    ingredient_amounts[ing] = amount

# ========== 保存 ==========
if st.button("Save Diet Record"):
    # 必填检查
    if not experiment_id or not group_id:
        st.error("Please fill in both Experiment ID and Group ID.")
    elif start_day > end_day:
        st.error("Start Day must be less than or equal to End Day.")
    elif len(ingredient_amounts) == 0:
        st.error("Please select at least one ingredient.")
    else:
        base_record = {
            "Experiment_ID": experiment_id,
            "Group_ID": group_id,
            "Start_Day": start_day,
            "End_Day": end_day,
        }

        # ✅ 正确添加：列名就是原料名
        for ing, val in ingredient_amounts.items():
            base_record[ing] = val

        df_new = pd.DataFrame([base_record])

        if os.path.exists(DIET_PATH):
            df_old = pd.read_csv(DIET_PATH)

            # ✅ 自动补齐缺的列（避免字段不一致）
            df_combined = pd.concat([df_old, df_new], ignore_index=True).fillna(0)
            df_combined.to_csv(DIET_PATH, index=False)
        else:
            df_new.to_csv(DIET_PATH, index=False)

        st.success("Diet record saved successfully.")

# ========== 删除功能 ==========
st.subheader("🗑️ Delete Diet Record")

if os.path.exists(DIET_PATH):
    try:
        df_prev = pd.read_csv(DIET_PATH)

        if not df_prev.empty:
            df_prev["Preview"] = (
                    "Exp:" + df_prev["Experiment_ID"].astype(str) +
                    ", Group:" + df_prev["Group_ID"].astype(str) +
                    ", Days:" + df_prev["Start_Day"].astype(str) + "-" + df_prev["End_Day"].astype(str)
            )

            selected_preview = st.selectbox("Select a record to delete", df_prev["Preview"].tolist())

            if st.button("❌ Delete Selected Record"):
                idx_to_delete = df_prev[df_prev["Preview"] == selected_preview].index[0]
                df_prev = df_prev.drop(index=idx_to_delete).drop(columns=["Preview"])
                df_prev.to_csv(DIET_PATH, index=False)
                st.success("Record deleted. Please refresh.")
        else:
            st.info("No records available to delete.")
    except pd.errors.EmptyDataError:
        st.warning("Diet record file exists but is empty or corrupted.")
else:
    st.info("No diet record file found.")
