# How the scoping assistant works

*AI/ML Engineer Intern assessment, Report 3 of 3 (the proof of concept lives in `scoper/` and `app.py`)*

## The idea in one paragraph

Paste in a client brief. The tool pulls out what's being asked for, predicts a *range* of hours (not a single number), flags risks, lists the questions Cynbit should ask before quoting, and drafts a proposal. My rule while building was: **the language model handles words, the statistical model handles numbers, and plain rules handle common sense.** I'll explain why I split it that way.

## Why not just ask an LLM for the estimate?

It's the obvious shortcut, and I tried to talk myself out of it. An LLM will happily say "about 400 hours" for anything. The answer will sound reasonable, differ on the next run, and can't be checked or improved with Cynbit's own history. A quote is a financial commitment, so I want a number that is repeatable and that gets better as real data arrives. So the LLM never touches the estimate.

## The pipeline

1. **Extraction.** Turn messy text into a structured record: which services (web, mobile, SEO...), which features (login, payments, admin panel...), roughly how many pages, how many platforms, any stated deadline.
2. **Estimation.** Feed that record into a trained model that outputs hours.
3. **Sanity layer.** Rules that notice things a human would: a short deadline, no budget mentioned, "simple" used next to five features.
4. **Proposal.** Fill a template with the results; optionally let an LLM polish the wording while the numbers stay locked.

## Decisions and the reasoning behind them

**Extraction: LLM first, keyword rules as fallback.** Real briefs are messy, sometimes mixing Hindi and English, and an LLM copes far better than regex. But I wanted the demo to run with no API key and no internet, and I wanted a safety net if the model returns junk. So the LLM must answer in JSON using a fixed list of allowed services and features; anything outside the list is dropped; and if anything fails the rule-based extractor takes over.

**Estimation: three gradient-boosting models, not one.** I trained separate models for the 20th, 50th and 80th percentile of hours. A single "predicted 669 hours" hides how unsure the model is. A range like "530 to 980, most likely 670" is more honest, and it's how a good estimator talks to a client anyway. I trained on the logarithm of hours because project effort behaves multiplicatively (two platforms costs roughly a third more, a rush job adds overhead) and because it stops the model predicting negative hours.

I picked gradient boosting over a neural network because the dataset will be small, tabular and full of interactions between features, which is exactly where tree models are strong and deep learning is wasteful. I picked it over simple linear regression because "payments" costs different amounts in an e-commerce site than in a mobile app.

**Data: synthetic, and I'm saying so loudly.** I don't have Cynbit's project history, so I generated 600 fake projects from a formula with realistic noise. That lets the prototype run, nothing more. The numbers it prints are illustrative and **should not be read as real Cynbit costs.** The point of the architecture is that you swap in a CSV of real past projects and the same code trains on it. The only column that matters most is `hours`: the *actual* hours a project took, not what was quoted. Training on quotes would just teach the model to repeat old mistakes.

## What testing taught me

I ran a few sample briefs through it and found problems I hadn't predicted.

- An SEO brief ("we need SEO, keyword research and a blog") was being tagged as needing a *site search feature*, because my keyword list contained the word "search" and the phrase "search engine" matched it. I fixed it by using more specific phrases ("site search", "search bar"). A small bug, but it shows why keyword rules need testing against real language, and why the LLM path matters.
- A "simple" food delivery app brief (Android and iOS, login, live tracking, notifications, payments, admin dashboard, 5 weeks) came out at roughly 530 to 980 hours with a likely 670, plus flags for the tight timeline and a "client says simple but the scope isn't" warning. That last one I added deliberately, because "simple" is the most expensive word in software sales.
- The risk and question logic ended up being the part I'd demo first. It's the least "AI" part of the system and arguably the most useful.

## How I'd judge whether it's any good

- **Extraction:** hand-label about 50 real briefs and check whether the right features are found. I'd want 85% or better on both precision and recall before trusting it.
- **Estimates:** mean absolute percentage error against actual hours, once there are at least 30 real projects. Also check *calibration*: about 60% of real outcomes should fall inside the low-to-high band. If only 40% do, the range is too narrow and the model is overconfident.
- **Usefulness:** ask the people who use it whether the clarifying questions were worth asking. If reviewers keep ignoring them, I've built the wrong thing.

## Plan

| Weeks | What happens |
|---|---|
| 1-2 | Collect 20-40 past projects with real final hours; run the tool blind against human estimates |
| 3-4 | Retrain on real data; adjust the feature list to match what Cynbit actually sells |
| 5-6 | Put it behind a login, connect to the enquiry form, log every use |
| After | Monthly retraining; add "similar past projects" search using text embeddings; extend to SEO briefs |

Stack: Python, pandas, scikit-learn, Streamlit for the interface, the Anthropic API as an optional extra.

## Limits, plainly

- The estimator learned from synthetic data, so it demonstrates a mechanism, not Cynbit's reality.
- The $18 hourly rate and the team-capacity assumption used for duration are placeholders.
- Keyword extraction misses nuance. The LLM mode is better but needs a key.
- This should assist a person, never replace the sign-off before a quote reaches a client.
- For privacy, I'd strip names, emails and phone numbers before any brief goes to an external model, and keep the offline mode for sensitive projects.
