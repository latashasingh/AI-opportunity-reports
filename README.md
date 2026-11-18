# Cynbit Project Scoper

A small tool built for the Cynbit AI/ML intern assessment. You paste in a client brief, and it tells you what's being asked for, how many hours that probably means (as a range), what could go wrong, and what to ask the client before quoting.

The thinking behind it is in `docs/`:
- `docs/01_AI_Opportunity_Report.md` - why I picked this problem over six others
- `docs/02_Technical_Approach_Report.md` - how it works and what I'd do next

## Try it

```bash
pip install -r requirements.txt
python tests/test_core.py
streamlit run app.py
```

It runs offline. If you set `ANTHROPIC_API_KEY`, there's a toggle to let Claude do the extraction and tidy the proposal wording. The hour estimates never come from the LLM.

## Read this before trusting any number

The estimator is trained on made-up project history, because I don't have Cynbit's real data. The output shows how the system behaves, not what Cynbit would actually charge. To use it for real, point `train_model()` at a CSV of past projects (same columns as `to_row()` plus an `hours` column holding *actual* hours).

Company details came from public directory listings and should be checked against cynbit.in.
