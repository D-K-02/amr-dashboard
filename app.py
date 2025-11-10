import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="AMR Dashboard", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
@st.cache_data
def load_data():
    csv_url = "https://figshare.com/ndownloader/files/59436200" 
    df = pd.read_csv(csv_url, low_memory=False, dtype=str)
    df.columns = df.columns.str.strip()  # Removes extra spaces
    df.fillna("", inplace=True)
    df["Year"] = df["PubDate"].astype(str).str[:4]
    return df

df = load_data()

# Store entire data and filtered data in session_state
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df

# Custom header (only tool name here)
st.markdown("""
<div class="custom-header">
    <h1 class="tool-name">AMR Curator</h1>
</div>
""", unsafe_allow_html=True)

# Navigation stays as Streamlit tabs
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Statistics", "About", "Contact"])

with tab1:
    st.markdown("""
    <div class="home-container">
        <h2> Antimicrobial Resistance (AMR)</h2>
        <p>
        Antimicrobial resistance (AMR)  is a growing global health crisis where microorganisms — such as bacteria, fungi, and viruses — evolve to resist treatment by antimicrobial agents. This leads to prolonged illness, higher healthcare costs, and increased mortality.
        </p>
        <p>
            Our dashboard leverages <strong>Natural Language Processing (NLP)</strong> to automatically analyze and enrich scientific literature on AMR.
        This enriched dataset allows researchers to quickly identify key topics, trends, and entities by interactive exploration of scientific articles related to AMR, using techniques such as:
        </p>
        <ul>
            <li>Named Entity Recognition (NER)</li>
            <li>TF-IDF Keyword Extraction</li>
            <li>MeSH Term Word Clouds</li>
        </ul>
        <h3> Smart Article Search</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        year = st.selectbox("Select Year", ["Any"] + sorted(df["Year"].unique()))
    with col2:
        pathogen = st.text_input("Select Pathogen", placeholder="e.g., E. coli")

    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Search"):
        filtered = df.copy()
        if year != "Any":
            filtered = filtered[filtered["Year"] == year]
        if pathogen:
            filtered = filtered[filtered["Abstract"].str.contains(pathogen, case=False, na=False)]
        st.session_state.filtered_df = filtered  # <--- Save the filtered results to session state!
        st.success(f"Found {len(filtered)} matching articles")
        st.dataframe(filtered[["Title", "Journal", "PubDate", "Abstract"]].reset_index(drop=True), height=400)
    else:
        # Show the most recent search results (if any)
        filtered = st.session_state.filtered_df
        st.dataframe(filtered[["Title", "Journal", "PubDate", "Abstract"]].reset_index(drop=True), height=400)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<h3 class="custom-heading"> TF-IDF Keyword Frequency</h3>', unsafe_allow_html=True)
    filtered = st.session_state.filtered_df  # <-- Use filtered results!
    if "TopKeyword" in filtered.columns:
        top_keywords = filtered["TopKeyword"].value_counts().head(15)
        fig, ax = plt.subplots()
        top_keywords.plot(kind="barh", ax=ax, color="#A4B6BB")
        ax.invert_yaxis()
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Keyword")
        st.pyplot(fig)
    else:
        st.info("No TF-IDF keywords available for the current search results.")

    st.markdown('<h3 class="custom-heading"> MeSH Term Word Cloud</h3>', unsafe_allow_html=True)
    mesh_text = " ".join(filtered["MeSH_Terms"].dropna().astype(str))
    if mesh_text.strip():
        wordcloud = WordCloud(width=900, height=400, background_color="white").generate(mesh_text)
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wordcloud, interpolation="bilinear")
        ax_wc.axis("off")
        st.pyplot(fig_wc)
    else:
        st.info("No MeSH Terms available for the current search results.")

with tab3:
    st.markdown("""
    <div class="main-content-wrapper">
        <h2> About This Tool</h2>
        <p>
        <strong>AMR Curator</strong> is a  literature mining and visualization platform, built to accelerate discovery in antimicrobial resistance (AMR) research. By utilising <strong>Python</strong> for data processing, it provides an interactive interface and transforms raw scientific publications into actionable intelligence.
        </p>
        <p>
        Our platform integrates <strong>Natural Language Processing (NLP)</strong> pipelines that automatically extract and enrich data from PubMed articles. By combining Named Entity Recognition (NER), TF-IDF keyword extraction, and MeSH term mapping, each record is transformed into a structured, high-value entry in a <strong>curated AMR knowledgebase</strong>.
        </p>
        <p>
        At the core of this tool is a <strong>curated, enriched dataset</strong> of PubMed articles related to AMR, from last 10 years. It supports exploration of trends, keywords, and semantic features from research articles using:
        </p>
        <ul>
            <li>Interactive article search by year or pathogen</li>
            <li>Keyword frequency and semantic trends</li>
            <li>Named entity recognition (NER)</li>
            <li>MeSH term cloud and statistical visualization</li>
        </ul>
        <p>
        By combining NLP with a clean, accessible interface, the AMR Dashboard empowers researchers, policymakers, and healthcare professionals to uncover patterns, track emerging threats, and focus on the most impactful areas of AMR research.
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown(
        """
        <div style="text-align: center; max-width: 900px; margin: auto;">
            <h3>Contact Us</h3>
            <p>Fill out the form below to reach us with your queries or feedback:</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScPHH2Xat1e5_Z80yocEuHGVv4YHhioUdsK7EiPoZSmjXr7ew/viewform?embedded=true"
                    width="800"
                    height="1700"
                    frameborder="0"
                    marginheight="0"
                    marginwidth="0">
                Loading…
            </iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<div class="fixed-footer">© 2025 AMR Dashboard</div>', unsafe_allow_html=True)


