import streamlit as st
from scoper import analyze_brief

st.set_page_config(page_title="Cynbit AI Project Scoper", layout="wide")
st.title("Cynbit Project Scoper")
st.caption("Paste a client brief. Get back a scope, an hours range, the risks, and what to ask before you quote.")

EXAMPLES = {
    "E-commerce store": "We want an online store for our handloom brand with checkout via Razorpay, "
                        "user accounts, an admin panel to manage products, WhatsApp order alerts and "
                        "reports. Around 15 pages. Need it in 2 months.",
    "Mobile app": "Simple food delivery app for Android and iOS with login, live location tracking, "
                  "push notifications, payments and an admin dashboard. Launch in 5 weeks.",
    "SEO": "Our law firm website gets little organic traffic. We need SEO, keyword research and a blog.",
}
choice = st.selectbox("Load an example", ["(write your own)"] + list(EXAMPLES))
brief = st.text_area("Client brief", EXAMPLES.get(choice, ""), height=160)
use_llm = st.toggle("Let Claude read the brief and polish the proposal (needs ANTHROPIC_API_KEY)", value=False)

if st.button("Analyze", type="primary") and brief.strip():
    r = analyze_brief(brief, use_llm=use_llm)
    e, q = r["estimate"], r["requirements"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Likely effort", f"{e['hours_likely']} h")
    c2.metric("Range", f"{e['hours_low']}-{e['hours_high']} h")
    c3.metric("Cost (USD)", f"${e['cost_low']:,.0f}-{e['cost_high']:,.0f}")
    c4.metric("Duration", f"~{e['weeks_likely']} wks")
    l, rcol = st.columns(2)
    with l:
        st.subheader("Extracted requirements")
        st.json(q)
        st.subheader("Risks")
        for x in r["risks"]: st.warning(x)
    with rcol:
        st.subheader("Clarifying questions")
        for x in r["questions"]: st.info(x)
    st.divider()
    st.markdown(r["proposal"])
