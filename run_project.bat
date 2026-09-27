@echo off
python -m src.ingest
python -m src.index
streamlit run app.py
