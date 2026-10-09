import streamlit as st
from datetime import datetime, timezone

from stats_store import get_scoreboard

st.set_page_config(page_title="Workshop Stats", page_icon="📊", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {
    --stats-ink: #f7f4ff;
    --stats-muted: #c4bee8;
    --stats-line: rgba(190, 179, 255, 0.22);
    --stats-panel: rgba(22, 24, 74, 0.82);
    --stats-pink: #ff39c8;
    --stats-violet: #862eff;
    --stats-cyan: #68d5ff;
}
.stApp {
    color: var(--stats-ink);
    background:
        radial-gradient(ellipse 52% 48% at 7% -18%, rgba(139,36,255,.75) 0%, rgba(119,24,226,.3) 42%, transparent 76%),
        radial-gradient(ellipse 42% 50% at 103% 28%, rgba(255,45,190,.68) 0%, rgba(179,34,234,.32) 43%, transparent 76%),
        linear-gradient(135deg, #171943 0%, #11106a 52%, #171943 100%);
    background-attachment: fixed;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] { max-width: 1180px; padding-top: 3rem; }
h1, h2, h3 { color: var(--stats-ink) !important; font-family: 'Space Grotesk', sans-serif !important; }
p, [data-testid="stCaptionContainer"] { color: var(--stats-muted); }
[data-testid="stMetric"] {
    min-height: 128px;
    padding: 1.1rem 1.4rem;
    border: 1px solid var(--stats-line);
    border-radius: 18px;
    background: linear-gradient(140deg, rgba(33,34,105,.86), rgba(19,20,70,.82));
    box-shadow: 0 14px 40px rgba(4,5,32,.18);
}
[data-testid="stMetricLabel"] { color: var(--stats-muted) !important; font-size: .95rem; }
[data-testid="stMetricValue"] { color: var(--stats-ink) !important; font-family: 'Space Grotesk',sans-serif !important; font-size: 2.8rem !important; }
[data-testid="stAlert"] {
    color: var(--stats-muted);
    border: 1px solid var(--stats-line);
    border-radius: 16px;
    background: var(--stats-panel);
}
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p { color: var(--stats-muted); }
[data-testid="stDataFrame"] {
    overflow: hidden;
    border: 1px solid var(--stats-line);
    border-radius: 16px;
    background: var(--stats-panel);
}
[data-testid="stExpander"] {
    border: 1px solid var(--stats-line);
    border-radius: 16px;
    background: var(--stats-panel);
}
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] { padding: 1.5rem 1rem; }
    [data-testid="stMetric"] { min-height: 100px; }
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; }
}
</style>
    """,
    unsafe_allow_html=True,
)

st.title("Workshop scoreboard")
st.caption("Successful breaks are Vulnerable-mode refund recommendations above the 15% limit. Auto-refreshes every 5 seconds.")

@st.fragment(run_every=5)
def render_live_scoreboard():
    scoreboard = get_scoreboard()
    st.caption(f"Last updated: {datetime.now(timezone.utc).strftime('%H:%M:%S')} UTC")
    st.metric("Successful breaks", scoreboard["total_successful_breaks"])

    if scoreboard["participants"]:
        st.subheader("Participants")
        st.dataframe(
            [
                {
                    "Participant": row["participant_alias"],
                    "Successful breaks": row["successful_breaks"],
                    "Highest recommendation": f"{row['highest_percent']:.1f}%",
                    "Latest (UTC)": row["latest_at"],
                }
                for row in scoreboard["participants"]
            ],
            use_container_width=True,
            hide_index=True,
        )

        with st.expander("Recent successful breaks"):
            st.dataframe(
                [
                    {
                        "Participant": row["participant_alias"],
                        "Recommendation": f"{row['refund_percent']:.1f}%",
                        "Time (UTC)": row["created_at"],
                    }
                    for row in scoreboard["recent"]
                ],
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No successful breaks recorded yet.")


render_live_scoreboard()
