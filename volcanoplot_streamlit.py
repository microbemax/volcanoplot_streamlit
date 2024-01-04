import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_volcano_plot(df, pvalue_col, log2foldchange_col, top_n, pvalue_threshold):
    # Calculate -log10 of p-values
    df['minus_log10_pvalue'] = -np.log10(df[pvalue_col])

    # Create a volcano plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df[log2foldchange_col], df['minus_log10_pvalue'], alpha=0.5)

    # Highlight top N genes
    top_genes = df.nlargest(top_n, 'minus_log10_pvalue')
    plt.scatter(top_genes[log2foldchange_col], top_genes['minus_log10_pvalue'], color='red', alpha=0.5)

    # Annotate top N genes
    for i, row in top_genes.iterrows():
        plt.text(row[log2foldchange_col], row['minus_log10_pvalue'], i, fontsize=6.5)

    # Add labels and title
    plt.xlabel('Log2 Fold Change')
    plt.ylabel('-Log10 p-value')
    plt.title('Volcano Plot')

    # Show the plot
    st.pyplot(plt)

# Streamlit app layout
st.title('Volcano Plot Generator')

# File upload
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=0)

    # User inputs for column names
    pvalue_col = st.selectbox('Select p-value column', df.columns)
    log2foldchange_col = st.selectbox('Select log2 fold change column', df.columns)

    # Number of top genes to highlight and p-value threshold
    top_n = st.slider('Number of top genes to highlight', min_value=1, max_value=100, value=20)
    pvalue_threshold = st.slider('P-value threshold', min_value=0.0001, max_value=0.05, value=0.01, step=0.0001)

    if st.button('Generate Volcano Plot'):
        create_volcano_plot(df, pvalue_col, log2foldchange_col, top_n, pvalue_threshold)
