# Melodify AI — Streamlit Deployment

## Deploy to Streamlit Community Cloud

1. Push this folder to a **GitHub repo** (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

## Local Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- The SQLite database (`song_player.db`) is created automatically on first run.
- On Streamlit Cloud the DB resets on each redeploy — this is expected for a free tier deployment.
- Gemini API key is entered in-app (no secrets file needed).
