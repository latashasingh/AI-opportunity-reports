# Where AI can actually help Cynbit

*AI/ML Engineer Intern assessment, Report 1 of 3*

## Starting point

Cynbit Technologies is a Jaipur agency founded in 2024. Public listings put it at 20-plus people, selling web and app development, UX/UI, SEO and custom software to small and mid-size clients. I couldn't find much beyond directory entries, so I treated it as what it looks like: a young services firm whose only real assets are its people's time and its reputation for not blowing deadlines.

That framing shaped everything below. When I started brainstorming I had the usual list ("add a chatbot!", "AI for SEO!"), but the sharper question was different: **where does a 20-person agency lose money or time without noticing?**

Talking it through with how agencies generally work, three leaks keep coming up:

1. **Quoting.** A client sends a vague email ("we need an app like Zomato, but simple"). Someone senior spends hours on calls and spreadsheets turning that into a number. If the number is low, the agency eats the overrun on fixed-price work. If it's high, they lose the deal.
2. **Repeated work.** Auth, admin panels, SEO audits and content briefs get rebuilt from scratch for every client.
3. **Growth tied to headcount.** More revenue means more hires, because nothing multiplies a developer's output.

## What I considered

I wrote down seven ideas and tried to be harsh about each one.

- **AI scoping and estimation assistant** (brief in, requirements, hours range and proposal out). Hits leak #1 directly.
- **SEO toolkit** (keyword clustering, content briefs, on-page audits). Real, and SEO is already a Cynbit service. But SEO tooling is a crowded market (Ahrefs, Semrush, Surfer). Cynbit would be competing with products that have years of head start.
- **Website chatbot for lead capture.** Easy to build, honestly the thing most agencies would do first. The catch is that it improves a trickle of website traffic, not the core business. Nice, not important.
- **AI add-ons to sell to clients** (support bots, recommendations). Probably the biggest long-term upside, but each one needs client data, and Cynbit has no reference projects yet to sell from.
- **Developer copilots** (code review, test generation). Valuable, but GitHub Copilot and similar tools already exist. Building our own is reinventing a commodity.
- **Project delay prediction.** Needs a year or more of clean tracker data. Cynbit is two years old at most.
- **Churn / upsell prediction.** Same data problem, plus too few clients for any model to learn from.

The last two were easy to rule out. The data simply doesn't exist yet, and a model trained on forty rows is mostly decoration.

## The pick: a scoping assistant

I chose the quoting problem for four reasons.

**It works without data.** Most ML ideas die at "we don't have the data." Here an LLM plus a few rules is useful on day one, and the system *creates* its own training data as a side effect. Every quote Cynbit sends, and every project it later closes, becomes a labelled example of predicted versus actual hours. After a year that is a dataset competitors can't copy.

**It's low risk.** Nothing goes to a client automatically. A human reads the output, which matters because the failure I worry about most is a confident wrong number.

**It gets better questions, not only faster answers.** While building the prototype I noticed the most useful output wasn't the estimate, it was the *clarifying questions*. "Which payment gateway?" "New build or rebuild?" "Android, iOS or both?" Each of those is a scope gap that normally surfaces three weeks after the contract is signed. An assistant that asks them at quoting time saves more money than one that estimates slightly better.

**It reuses easily.** The structured view of a project (services, features, size) is the same input a chatbot or an upsell engine would need later.

## A back-of-envelope business case

I don't have Cynbit's numbers, so treat these as assumptions to replace:

- Around 30 inbound enquiries a month, about 3 senior hours each to quote. That is 90 hours a month.
- With the assistant doing the first draft, review might take an hour each. That frees roughly 60 senior hours a month.
- If fixed-price work currently overruns by about 20% and calibrated ranges bring that to 10-12%, the margin impact on a handful of mid-size projects will likely be bigger than the time savings.

The second point is the one I'd bet on, but it's also the least provable until there's real data. I'd rather say that than pretend otherwise.

## Where this could go wrong

- **Wrong numbers that look authoritative.** This is why the tool shows a range (optimistic to pessimistic) rather than one figure, and why a person signs off.
- **The LLM inventing scope.** Extraction is forced into a fixed list of services and features, and anything outside the list is thrown away.
- **Client confidentiality.** Briefs can contain sensitive business details, so the tool has a fully offline mode and an LLM mode that should only ever see redacted text.
- **Garbage time logs.** If developers don't record hours honestly, the model learns fiction. The plan below starts with cleaning that up.

## Roadmap I'd follow

1. **First two weeks:** take 20 old briefs where the final hours are known, run them through the tool blind, and compare. This tells us whether the idea is worth continuing.
2. **Weeks 3-6:** put it behind a simple login, connect it to the enquiry form, and log every run.
3. **Months 2-4:** retrain on real history, add "similar past projects" retrieval so the answer comes with evidence.
4. **After that:** extend the same pattern to SEO briefs, and consider the website chatbot as a cheap add-on.

## How I'd know it worked

Time to first proposal. How often final hours land within 15% of the quote. Win rate on proposals. Margin on fixed-price jobs. Senior hours saved. If after three months estimation error isn't dropping, I'd say so and rethink.
