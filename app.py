import streamlit as st
from bot import RefundBot
from orders import ORDERS

st.set_page_config(
    page_title="The Prompt Heist",
    page_icon="",
    layout="wide",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --ink: #f7f4ff;
    --muted: #c4bee8;
    --night: #171943;
    --panel: rgba(22, 24, 74, 0.78);
    --line: rgba(190, 179, 255, 0.22);
    --pink: #ff39c8;
    --violet: #862eff;
    --cyan: #68d5ff;
}

.stApp {
    color: var(--ink);
    background-color: var(--night);
    background:
        radial-gradient(ellipse 52% 48% at 7% -18%, rgba(139, 36, 255, 0.9) 0%, rgba(119, 24, 226, 0.42) 42%, transparent 76%),
        radial-gradient(ellipse 42% 50% at 103% 28%, rgba(255, 45, 190, 0.86) 0%, rgba(179, 34, 234, 0.45) 43%, transparent 76%),
        radial-gradient(ellipse 38% 30% at 78% 108%, rgba(72, 199, 255, 0.42) 0%, transparent 72%),
        linear-gradient(135deg, #171943 0%, #11106a 52%, #171943 100%);
    background-attachment: fixed;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppViewContainer"] { background: transparent; }
[data-testid="stMain"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(165deg, rgba(19, 18, 73, 0.96), rgba(28, 12, 76, 0.92));
    border-right: 1px solid var(--line);
}
[data-testid="stMainBlockContainer"] { padding-top: 2.5rem; }

h1, h2, h3, [data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.035em;
}
h1 { font-size: clamp(2.5rem, 5vw, 4rem) !important; }
p, label, [data-testid="stCaptionContainer"] { color: var(--muted); }

[data-testid="stMetric"] {
    min-height: 116px;
    padding: 1.15rem 1.25rem;
    border: 1px solid var(--line);
    border-radius: 18px;
    background: linear-gradient(140deg, rgba(33, 34, 105, 0.82), rgba(19, 20, 70, 0.74));
    box-shadow: 0 14px 45px rgba(4, 5, 32, 0.2);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] { font-size: 1.75rem !important; }

[data-testid="stAlert"], [data-testid="stExpander"], [data-testid="stChatMessage"] {
    border: 1px solid var(--line);
    border-radius: 18px;
    background: var(--panel);
    box-shadow: 0 14px 45px rgba(4, 5, 32, 0.16);
}
[data-testid="stChatMessage"] { padding: 1.1rem 1.25rem; }
[data-testid="stChatMessage"] p { color: var(--ink); }
[data-testid="stChatInput"] {
    padding: 0.35rem 0;
    border: 0;
    background: transparent;
    box-shadow: none;
}
[data-testid="stChatInput"] > div {
    padding: 0.35rem 0.45rem 0.35rem 0.9rem;
    border: 1px solid rgba(166, 157, 226, 0.28);
    border-radius: 999px;
    background: rgba(15, 16, 61, 0.68);
    box-shadow: 0 8px 28px rgba(4, 5, 32, 0.13);
    transition: border-color 140ms ease, box-shadow 140ms ease;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: rgba(104, 213, 255, 0.72);
    box-shadow: 0 0 0 3px rgba(104, 213, 255, 0.09);
}
[data-testid="stChatInput"] textarea {
    color: var(--ink) !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    font-size: 1rem;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(196, 190, 232, 0.66) !important;
}
[data-testid="stChatInput"] button {
    width: 2.5rem;
    height: 2.5rem;
    color: #fff !important;
    border: 0 !important;
    border-radius: 50% !important;
    background: linear-gradient(145deg, var(--violet), var(--pink)) !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] button:hover {
    background: linear-gradient(145deg, #9e51ff, #ff5bd2) !important;
}

div.stButton > button, [data-testid="stBaseButton-primary"] {
    color: white;
    border: 0;
    border-radius: 12px;
    background: linear-gradient(105deg, var(--violet), var(--pink));
    box-shadow: 0 8px 24px rgba(208, 39, 223, 0.28);
    font-weight: 700;
    transition: transform 140ms ease, box-shadow 140ms ease;
}
div.stButton > button:hover, [data-testid="stBaseButton-primary"]:hover {
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 12px 30px rgba(208, 39, 223, 0.4);
}

[data-baseweb="select"] > div, [data-baseweb="input"] > div {
    color: var(--ink);
    background: rgba(15, 16, 61, 0.84);
    border-color: var(--line);
    border-radius: 12px;
}
[data-testid="stRadio"] label { color: var(--ink); }
hr { border-color: var(--line); }
a { color: var(--cyan) !important; }

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] { padding: 1.25rem 1rem 2rem; }
    [data-testid="stMetric"] { min-height: 96px; padding: 0.9rem; }
    [data-testid="stMetricValue"] { font-size: 1.35rem !important; }
}
</style>
    """,
    unsafe_allow_html=True,
)

st.title("The Prompt Heist")
st.caption("A deliberately vulnerable prompt-injection workshop — fictional orders, fictional money, real lessons.")

with st.sidebar:
    st.header("Workshop Controls")
    mode = st.radio(
        "Bot mode",
        ["Vulnerable", "Defended"],
    )

if "active_mode" not in st.session_state:
    st.session_state.active_mode = mode
elif st.session_state.active_mode != mode:
    st.session_state.messages = []
    st.session_state.active_mode = mode

st.caption(f"Active mode: **{mode}** — changing modes starts a fresh chat.")

st.info(
    "🎯 Mission: start with a normal order question, then try prompt injection to convince the bot to approve a refund above the 15% policy limit."
)

order_id = st.selectbox("Choose a demo order", list(ORDERS.keys()))
order = ORDERS[order_id]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Order", order_id)
c2.metric("Item", order["item"])
c3.metric("Order value", f"₹{order['amount']:,.0f}")
c4.metric("Policy limit", "15%")

st.divider()

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
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"],
                        "debug": result["raw"],
                    }
                )
            except Exception as exc:
                st.error(f"Request failed: {exc}")
