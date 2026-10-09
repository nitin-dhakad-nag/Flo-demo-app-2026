import streamlit as st
from bot import RefundBot
from orders import ORDERS
from stats_store import record_successful_bypass

st.set_page_config(page_title="The Prompt Heist", page_icon="", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {
    --ink: #f7f4ff; --muted: #c4bee8; --night: #171943;
    --panel: rgba(22, 24, 74, 0.78); --line: rgba(190, 179, 255, 0.22);
    --pink: #ff39c8; --violet: #862eff; --cyan: #68d5ff;
}
.stApp {
    color: var(--ink); background-color: var(--night);
    background:
        radial-gradient(ellipse 52% 48% at 7% -18%, rgba(139,36,255,.9) 0%, rgba(119,24,226,.42) 42%, transparent 76%),
        radial-gradient(ellipse 42% 50% at 103% 28%, rgba(255,45,190,.86) 0%, rgba(179,34,234,.45) 43%, transparent 76%),
        radial-gradient(ellipse 38% 30% at 78% 108%, rgba(72,199,255,.42) 0%, transparent 72%),
        linear-gradient(135deg, #171943 0%, #11106a 52%, #171943 100%);
    background-attachment: fixed; font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: transparent; }
[data-testid="stBottom"], [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {
    background: transparent !important; border-top: 0 !important; box-shadow: none !important;
}
[data-testid="stBottomBlockContainer"] { max-width: 1120px; padding: .8rem 1.5rem 1.25rem; }
[data-testid="stSidebar"] { background: linear-gradient(165deg, rgba(19,18,73,.96), rgba(28,12,76,.92)); border-right: 1px solid var(--line); }
[data-testid="stMainBlockContainer"] { padding-top: 2.5rem; }
.order-card {
    margin: 1.8rem 0 2rem; padding: 1.4rem 1.6rem;
    border: 1px solid var(--line); border-radius: 18px;
    background: linear-gradient(140deg, rgba(33,34,105,.82), rgba(19,20,70,.74));
    box-shadow: 0 14px 45px rgba(4,5,32,.16);
}
.order-card-heading, .order-details { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.order-card-heading { margin-bottom: .55rem; }
.order-label { color: var(--cyan); font-size: .72rem; font-weight: 700; letter-spacing: .12em; }
.order-id { color: var(--muted); font-size: .9rem; }
.order-item { margin-bottom: 1rem; color: var(--ink); font-family: 'Space Grotesk',sans-serif; font-size: 1.35rem; font-weight: 600; }
.order-details { color: var(--muted); font-size: .92rem; gap: 1.5rem; }
.order-details b { margin-right: .35rem; color: var(--ink); }
h1, h2, h3, [data-testid="stMetricValue"] { color: var(--ink) !important; font-family: 'Space Grotesk',sans-serif !important; letter-spacing: -.035em; }
h1 { font-size: clamp(2.5rem,5vw,4rem) !important; }
p, label, [data-testid="stCaptionContainer"] { color: var(--muted); }
[data-testid="stMetric"] { min-height: 116px; padding: 1.15rem 1.25rem; border: 1px solid var(--line); border-radius: 18px; background: linear-gradient(140deg,rgba(33,34,105,.82),rgba(19,20,70,.74)); box-shadow: 0 14px 45px rgba(4,5,32,.2); }
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] { font-size: 1.75rem !important; }
[data-testid="stAlert"], [data-testid="stExpander"], [data-testid="stChatMessage"] { border: 1px solid var(--line); border-radius: 18px; background: var(--panel); box-shadow: 0 14px 45px rgba(4,5,32,.16); }
[data-testid="stChatMessage"] { padding: 1.1rem 1.25rem; }
[data-testid="stChatMessage"] p { color: var(--ink); }
[data-testid="stChatInput"] { width: 100%; margin: 0 auto; padding: .2rem 0; border: 0; background: transparent; box-shadow: none; }
[data-testid="stChatInput"] > div { padding: .28rem .38rem .28rem .85rem; border: 1px solid rgba(190,179,255,.25); border-radius: 999px; background: rgba(22,24,74,.82); box-shadow: 0 8px 28px rgba(4,5,32,.1); transition: border-color 140ms ease,box-shadow 140ms ease; }
[data-testid="stChatInput"] > div:focus-within { border-color: rgba(104,213,255,.72); box-shadow: 0 0 0 3px rgba(104,213,255,.09); }
[data-testid="stChatInput"] textarea { color: var(--ink) !important; background: transparent !important; border: 0 !important; box-shadow: none !important; font-size: 1rem; }
[data-testid="stChatInput"] > div { min-height: 4.1rem !important; padding: .55rem .5rem .55rem 1rem !important; }
[data-testid="stChatInput"] textarea { min-height: 2.8rem !important; }
[data-testid="stChatInput"] button { width: 2.8rem !important; height: 2.8rem !important; }
[data-testid="stChatInput"] textarea::placeholder { color: rgba(196,190,232,.66) !important; }
[data-testid="stChatInput"] button { width: 2.5rem; height: 2.5rem; color: #fff !important; border: 0 !important; border-radius: 50% !important; background: linear-gradient(145deg,var(--violet),var(--pink)) !important; box-shadow: none !important; }
[data-testid="stChatInput"] button:hover { background: linear-gradient(145deg,#9e51ff,#ff5bd2) !important; }
div.stButton > button, [data-testid="stBaseButton-primary"] { color: white; border: 0; border-radius: 12px; background: linear-gradient(105deg,var(--violet),var(--pink)); box-shadow: 0 8px 24px rgba(208,39,223,.28); font-weight: 700; transition: transform 140ms ease,box-shadow 140ms ease; }
div.stButton > button:hover, [data-testid="stBaseButton-primary"]:hover { color: white; transform: translateY(-1px); box-shadow: 0 12px 30px rgba(208,39,223,.4); }
[data-baseweb="select"] > div, [data-baseweb="input"] > div { color: var(--ink); background: rgba(15,16,61,.84); border-color: var(--line); border-radius: 12px; }
[data-testid="stRadio"] label { color: var(--ink); }
hr { border-color: var(--line); } a { color: var(--cyan) !important; }
@media (max-width:700px) { [data-testid="stMainBlockContainer"] { padding: 1.25rem 1rem 2rem; } [data-testid="stMetric"] { min-height: 96px; padding: .9rem; } [data-testid="stMetricValue"] { font-size: 1.35rem !important; } }
</style>
    """,
    unsafe_allow_html=True,
)

st.title("The Prompt Heist")
st.caption("Prompt injection and guardrails, demonstrated with a fictional order.")

with st.sidebar:
    st.header("Workshop Controls")
    participant_alias = st.text_input(
        "Participant name / alias",
        max_chars=40,
        key="participant_alias",
    )
    mode = st.radio("Bot mode", ["Vulnerable", "Defended"])

if "active_mode" not in st.session_state:
    st.session_state.active_mode = mode
elif st.session_state.active_mode != mode:
    st.session_state.messages = []
    st.session_state.active_mode = mode

order_id = "SE-1001"
order = ORDERS[order_id]
st.markdown(
    f"""
<section class="order-card">
  <div class="order-card-heading"><span class="order-label">DEMO ORDER</span><span class="order-id">{order_id}</span></div>
  <div class="order-item">{order['item']}</div>
  <div class="order-details"><span><b>Order value</b> ₹{order['amount']:,.0f}</span><span><b>Status</b> {order['status']}</span><span><b>Refund limit</b> 15%</span></div>
</section>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about the order, request a refund, or try to bypass the policy…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    bot = RefundBot(defended=(mode == "Defended"))
    with st.chat_message("assistant"):
        with st.spinner("RefundBot is thinking..."):
            try:
                result = bot.respond(
                    order_id=order_id,
                    order=order,
                    history=st.session_state.messages,
                    user_prompt=prompt,
                )
                st.markdown(result["answer"])
                if mode == "Vulnerable" and participant_alias.strip():
                    simulated_bypass = bot._vulnerable_override_decision(
                        st.session_state.messages,
                        prompt,
                    )
                    if simulated_bypass:
                        record_successful_bypass(participant_alias, simulated_bypass["percent"])
                st.session_state.messages.append(
                    {"role": "assistant", "content": result["answer"], "debug": result["raw"]}
                )
            except Exception as exc:
                st.error(f"Request failed: {exc}")
