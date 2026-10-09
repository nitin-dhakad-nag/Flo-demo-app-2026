import streamlit as st

st.markdown("""
<style>
	[data-testid="stChatInput"] > div {
		min-height: 4.1rem;
		padding: 0.55rem 0.5rem 0.55rem 1rem;
	}

	[data-testid="stChatInput"] textarea {
		min-height: 2.8rem !important;
	}

	[data-testid="stChatInput"] button {
		width: 2.8rem;
		height: 2.8rem;
	}
</style>
""", unsafe_allow_html=True)

workshop_page = st.Page("pages/workshop.py", title="The Prompt Heist", default=True)
stats_page = st.Page("pages/stats.py", title="Workshop Stats", url_path="stats")

st.navigation([workshop_page, stats_page], position="hidden").run()
