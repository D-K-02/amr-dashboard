import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Page config
st.set_page_config(page_title="AMR Dashboard", layout="wide")

# Load external CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1UTx-ca3iv3KPWgkc6LBqSlX8Q-CAvvRW"
    df = pd.read_csv(url)
    df.fillna("", inplace=True)
    df["Year"] = df["Pub_Date"].astype(str).str[:4]
    return df

df = load_data()
# Custom fixed header + navbar
tab = st.query_params.get("tab", "home") # ← Already present

st.markdown(f"""
<div class="custom-header">
    <h1 class="tool-name">AMR-Viz</h1>
    <div class="navbar">
        <a href="/?tab=home" class="nav-item {'active' if tab == 'home' else ''}">Home</a>
        <a href="/?tab=stats" class="nav-item {'active' if tab == 'stats' else ''}">Statistics</a>
        <a href="/?tab=about" class="nav-item {'active' if tab == 'about' else ''}">About</a>
        <a href="/?tab=contact" class="nav-item {'active' if tab == 'contact' else ''}">Contact</a>
    </div>
    <div class="bottom-accent"></div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.main-content-wrapper {
    margin-top: 60px;       /* Pushes content below the fixed header */
    padding: 0 40px;         /* Adds spacing from left and right sides */
}
</style>
<div class="main-content-wrapper">
""", unsafe_allow_html=True)

# --------- Page: HOME ----------
if tab == "home":
    st.markdown("""
    <div class="home-container">
        <h2> Antimicrobial Resistance (AMR)</h2>
        <p>
        Antimicrobial resistance (AMR) is a global health crisis where microorganisms (like bacteria, fungi, and viruses)
        become resistant to treatment by antimicrobial agents. It results in prolonged illness, higher healthcare costs, and increased mortality.
        </p>
        <p>
        This dashboard allows interactive exploration of scientific articles related to AMR, using techniques such as:
        </p>
        <ul>
            <li>Named Entity Recognition (NER)</li>
            <li>TF-IDF Keyword Extraction</li>
            <li>MeSH Term Word Clouds</li>
            <li>Search by Year or Pathogen</li>
        </ul>
        <h3> Smart Article Search</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        year = st.selectbox("Select Year", ["Any"] + sorted(df["Year"].unique()))
    with col2:
        pathogen = st.text_input("Search by Pathogen", placeholder="e.g., Escherichia coli")

    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Search"):
        filtered = df.copy()
        if year != "Any":
            filtered = filtered[filtered["Year"] == year]
        if pathogen:
            filtered = filtered[filtered["Abstract"].str.contains(pathogen, case=False, na=False)]

        st.success(f" Found {len(filtered)} matching articles")
        st.dataframe(filtered[["Title", "Journal", "PubDate", "Abstract"]].reset_index(drop=True), height=400)
    st.markdown("</div>", unsafe_allow_html=True)

# --------- Page: STATISTICS ----------
elif tab == "stats":
    st.markdown("###  TF-IDF Keyword Frequency")
    if "TopKeyword" in df.columns:
        top_keywords = df["TopKeyword"].value_counts().head(15)
        fig, ax = plt.subplots()
        top_keywords.plot(kind="barh", ax=ax, color="#00bfa6")
        ax.invert_yaxis()
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Keyword")
        st.pyplot(fig)
    else:
        st.info("No TF-IDF keywords available.")

    st.markdown("###  MeSH Term Word Cloud")
    mesh_text = " ".join(df["MeSH_Terms"].dropna().astype(str))
    wordcloud = WordCloud(width=1000, height=400, background_color="white").generate(mesh_text)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

# --------- Page: ABOUT ----------
elif tab == "about":
    st.markdown("""
    <div class="main-content-wrapper">
        <h2> About This Tool</h2>
        <p>
        <strong>AMR Dashboard</strong> is a literature mining and visualization tool designed to analyze PubMed articles related to antimicrobial resistance.
        </p>
        <p>
        It supports exploration of trends, keywords, and semantic features from research articles using:
        </p>
        <ul>
            <li>Interactive article search by year or pathogen</li>
            <li>Keyword frequency and semantic trends</li>
            <li>Named entity recognition (NER)</li>
            <li>MeSH term cloud and statistical visualization</li>
        </ul>
        <p>
        Built using <strong>Python</strong>, <strong>Streamlit</strong>, <strong>Pandas</strong>, <strong>NLTK</strong>, and <strong>WordCloud</strong>.
        </p>
        <p>
        <strong>Author:</strong> [Your Name or Organization] <br>
        <strong>Contact:</strong> [Optional Email or GitHub] <br>
        <strong>Dataset:</strong> Extracted from PubMed using Entrez API
        </p>
    </div>
    """, unsafe_allow_html=True)


# --------- Page: CONTACT ----------
elif tab == "contact":
    st.markdown("###  Contact Us")
    st.markdown("Fill out the form below to reach us with your queries or feedback:")
    st.components.v1.iframe(
        src="https://docs.google.com/forms/d/e/1FAIpQLScPHH2Xat1e5_Z80yocEuHGVv4YHhioUdsK7EiPoZSmjXr7ew/viewform?embedded=true",
        height=1700,
        width=800
    )
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="fixed-footer">© 2025 AMR Dashboard</div>', unsafe_allow_html=True)
