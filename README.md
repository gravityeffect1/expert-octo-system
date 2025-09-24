# CRISPR Guide RNA Finder

This Streamlit application helps you find CRISPR guide RNAs in a DNA sequence.

## Features

- Upload a DNA sequence in FASTA or plain text format.
- Select a Protospacer Adjacent Motif (PAM) sequence (e.g., NGG).
- Displays a table of guide RNAs with their sequence, position, strand, GC content, and a score.
- Plots the positions of the guide RNAs on the DNA sequence.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
