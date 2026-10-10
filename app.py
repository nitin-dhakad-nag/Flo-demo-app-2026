import streamlit as st

st.markdown("""
<style>

/* Streamlit changes the sidebar-toggle markup between desktop/mobile builds. */
[data-testid="stHeader"] button,
[data-testid="stHeader"] button *,
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"] *,
button[aria-label="Open sidebar"],
button[aria-label="Open sidebar"] *,
button[aria-label="Close sidebar"],
button[aria-label="Close sidebar"] * {
	color: #fff !important;
	opacity: 1 !important;
}
[data-testid="stHeader"] button svg,
[data-testid="stHeader"] button svg *,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg *,
button[aria-label="Open sidebar"] svg,
button[aria-label="Open sidebar"] svg *,
button[aria-label="Close sidebar"] svg,
button[aria-label="Close sidebar"] svg * {
	fill: #fff !important;
	stroke: #fff !important;
}

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
