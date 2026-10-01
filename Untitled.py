import base64
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = {
	"Watch_Date",
	"Region",
	"Monthly_Revenue",
	"Subscription_Plan",
	"Rating",
	"Category",
}
MONTH_ORDER = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
]

st.set_page_config(
	page_title="Netflix viewing insights | Analytics",
	page_icon="N",
	layout="wide",
	initial_sidebar_state="collapsed",
)

LOGO_IMAGE_PATH = Path(__file__).with_name("logoimages.jfif")
BACKGROUND_IMAGE_DATA = base64.b64encode(
	Path(__file__).with_name("bgimages.jfif").read_bytes()
).decode("ascii")

st.markdown(
	"""
	<style>
		@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
		:root {
			--ink: #171717;
			--muted: #666666;
			--paper: #ffffff;
			--line: #e2e2e2;
			--red: #e50914;
		}
		html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
		.stApp { background-color: var(--paper); color: var(--ink); }
		[data-testid="stSidebar"] { background: rgba(255, 255, 255, .97); border-right: 1px solid var(--line); }
		[data-testid="stHeader"] { background: transparent; }
		.block-container { max-width: 1440px; padding-top: 2.2rem; padding-bottom: 3rem; }
		h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: 0; }
		h1, h2, h3, label, p { color: var(--ink); }
		h1 { font-size: 2.15rem !important; font-weight: 800 !important; }
		h2 { font-size: 1.15rem !important; font-weight: 700 !important; }
		.eyebrow { color: var(--red); font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
		.subtitle { color: var(--muted); font-size: .95rem; margin-top: -.5rem; }
		.metric-label { color: var(--muted); font-size: .76rem; font-weight: 600; text-transform: uppercase; }
		[data-testid="stMetric"] { background: rgba(255, 255, 255, .97); padding: 1rem 1.1rem; border: 1px solid var(--line); border-top: 2px solid var(--red); border-radius: 6px; }
		[data-testid="stMetricValue"] { font-family: 'Manrope', sans-serif; font-weight: 800; }
		[data-testid="stVerticalBlockBorderWrapper"] { background: rgba(255, 255, 255, .97); border-color: var(--line); border-radius: 6px; }
		div[data-testid="stFileUploader"] { padding-top: .4rem; }
		.stCaption { color: var(--muted); }
		hr { border-color: var(--line); }
		.stButton > button { border-color: var(--red); color: var(--ink); }
		.stButton > button:hover { border-color: #b20710; color: var(--red); }
		[data-testid="stMultiSelectTagsContainer"] span { background-color: var(--red) !important; color: #ffffff !important; }
		[data-testid="stMultiSelectTagsContainer"] button { color: #ffffff !important; }
		[data-testid="stSidebar"] [data-baseweb="select"]:focus-within > div,
		[data-testid="stSidebar"] [data-testid="stDateInput"]:focus-within,
		[data-testid="stSidebar"] input:focus { border-color: var(--red) !important; box-shadow: 0 0 0 1px var(--red) !important; }
		[data-testid="stSidebar"] [role="option"][aria-selected="true"] { background-color: #fde7e8; color: var(--red); }
	</style>
	""",
	unsafe_allow_html=True,
)

st.markdown(
	f"""
	<style>
		.stApp {{
			background-image: linear-gradient(rgba(255, 255, 255, .92), rgba(255, 255, 255, .97)),
				url("data:image/jpeg;base64,{BACKGROUND_IMAGE_DATA}");
			background-size: cover;
			background-position: center;
			background-attachment: fixed;
		}}
	</style>
	""",
	unsafe_allow_html=True,
)


def load_data(uploaded_file) -> pd.DataFrame | None:
	local_file = Path(__file__).with_name("netflix.csv")
	if not local_file.exists():
		local_file = Path(__file__).with_name("netflix.csv.csv")
	if not local_file.exists():
		local_file = Path(__file__).with_name("netflix_public.csv")

	if uploaded_file is not None:
		try:
			return pd.read_csv(uploaded_file)
		except (UnicodeDecodeError, pd.errors.ParserError) as error:
			st.error(f"Could not read this CSV: {error}")
			return None

	if local_file.exists():
		try:
			return pd.read_csv(local_file)
		except (UnicodeDecodeError, pd.errors.ParserError) as error:
			st.error(f"Could not read netflix.csv: {error}")
			return None

	return None


