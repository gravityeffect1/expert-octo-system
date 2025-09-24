import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('static/style.css')

def find_pam(seq, pam):
    pam_regex = pam.replace('N', '[ATCG]')
    guides = []
    for match in re.finditer(f'(?=({pam_regex}))', seq, re.IGNORECASE):
        pam_start = match.start(1)
        if pam_start >= 20:
            guide_start = pam_start - 20
            guides.append({
                "sequence": seq[guide_start:pam_start],
                "start": guide_start,
                "end": pam_start,
                "strand": "forward"
            })
    return guides

def get_reverse_complement(seq):
    complement = str.maketrans('ATCG', 'TAGC')
    return seq.upper().translate(complement)[::-1]

def calculate_gc_content(seq):
    return (seq.count('G') + seq.count('C')) / len(seq) * 100

st.title("CRISPR Dashboard")
st.markdown("""
**Upload a DNA sequence, select a PAM, and see guide RNAs + scores.**

This tool identifies potential guide RNA sequences for CRISPR-Cas9 gene editing. 
It searches for a given Protospacer Adjacent Motif (PAM) and extracts the 20 nucleotides upstream.
""")

uploaded_file = st.file_uploader("Upload your DNA sequence (FASTA or plain text)", type=["txt", "fasta", "fa"])
pam_option = st.selectbox("Select a PAM sequence", ("NGG",))

if uploaded_file is not None:
    sequence = uploaded_file.read().decode("utf-8")
    if sequence.startswith('>'):
        sequence = "".join(sequence.split('\n')[1:])
    
    sequence = sequence.replace('\n', '')

    st.text_area("Sequence", sequence, height=200)

    forward_guides = find_pam(sequence, pam_option)
    reverse_complement_sequence = get_reverse_complement(sequence)
    reverse_guides_raw = find_pam(reverse_complement_sequence, pam_option)

    reverse_guides = []
    for guide in reverse_guides_raw:
        reverse_guides.append({
            "sequence": guide["sequence"],
            "start": len(sequence) - guide["end"],
            "end": len(sequence) - guide["start"],
            "strand": "reverse"
        })

    all_guides = forward_guides + reverse_guides

    if all_guides:
        df = pd.DataFrame(all_guides)
        df['gc_content'] = df['sequence'].apply(calculate_gc_content)
        df['score'] = df['gc_content'].apply(lambda gc: 1 - abs(gc - 50) / 50)
        
        st.write("Found Guide RNAs:")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 2))
        ax.plot([0, len(sequence)], [0, 0], 'k-')
        for _, row in df.iterrows():
            color = 'r' if row['strand'] == 'forward' else 'b'
            ax.plot([row['start'], row['end']], [0, 0], color=color, linewidth=4)

        ax.set_title("Guide Positions")
        ax.set_xlabel("Sequence Position")
        ax.set_yticks([])
        st.pyplot(fig)
    else:
        st.warning("No guide RNAs found for the given PAM sequence.")
else:
    st.info("Awaiting DNA sequence file upload.")
