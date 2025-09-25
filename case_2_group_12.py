#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df1 = pd.read_csv("Stress_Dataset.csv")
df2 = pd.read_csv("StressLevelDataset.csv")
df = pd.concat([df1, df2], ignore_index=True)

st.header("📊 Summary Statistics")


st.write("### Summary Statistics")
styled_table = df.describe().style.background_gradient(cmap="magma").set_caption("Summary Statistics")
st.dataframe(styled_table)  # Streamlit can render pandas Styler objects


st.write("### Correlation Heatmap")
fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(
    df[['sleep_quality','stress_level','study_load','self_esteem']].corr(),
    annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax
)
st.pyplot(fig)


st.write("### Distribution of sleep quality per stress level")
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(data=df, x="sleep_quality", hue="stress_level", ax=ax)
st.pyplot(fig)


st.write("### Distribution of study load per self-image")
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(data=df, x="study_load", hue="self_esteem", ax=ax)
st.pyplot(fig)

st.write(f"**Aantal rijen en kolommen:** {df.shape[0]} rijen, {df.shape[1]} kolommen")



bullying_map = {0: "never bullied", 1: "rarely bullied",2: "sometimes bullied",3: "regularly bullied",4: "bullied often",5: "bullied very often"}

df["bullying_label"] = df["bullying"].map(bullying_map)



st.title("Bullying Level vs Stress Level")

bullying_options = [
    "never bullied",
    "rarely bullied",
    "sometimes bullied",
    "regularly bullied",
    "bullied often",
    "bullied very often"
]


df_filtered = df.dropna(subset=["bullying_label"])

selected_bullying = st.selectbox(
    "Select a bullying level:",
    bullying_options
)

filtered_df = df_filtered[df_filtered["bullying_label"] == selected_bullying]


fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(x="stress_level", data=filtered_df, palette="viridis", ax=ax)
ax.set_title(f"Stress Levels for {selected_bullying}")
st.pyplot(fig)



st.title("📊 Count table")

st.write("Check two variables below to make a scatterplot:")

columns = ["bullying_label", "stress_level", "study_load","sleep_quality"]
selected_vars = [col for col in columns if st.checkbox(col)]


if len(selected_vars) == 2:
    x_var, y_var = selected_vars
    fig, ax = plt.subplots()
    heatmap_data = df.groupby([x_var, y_var]).size().unstack(fill_value=0)
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="Blues")
    st.pyplot(fig)

elif len(selected_vars) < 2:
    st.info("👉 Please select *two variables* to plot.")
else:
    st.warning("⚠️ Please select only *two variables*.")




bullying_labels = [
    "never bullied",
    "rarely bullied",
    "sometimes bullied",
    "regularly bullied",
    "bullied often",
    "bullied very often"
]
df = df.dropna(subset=["self_esteem", "bullying"])  # remove NaNs
df["bullying_label"] = df["bullying"].astype(int).map({
    0: "never bullied",
    1: "rarely bullied",
    2: "sometimes bullied",
    3: "regularly bullied",
    4: "bullied often",
    5: "bullied very often"
})

st.title("Bullying Distribution by Self-Esteem Range")


selfesteem_range = st.slider(
    "Select self-esteem range:",
    min_value=0,
    max_value=30,
    value=(10, 20)  
)


filtered_df = df[(df["self_esteem"] >= selfesteem_range[0]) & 
                 (df["self_esteem"] <= selfesteem_range[1])]


fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(x="bullying_label", data=filtered_df, order=bullying_labels, palette="viridis", ax=ax)
ax.set_title(f"Bullying Distribution for Self-Esteem {selfesteem_range[0]}–{selfesteem_range[1]}")
ax.set_xlabel("Bullying Level")
ax.set_ylabel("Count")
plt.xticks(rotation=30)
st.pyplot(fig)


# In[ ]:







