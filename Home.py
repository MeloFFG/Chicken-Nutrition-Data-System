import streamlit as st

st.set_page_config(page_title="Chicken Nutrition Data System", layout="wide")
st.title("🐔 Chicken Nutrition Experiment System")

st.markdown("""
Welcome to the **Chicken Nutrition Data Entry App**.  
This system is designed to help you record, manage, and prepare nutrition-related experimental data for AI modeling.

---

### 📁 Available Modules (see sidebar to access):

- 📝 **Diet Entry**  
  Record feed composition by day range for each group.

- 🧬 **Gene Expression**  
  Input gene expression values for any tissue at specific time points.

- 🩸 **Blood Biomarkers**  
  Record values such as ALT, AST, GLU from blood samples.

- 🧈 **Tissue Fatty Acid**  
  Save fatty acid composition in liver, breast, thigh, etc.

- 📈 **Growth Performance**  
  Record feed intake, body weight gain, and compute ADFI & FCR.

- 📦 **Ingredient Library**  
  Maintain a central database of all raw materials and their nutrients.

---

### 💡 Tips:
- All records are saved into CSV files in the `/data/` folder.
- You can freely switch between pages using the sidebar on the left.
- This structure is designed for downstream AI dataset assembly.

---
""")
