import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(page_title="Healthcare", layout="wide")
st.title("Healthcare Data Analysis")
st.write("Upload any CSV file. The app auto-detects useful columns and runs simple analysis.")


ALIASES = {
    "age": ["age"],
    "bmi": ["bmi", "bodymassindex"],
    "glucose": ["glucose", "glucoselevel", "sugar"],
    "gender": ["gender", "sex"],
    "disease": ["disease", "diagnosis", "condition"],
    "outcome": ["outcome", "target", "result", "label"],
}


def norm(text: str) -> str:
    return "".join(ch.lower() for ch in str(text) if ch.isalnum())


def find_col(df: pd.DataFrame, key: str):
    name_map = {norm(c): c for c in df.columns}
    for candidate in ALIASES[key]:
        if candidate in name_map:
            return name_map[candidate]
    return None


@st.cache_data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna().copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.lower().str.strip()
    for col in [find_col(df, "age"), find_col(df, "bmi"), find_col(df, "glucose"), find_col(df, "outcome")]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna()


uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if not uploaded_file:
    st.info("Upload a CSV file to begin.")
    st.stop()

raw_df = pd.read_csv(uploaded_file)
df = clean_data(raw_df)

# Fixed, normal chart settings (no sidebar controls)
chart_width = 6
chart_height = 4
chart_dpi = 100
label_rotation = 25
hist_bins = 20
bar_top_n = 15
show_grid = True

age_col = find_col(df, "age")
bmi_col = find_col(df, "bmi")
glucose_col = find_col(df, "glucose")
gender_col = find_col(df, "gender")
disease_col = find_col(df, "disease")
outcome_col = find_col(df, "outcome")

st.subheader("Preview")
st.dataframe(df.head(), use_container_width=True)
st.write("Columns:", df.columns.tolist())

st.subheader("Data Quality")
quality = pd.DataFrame(
    {
        "Metric": ["Rows (raw)", "Rows (clean)", "Columns", "Missing values (raw)", "Duplicate rows (raw)"],
        "Value": [len(raw_df), len(df), raw_df.shape[1], int(raw_df.isna().sum().sum()), int(raw_df.duplicated().sum())],
    }
)
st.dataframe(quality, use_container_width=True)

st.subheader("Basic Analysis")
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
if numeric_cols:
    st.dataframe(df[numeric_cols].agg(["mean", "max", "min"]))
else:
    st.info("No numeric columns found for summary statistics.")

count_col = disease_col or gender_col or (df.select_dtypes(include=["object", "category"]).columns.tolist() or [None])[0]
if count_col:
    st.write(f"Count by {count_col}")
    count_series = df[count_col].value_counts()
    st.write(count_series)
else:
    count_series = None

st.subheader("GroupBy Analysis")
if disease_col and age_col and bmi_col:
    st.write(f"Average {age_col} and {bmi_col} by {disease_col}")
    st.dataframe(df.groupby(disease_col)[[age_col, bmi_col]].mean())
elif count_col and numeric_cols:
    st.write(f"Average numeric values by {count_col}")
    st.dataframe(df.groupby(count_col)[numeric_cols].mean())

if gender_col and glucose_col:
    st.write(f"Average {glucose_col} by {gender_col}")
    st.dataframe(df.groupby(gender_col)[glucose_col].mean().to_frame())

if outcome_col:
    st.write(f"Count by {outcome_col}")
    st.dataframe(df.groupby(outcome_col).size().reset_index(name="Count"))

st.subheader("NumPy Results")
if len(numeric_cols) >= 1:
    n1 = df[numeric_cols[0]].to_numpy()
    st.write(f"{numeric_cols[0]} mean:", np.mean(n1), " | sum:", np.sum(n1))
if len(numeric_cols) >= 2:
    n2 = df[numeric_cols[1]].to_numpy()
    st.write(f"{numeric_cols[1]} mean:", np.mean(n2), " | sum:", np.sum(n2))

if numeric_cols:
    st.subheader("Statistical Analysis")
    if len(numeric_cols) > 1:
        st.write("Correlation matrix")
        st.dataframe(df[numeric_cols].corr().round(3), use_container_width=True)
    if len(numeric_cols) >= 1:
        q1 = df[numeric_cols[0]].quantile(0.25)
        q3 = df[numeric_cols[0]].quantile(0.75)
        iqr = q3 - q1
        outlier_count = int(((df[numeric_cols[0]] < (q1 - 1.5 * iqr)) | (df[numeric_cols[0]] > (q3 + 1.5 * iqr))).sum())
        st.write(f"Outliers in {numeric_cols[0]} (IQR method): {outlier_count}")

cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
if len(cat_cols) >= 2:
    st.write(f"Top combinations: {cat_cols[0]} vs {cat_cols[1]}")
    pairs = df.groupby([cat_cols[0], cat_cols[1]]).size().reset_index(name="Count").sort_values("Count", ascending=False).head(10)
    st.dataframe(pairs, use_container_width=True)

st.subheader("Charts")
if count_series is not None:
    fig1, ax1 = plt.subplots(figsize=(chart_width, chart_height), dpi=chart_dpi)
    count_series.head(bar_top_n).plot(kind="bar", color="teal", ax=ax1)
    ax1.set_title(f"Count by {count_col}")
    ax1.set_xlabel(count_col)
    ax1.set_ylabel("Count")
    ax1.tick_params(axis="x", rotation=label_rotation)
    if show_grid:
        ax1.grid(axis="y", alpha=0.3)
    fig1.tight_layout()
    st.pyplot(fig1)

pie_col = outcome_col or count_col
if pie_col:
    fig2, ax2 = plt.subplots(figsize=(chart_width, chart_height), dpi=chart_dpi)
    df[pie_col].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    ax2.set_title(f"Distribution of {pie_col}")
    fig2.tight_layout()
    st.pyplot(fig2)

if numeric_cols:
    fig3, ax3 = plt.subplots(figsize=(chart_width, chart_height), dpi=chart_dpi)
    df[numeric_cols[0]].plot(kind="hist", bins=hist_bins, color="#4C78A8", ax=ax3)
    ax3.set_title(f"Distribution of {numeric_cols[0]}")
    ax3.set_xlabel(numeric_cols[0])
    if show_grid:
        ax3.grid(axis="y", alpha=0.3)
    fig3.tight_layout()
    st.pyplot(fig3)

if len(numeric_cols) > 1:
    fig4, ax4 = plt.subplots(figsize=(chart_width, chart_width), dpi=chart_dpi)
    corr = df[numeric_cols].corr().values
    im = ax4.imshow(corr, cmap="coolwarm", aspect="auto")
    ax4.set_xticks(range(len(numeric_cols)))
    ax4.set_yticks(range(len(numeric_cols)))
    ax4.set_xticklabels(numeric_cols, rotation=label_rotation, ha="right")
    ax4.set_yticklabels(numeric_cols)
    ax4.set_title("Correlation Heatmap")
    fig4.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)
    fig4.tight_layout()
    st.pyplot(fig4)
