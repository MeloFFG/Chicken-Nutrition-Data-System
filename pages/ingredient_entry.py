import streamlit as st
import pandas as pd
import os

# ------------------------
# 路径配置
# ------------------------
DB_PATH = "data/ingredient_db.csv"

# ------------------------
# 页面设置
# ------------------------
st.set_page_config(page_title="Ingredient Library", layout="wide")
st.title("Ingredient Library Management")


# ------------------------
# 添加新原料表单（完整字段）
# ------------------------
with st.expander("Add New Ingredient to Database"):
    st.subheader("New Ingredient Entry")

    # 原料名称
    new_name = st.text_input("Ingredient Name")

    # 加载字段列表（手动写死或从 CSV 读）
    all_fields = [
        "kcal/g", "Dry matter, %", "Overall", "NDF, %", "ADF,%", "NFC,%",
        "Crude fiber, %", "Starch, %", "CP, %", "Arginine, %", "Histidine, %",
        "Isoleucine, %", "Leucine, %", "Lysine, %", "Methionine, %", "Phenylalanine, %",
        "Threonine, %", "Tryptophan, %", "Valine, %", "Alanine, %", "Aspartic acid, %",
        "Cystine, %", "Met + Cys, %", "Glutamic acid, %", "Glycine,%", "Proline,%",
        "Serine, %", "Tyrosine, %", "Phe + Tyr, %", "Ether extract, %", "SFA, %",
        "MUFA, %", "PUFA, %", "n-3 PUFA, %", "n-6 PUFA, %", "n-3/n-6 ratio", "C14:0, %",
        "C15:0, %", "C15:1, %", "C16:0, %", "C16:1, %", "C17:0, %", "C17:1, %",
        "C18:0, %", "C18:1, %", "C18:2 cis n-6 (LA), %", "C18:3 cis n-3 (ALA), %",
        "C20:0, %", "C20:1, %", "C20:4n-6 (ARA), %", "C20:5n-3 (EPA), %", "C22:0, %",
        "C22:1, %", "C22:6n-3 (DHA), %", "C24:0, %", "Ash", "Vitamin A",
        "beta-carotene, ppm", "Vitamin D3, ppm", "25(OH)D3", "Vitamin E (as α-tocopherol), ppm",
        "Vitamin K", "Astaxanthin (AST)", "Thiamin (B1), ppm", "Riboflavin (B2), ppm",
        "Niacin (B3), ppm", "Pantothenic acid (B5), ppm", "Pyridoxine (B6), ppm",
        "Biotin (B7), ppm", "Folate (B9), ppm", "Vitamin B12, ppm", "Choline, ppm",
        "Calcium, %", "(Total) Phosphorus, %", "(non-phytate) available P, %",
        "Ca:P ratio", "Na, %", "Cl, %", "K, %", "Mg, %", "S, %", "Cu, ppm", "I, ppm",
        "Fe, ppm", "Mn, ppm", "Se, ppm", "Zn, ppm", "ME, kcal/kg"
    ]

    # 用于保存用户输入的新原料数据
    new_data = {}
    for field in all_fields:
        new_data[field] = st.number_input(field, value=0.0, step=0.001, format="%.6f")

    # 保存操作
    if st.button("Save Ingredient"):
        df = pd.read_csv(DB_PATH)
        new_row = {"Name": new_name}
        new_row.update(new_data)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DB_PATH, index=False)
        st.success(f"Ingredient '{new_name}' added successfully.")


# ------------------------
# 读取原料数据库
# ------------------------
if os.path.exists(DB_PATH):
    df = pd.read_csv(DB_PATH)
    st.success(f"Loaded ingredient database with {len(df)} items.")
else:
    st.error("Ingredient database not found.")
    st.stop()

# ------------------------
# 原料下拉菜单
# ------------------------
ingredient_names = df["Name"].dropna().unique().tolist()
selected_ingredient = st.selectbox("Select an ingredient to view its composition", ingredient_names)

# ------------------------
# 显示所选原料的所有营养信息
# ------------------------
if selected_ingredient:
    st.subheader(f"Nutrient profile for: {selected_ingredient}")
    nutrient_data = df[df["Name"] == selected_ingredient].T.reset_index()
    nutrient_data.columns = ["Nutrient", "Value"]
    st.dataframe(nutrient_data)

# ------------------------
# 强制刷新数据库显示
# ------------------------
st.subheader("Full Ingredient Table (Live)")
df = pd.read_csv(DB_PATH)  # 每次运行时都重新读取最新内容
st.dataframe(df)

# ------------------------
# 删除功能（按原料名删除）
# ------------------------
st.subheader("🗑️ Delete Ingredient")

ingredient_to_delete = st.selectbox("Select an ingredient to delete", ingredient_names, key="delete_box")

if st.button("❌ Delete Selected Ingredient"):
    df = df[df["Name"] != ingredient_to_delete]
    df.to_csv(DB_PATH, index=False)
    st.success(f"Deleted ingredient: {ingredient_to_delete}. Please refresh the page.")
