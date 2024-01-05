import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_volcano_plot(df, pvalue_col, log2foldchange_col, top_n, dot_size, alpha, title, annotation_fontsize, save_path=None):
    # Calculate -log10 of p-values
    df['minus_log10_pvalue'] = -np.log10(df[pvalue_col])

    # Create a volcano plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df[log2foldchange_col], df['minus_log10_pvalue'], alpha=alpha, s=dot_size)

    # Highlight top N genes
    top_genes = df.nlargest(top_n, 'minus_log10_pvalue')
    plt.scatter(top_genes[log2foldchange_col], top_genes['minus_log10_pvalue'], color='red', alpha=alpha, s=dot_size)

    # Annotate top N genes
    for i, row in top_genes.iterrows():
        plt.text(row[log2foldchange_col], row['minus_log10_pvalue'], i, fontsize=annotation_fontsize)

    # Add labels and title
    plt.xlabel('Log2 Fold Change', fontsize= 16)
    plt.ylabel('-Log10 p-value', fontsize = 16)
    plt.title(title, fontsize = 14)

    # Save the plot if a save path is provided
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    # Show the plot
    st.pyplot(plt)

# Streamlit app layout
st.title('Volcano Plot Generator')

# File upload
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=0)

    # User inputs for column names and plot title
    pvalue_col = st.sidebar.selectbox('Select p-value column', df.columns)
    log2foldchange_col = st.sidebar.selectbox('Select log2 fold change column', df.columns)
    plot_title = st.sidebar.text_input('Enter title for the plot', 'My Volcano Plot')

    # Sliders for dot size, alpha, and annotation font size
    dot_size = st.sidebar.slider('Dot size', min_value=1, max_value=100, value=20)
    alpha = st.sidebar.slider('Dot transparency (alpha)', min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    annotation_fontsize = st.sidebar.slider('Annotation Font Size for Top Genes', min_value=4, max_value=20, value=7)

    # Number of top genes to highlight
    top_n = st.sidebar.slider('Number of top genes to highlight', min_value=1, max_value=50, value=20)

    if st.button('Generate Volcano Plot'):
        create_volcano_plot(df, pvalue_col, log2foldchange_col, top_n, dot_size, alpha, plot_title, annotation_fontsize)

    # Option to save the plot
    save_fig = st.checkbox('Save plot as a file')
    if save_fig:
        save_path = st.text_input('Enter a file path to save the plot', 'volcano_plot.png')
        if st.button('Save Plot'):
            create_volcano_plot(df, pvalue_col, log2foldchange_col, top_n, dot_size, alpha, plot_title, annotation_fontsize, save_path)
            st.success(f'Plot saved as {save_path}')
