import streamlit as st

from stats_store import get_scoreboard

st.set_page_config(page_title="Workshop Stats", page_icon="📊", layout="wide")

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] { padding-top: 2.5rem; }
[data-testid="stMetric"], [data-testid="stDataFrame"] {
    border: 1px solid rgba(190, 179, 255, 0.22);
    border-radius: 16px;
    background: rgba(22, 24, 74, 0.78);
    box-shadow: 0 12px 34px rgba(4, 5, 32, 0.12);
}
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }
</style>
    """,
    unsafe_allow_html=True,
)

st.title("Workshop scoreboard")
st.caption("Successful breaks are Vulnerable-mode refund recommendations above the 15% limit.")

scoreboard = get_scoreboard()
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