def format_revenue(value: float) -> str:
	return f"${value:,.0f}"


def style_axis(axis: plt.Axes) -> None:
	axis.spines[["top", "right"]].set_visible(False)
	axis.spines["bottom"].set_color("#d8d8d8")
	axis.spines["left"].set_color("#d8d8d8")
	axis.tick_params(axis="both", colors="#5f5f5f", labelsize=9, length=0)
	axis.grid(axis="y", color="#ededed", linewidth=0.8)
	axis.set_axisbelow(True)


def show_bar_chart(data: pd.Series, title: str, value_label: str) -> None:
	fig, axis = plt.subplots(figsize=(7, 3.4))
	fig.patch.set_facecolor("white")
	axis.set_facecolor("white")
	chart_data = data.sort_values(ascending=True)
	bars = axis.bar(chart_data.index.astype(str), chart_data.values, color="#e50914", width=0.58)
	style_axis(axis)
	axis.tick_params(axis="x", labelrotation=25)
	for label in axis.get_xticklabels():
		label.set_horizontalalignment("right")
	axis.set_title(title, loc="left", fontsize=12, fontweight="bold", color="#171717", pad=15)
	axis.set_ylabel(value_label, color="#5f5f5f", fontsize=9, labelpad=10)
	axis.margins(y=0.18)
	axis.bar_label(
		bars,
		labels=[f"{value:,.0f}" for value in chart_data.values],
		padding=5,
		fontsize=8,
		color="#343434",
	)
	fig.tight_layout()
	st.pyplot(fig, width="stretch")
	plt.close(fig)


