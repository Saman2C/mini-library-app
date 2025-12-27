# Bonus UI (Streamlit)

This UI is an optional bonus for the Mini Library App.

## Tech
- Streamlit
- Uses the same JSON storage: `data/books.json`

## Run UI
From the project root:

```bash
pip install -r requirements.txt
streamlit run ui/app_streamlit.py


git add requirements.txt ui/app_streamlit.py ui/README_UI.md README.md
git commit -m "feat(ui): add streamlit bonus UI"
git push -u origin ui/streamlit