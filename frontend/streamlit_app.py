# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.data_fetch import get_history
from backend.indicators import compute_indicators, compute_score