def show_dashboard(data: pd.DataFrame) -> None:
	missing_columns = REQUIRED_COLUMNS - set(data.columns)
	if missing_columns:
		st.error("This file is missing required columns: " + ", ".join(sorted(missing_columns)))
		st.caption("Expected columns: " + ", ".join(sorted(REQUIRED_COLUMNS)))
		return

	data = data.copy()
	data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
	data["Monthly_Revenue"] = pd.to_numeric(data["Monthly_Revenue"], errors="coerce")
	data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")
	for column in ("Viewing_Records", "Rating_Total"):
		if column in data.columns:
			data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)
	data = data.dropna(subset=["Watch_Date"])

	st.sidebar.divider()
	st.sidebar.markdown("#### Refine the view")
	if data.empty:
		st.warning("No rows have a valid Watch_Date. Check the date format in your CSV.")
		return

	start_date = data["Watch_Date"].min().date()
	end_date = data["Watch_Date"].max().date()
	selected_dates = st.sidebar.date_input(
		"Watch date range",
		value=(start_date, end_date),
		min_value=start_date,
		max_value=end_date,
	)

	filters = ["Region", "Subscription_Plan", "Category"]
	selected_values = {}
	for column in filters:
		options = sorted(data[column].dropna().astype(str).unique())
		selected_values[column] = st.sidebar.multiselect(
			column.replace("_", " "), options, default=options
		)

	filtered = data
	if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
		filtered = filtered[
			filtered["Watch_Date"].dt.date.between(selected_dates[0], selected_dates[1])
		]
	for column, values in selected_values.items():
		filtered = filtered[filtered[column].astype(str).isin(values)]

	if filtered.empty:
		st.info("No records match these filters. Adjust the date range or selections in the sidebar.")
		return

	total_revenue = filtered["Monthly_Revenue"].sum()
	if {"Viewing_Records", "Rating_Total"}.issubset(filtered.columns):
		viewing_records = filtered["Viewing_Records"].sum()
		average_rating = filtered["Rating_Total"].sum() / viewing_records if viewing_records else float("nan")
		rating_by_plan = filtered.groupby("Subscription_Plan")["Rating_Total"].sum()
	else:
		viewing_records = len(filtered)
		average_rating = filtered["Rating"].mean()
		rating_by_plan = filtered.groupby("Subscription_Plan")["Rating"].sum()
	region_count = filtered["Region"].nunique()
	duplicate_count = int(filtered.duplicated().sum())

	metrics = st.columns(4)
	metrics[0].metric("Total revenue", format_revenue(total_revenue))
	metrics[1].metric("Average rating", f"{average_rating:.1f}" if pd.notna(average_rating) else "N/A")
	metrics[2].metric("Viewing records", f"{viewing_records:,.0f}")
	metrics[3].metric("Regions", f"{region_count:,}")

	st.markdown(" ")
	rating_by_plan = rating_by_plan[rating_by_plan > 0]
	with st.container(border=True):
		if rating_by_plan.empty:
			st.info("No positive ratings to display for these filters.")
		else:
			fig, axis = plt.subplots(figsize=(10, 4.5))
			fig.patch.set_facecolor("white")
			axis.set_facecolor("white")
			axis.pie(
				rating_by_plan.values,
				labels=rating_by_plan.index.astype(str),
				autopct="%1.0f%%",
				startangle=90,
				colors=["#e50914", "#b20710", "#f05a61", "#7a0710", "#ff9a9e"],
				wedgeprops={"edgecolor": "white", "linewidth": 2},
				textprops={"color": "#343434", "fontsize": 9},
			)
			axis.set_title(
				"Rating share by subscription plan",
				loc="left",
				fontsize=12,
				fontweight="bold",
				color="#171717",
				pad=12,
			)
			fig.tight_layout()
			st.pyplot(fig, width="stretch")
			plt.close(fig)

	with st.container(border=True):
		show_bar_chart(
			filtered.groupby("Category")["Monthly_Revenue"].sum(),
			"Revenue by category",
			"Revenue",
		)

	left, right = st.columns(2, gap="large")
	with left, st.container(border=True):
		show_bar_chart(
			filtered.groupby("Region")["Monthly_Revenue"].sum(),
			"Revenue by region",
			"Revenue",
		)
	with right, st.container(border=True):
		monthly_revenue = filtered.assign(
			Month=filtered["Watch_Date"].dt.month_name()
		).groupby("Month")["Monthly_Revenue"].sum().reindex(MONTH_ORDER, fill_value=0)
		months_in_data = filtered["Watch_Date"].dt.month_name().unique()
		show_bar_chart(
			monthly_revenue[monthly_revenue.index.isin(months_in_data)],
			"Revenue by month",
			"Revenue",
		)

	st.markdown(" ")
	with st.container(border=True):
		if "Viewing_Records" in filtered.columns:
			daily_views = filtered.set_index("Watch_Date")["Viewing_Records"].resample("MS").sum()
		else:
			daily_views = filtered.set_index("Watch_Date").resample("MS").size()
		daily_views.index = daily_views.index.strftime("%b %Y")
		st.subheader("Viewing activity over time")
		st.bar_chart(daily_views.rename("Viewing records"), color="#e50914", height=260)

	st.markdown(" ")
	with st.expander("Dataset details"):
		detail_left, detail_right = st.columns(2)
		detail_left.write(f"**Rows shown:** {len(filtered):,} of {len(data):,}")
		detail_left.write(f"**Exact duplicate rows:** {duplicate_count:,}")
		detail_right.write(f"**Missing values:** {int(filtered.isna().sum().sum()):,}")
		detail_right.write(f"**Date coverage:** {filtered['Watch_Date'].min():%b %d, %Y} to {filtered['Watch_Date'].max():%b %d, %Y}")
		st.dataframe(filtered, width="stretch", hide_index=True)


st.sidebar.markdown("### NETFLIX / INSIGHTS")
st.sidebar.caption("Viewing and revenue analytics")
logo_column, title_column = st.columns([1, 8], vertical_alignment="center")
with logo_column:
	st.image(str(LOGO_IMAGE_PATH), width=100)
with title_column:
	st.markdown('<div class="eyebrow">Audience intelligence / 01</div>', unsafe_allow_html=True)
	st.title("Netflix viewing insights")
	st.markdown('<p class="subtitle">Revenue, audience ratings and viewing patterns across your catalog.</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload viewing data", type=["csv"])
netflix = load_data(uploaded_file)

if netflix is None:
	st.info("Upload your Netflix CSV above to explore the dashboard.")
	st.caption("The file should include Watch_Date, Region, Monthly_Revenue, Subscription_Plan, Rating and Category.")
else:
	show_dashboard(netflix)




