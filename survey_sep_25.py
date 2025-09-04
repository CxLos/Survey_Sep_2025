# =================================== IMPORTS ================================= #

import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import dash
from dash import dcc, html, dash_table

# Google Web Credentials
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 'data/~$bmhc_data_2024_cleaned.xlsx'
# print('System Version:', sys.version)

# ------ Pandas Display Options ------ #
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns (if needed)
pd.set_option('display.width', 1000)  # Adjust the width to prevent line wrapping

pd.reset_option('display.max_columns')
# -------------------------------------- DATA ------------------------------------------- #

current_dir = os.getcwd()
current_file = os.path.basename(__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))
# data_path = 'data/Submit_Review_Responses.xlsx'
# file_path = os.path.join(script_dir, data_path)
# data = pd.read_excel(file_path)
# df = data.copy()

# Define the Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1pxi6x6ikRZEjzEwM1Aw28yWK1h-G1p61wulYS5F9kOw/edit?resourcekey=&gid=586078421#gid=586078421"
sheet_url_2 = "https://docs.google.com/spreadsheets/d/1Vi5VQWt9AD8nKbO78FpQdm6TrfRmg0o7az77Hku2i7Y/edit#gid=78776635"
sheet_url_3 = "https://docs.google.com/spreadsheets/d/1GWnQrLptjkgg8CR1G8OpYaCHZMmW5xOzg0kFtPCkxKw/edit?gid=1975848686#gid=1975848686"

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials
encoded_key = os.getenv("GOOGLE_CREDENTIALS")

if encoded_key:
    json_key = json.loads(base64.b64decode(encoded_key).decode("utf-8"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
else:
    creds_path = r"C:\Users\CxLos\OneDrive\Documents\BMHC\Data\bmhc-timesheet-4808d1347240.json"
    if os.path.exists(creds_path):
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    else:
        raise FileNotFoundError("Service account JSON file not found and GOOGLE_CREDENTIALS is not set.")
    
expected_headers = [
    'Timestamp',
    'Email Address', 
    'Name:', 
    "Prior to today's visit, when was the last time you visited a doctor?", 
    'Which services were provided to you today?', 
    'How do you feel about the health issue that brought you to BMHC?', 
    'What is your overall stress level?', 
    'How would you rate your overall level of mental health?', 
    'How would you rate your overall physical health?',
    "What is your overall impression of the Black Men's Health Clinic?", 
    'Did the medical provider meet your expectations?', 
    'Did the medical care meet your needs?', 
    'Did the Outreach & Engagement Team provide a strong support system?', 
    'Are you a member of the HealthyCuts™ Program?',
]

# Authorize and load the sheet
client = gspread.authorize(creds)
sheet = client.open_by_url(sheet_url)
worksheet = sheet.get_worksheet(0)  
# values = worksheet.get_all_values()
# headers = values[0] 
# rows = values[1:] # Remaining rows as data

# data = pd.DataFrame(rows, columns=headers)
# data = pd.DataFrame(worksheet.get_all_records())
# data = pd.DataFrame(client.open_by_url(sheet_url).get_all_records())
data = pd.DataFrame(worksheet.get_all_records(expected_headers=expected_headers))
df = data.copy()

# -----------------------------

# Get the reporting month:
mo = "Sep"
int_month = 9
report_month = datetime(2025, 9, 1).strftime("%B")
report_year = datetime(2025, 9, 1).strftime("%Y")

# Strip whitespace from string entries in the whole DataFrame
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

# Filtered df where 'Date of Activity:' is between Ocotber to December:
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['Month'] = df['Timestamp'].dt.month_name()
df = df[(df['Timestamp'].dt.month == int_month) & (df['Timestamp'].dt.year == int(report_year))]

# ------ Navigation ------ #

data_2 = pd.DataFrame(client.open_by_url(sheet_url_2).sheet1.get_all_records())
df_2 = data_2.copy()

for col in df_2.select_dtypes(include='object').columns:
    df_2[col] = df_2[col].map(lambda x: x.strip() if isinstance(x, str) else x)

df_2['Date of Activity'] = pd.to_datetime(df_2['Date of Activity'], errors='coerce')
df_2['Month'] = df_2['Date of Activity'].dt.month_name()
df_2 = df_2[(df_2['Date of Activity'].dt.month == int_month) & (df_2['Date of Activity'].dt.year == int(report_year))]

# ------ Findhelp ------ #

client_3 = gspread.authorize(creds)
sheet_3 = client_3.open_by_url(sheet_url_3)
worksheet_3 = sheet_3.worksheet(f"{report_month}")
data_3 = pd.DataFrame(worksheet_3.get_all_records())
df_3 = data_3.copy()

for col in df_3.select_dtypes(include='object').columns:
    df_3[col] = df_3[col].map(lambda x: x.strip() if isinstance(x, str) else x)

# --------------------------------------

# print(df.head(10))
# print(df_2.head(10))
# print(df_3.head(10))
# print('Total Marketing Events: ', len(df))
# print('Column Names: \n', df.columns)
# print('DF Shape:', df.shape)
# print('Dtypes: \n', df.dtypes)
# print('Info:', df.info())
# print("Amount of duplicate rows:", df.duplicated().sum())

# print('Current Directory:', current_dir)
# print('Script Directory:', script_dir)
# print('Path to data:',file_path)

# ================================= Columns ================================= #

columns =[
    'Timestamp',
    'Email Address', 
    'Name:', 
    "Prior to today's visit, when was the last time you visited a doctor?", 
    'Which services were provided to you today?', 
    'How do you feel about the health issue that brought you to BMHC?', 
    'What is your overall stress level?', 
    'Explain the reason for your answer:', 
    'How would you rate your overall level of mental health?', 
    'How would you rate your overall physical health?',
    'Please explain the reason for your answer:', 
    "What is your overall impression of the Black Men's Health Clinic?", 
    'Did the medical provider meet your expectations?', 
    'Did the medical care meet your needs?', 
    'Did the Outreach & Engagement Team provide a strong support system?', 
    'Please explain the reason for your answer:',
    'Are you a member of the HealthyCuts™ Program?',
    'Are you a Movement is Medicine member?', 
    'Are you interested in potential clinical trial opportunities?', 
    'Month'
]

# =============================== Missing Values ============================ #

# missing = df.isnull().sum()
# print('Columns with missing values before fillna: \n', missing[missing > 0])

# ============================== Data Preprocessing ========================== #

# Check for duplicate columns
# duplicate_columns = df.columns[df.columns.duplicated()].tolist()
# print(f"Duplicate columns found: {duplicate_columns}")
# if duplicate_columns:
#     print(f"Duplicate columns found: {duplicate_columns}")

df.rename(
    columns={
        'Email Address': 'Email',
        "Prior to today's visit, when was the last time you visited a doctor?": 'Last Doctor Visit',
        # ------------------------------------------------
        'Which services were provided to you today?': 'Service',
        'How do you feel about the health issue that brought you to BMHC?': 'Health',
        'What is your overall stress level?': 'Stress',
        'How would you rate your overall level of mental health?': 'Mental',
        'How would you rate your overall physical health?': 'Physical',
        'Did the medical provider meet your expectations?': 'Expectation',
        'Did the medical care meet your needs?': 'Care',
        'Did the Outreach & Engagement Team provide a strong support system?': 'Outreach',
        'Are you a member of the HealthyCuts™ Program?': 'Healthy Cuts',
        'Are you a Movement is Medicine member?': 'MIM',
        'Are you interested in potential clinical trial opportunities?': 'Trials',
        # ------------------------------------------------
        "What is your overall impression of the Black Men's Health Clinic?": 'Impression',
    },
    inplace=True
)

# Define a standardized color palette for ratings 1 to 5
rating_colors = {
    '1': 'rgb(255, 2, 2)',      # Bright Red
    '2': 'rgb(231, 123, 0)',    # Orange
    '3': 'rgb(255, 207, 62)',   # Yellow-Gold
    '4': 'rgb(9, 132, 0)',      # Green
    '5': 'rgb(42, 147, 252)'    # Blue
}

rating_order = ['1', '2', '3', '4', '5']

columns_to_order = ['Health', 'Mental', 'Stress', 'Physical', 
                    # 'Impression', 'Expectation', 'Care'
                    ]

for col in columns_to_order:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .replace(to_replace=["", "nan"], value="N/A") 
    )
    df[col] = pd.Categorical(df[col], categories=rating_order, ordered=True)

# Calculate start and end month indices for the quarter
# all_months = [
#     'January', 'February', 'March', 
#     'April', 'May', 'June',
#     'July', 'August', 'September', 
#     'October', 'November', 'December'
# ]
# start_month_idx = (quarter - 1) * 3
# month_order = all_months[start_month_idx:start_month_idx + 3]

# =========================== Total Reviews ============================ #

total_reviews = len(df)
# print(f'Total Client Reviews {current_month}: ', total_reviews)

# --- Missing Reviews --- #
len_nav = len(df_2)
# print(f'Navigation Visits {current_month}: ', len_nav)
len_fh = len(df_3)
# print(f'Findhelp Visits {current_month}: ', len_fh)
total_nav = len_nav + len_fh
# print(f'Combined Visits {current_month}: ', total_nav)

missing_reviews = total_nav - total_reviews
# print(f'Clients didn\'t submit reviews {current_month}: ', missing_reviews)

# --- Capture Rate --- # 
capture_rate = (total_reviews / total_nav) * 100 
capture_rate = round(capture_rate)
# print(f'Capture Rate {current_month}: {capture_rate}%')

# ------------------------ Health Issue ---------------------------- #

# print("Unique Health Before: \n", df['Health'].unique().tolist())
# print("Health Value Counts: \n", df['Health'].value_counts())

# df['Health'] = (df['Health']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "" : ""
#     })          
# )

# print("Health Unique After: \n", df['Health'].unique().tolist())

df_health_counts = df['Health'].value_counts().reset_index(name='Count')

health_fig = px.bar(
    df_health_counts, 
    x='Health', 
    y='Count',
    color='Health', 
    text='Count',  
    category_orders={'Health': rating_order}, 
    color_discrete_map=rating_colors, 
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'How Clients Feel About The Health Issue That Brought Them to BMHC',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            # text=None,
            text="Rating",
            font=dict(size=20), 
        ),
        tickmode='array',
        # tickvals=sorted(df_health_counts['Month'].unique()),
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            # text=None,
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    # margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

health_pie = px.pie(
    df_health_counts,
    names='Health',
    values='Count',
    color='Health',
    # category_orders={'Health': rating_order}, 
    color_discrete_map=rating_colors, 
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of How Clients Feel About The Health Issue That Brought Them to BMHC', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Rating',
        # title=None,
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0   
    )  
).update_traces(
    rotation=-40,  #
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Stress Level ---------------------------- #

# df['Stress'] = (
#     df['Stress']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "" : "",
#     })
# )

# Count values
df_stress_counts = df['Stress'].value_counts().reset_index(name='Count')

# Bar chart
stress_fig = px.bar(
    df_stress_counts,
    x='Stress',
    y='Count',
    color='Stress',
    text='Count',
    category_orders={'Stress': rating_order},
    color_discrete_map=rating_colors,
).update_layout(
    # height=600,
    # width=900,
    title=dict(
        text=f'How Clients Feel About Their Stress Levels',
        x=0.5,
        font=dict(size=22, family='Calibri', color='black')
    ),
    font=dict(family='Calibri', size=17, color='black'),
    xaxis=dict(
        title=dict(text="Rating", font=dict(size=20)),
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(text="Count", font=dict(size=20)),
    ),
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),
    textposition='auto',
    textangle=0,
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

# Pie chart
stress_pie = px.pie(
    df_stress_counts,
    names='Stress',
    values='Count',
    color='Stress',
    # category_orders={'Stress': rating_order},
    color_discrete_map=rating_colors,
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of How Clients Feel About Their Stress Levels',
        font=dict(size=22, family='Calibri', color='black'),
    ),
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=60, l=0)
).update_traces(
    rotation=-40,
    textfont=dict(size=14),
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Mental Health ---------------------------- #

# print("Unique Mental Before: \n", df['Mental'].unique().tolist())
# print("Mental Value Counts: \n", df['Mental'].value_counts())

# df['Mental'] = (
#     df['Mental']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "": ""
#     })          
# )

# print("Mental Unique After: \n", df['Mental'].unique().tolist())

df_mental_counts = df['Mental'].value_counts().reset_index(name='Count')
df_mental_counts.rename(columns={'index': 'Mental'}, inplace=True)

mental_fig = px.bar(
    df_mental_counts, 
    x='Mental', 
    y='Count',
    color='Mental', 
    text='Count',  
    category_orders={'Mental': rating_order},
    color_discrete_map=rating_colors, 
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'How Clients are Feeling About Their Mental Well-being',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Rating",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

mental_pie = px.pie(
    df_mental_counts,
    names='Mental',
    values='Count',
    color='Mental',
    color_discrete_map=rating_colors,
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of How Clients are Feeling About Their Mental Well-being', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0)  
).update_traces(
    rotation=-40,
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Physical Health ---------------------------- #

# print("Unique Physical Before: \n", df['Physical'].unique().tolist())
# print("Physical Value Counts: \n", df['Physical'].value_counts())

# df['Physical'] = (
#     df['Physical']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "": ""
#     })          
# )

# print("Physical Unique After: \n", df['Physical'].unique().tolist())

df_physical_counts = df['Physical'].value_counts().reset_index(name='Count')
# df_physical_counts.rename(columns={'index': 'Physical'}, inplace=True)

physical_fig = px.bar(
    df_physical_counts, 
    x='Physical', 
    y='Count',
    color='Physical', 
    text='Count',  
    category_orders={'Physical': rating_order},
    color_discrete_map=rating_colors, 
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'How Clients are Feeling About Their Physical Well-being',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Rating",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

physical_pie = px.pie(
    df_physical_counts,
    names='Physical',
    values='Count',
    color='Physical',
    color_discrete_map=rating_colors,
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of How Clients are Feeling About Their Physical Well-being', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0)  
).update_traces(
    rotation=-40,
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Provider Expectation ---------------------------- #

# print("Unique Expectation Before: \n", df['Expectation'].unique().tolist())
# print("Expectation Value Counts: \n", df['Expectation'].value_counts())

df['Expectation'] = (
    df['Expectation']
    .astype(str)
    .str.strip()
    .replace(to_replace=["",], value="N/A")          
)

# print("Expectation Unique After: \n", df['Expectation'].unique().tolist())

df_expectation_counts = df['Expectation'].value_counts().reset_index(name='Count')
# df_expectation_counts.rename(columns={'index': 'Expectation'}, inplace=True)

expectation_fig = px.bar(
    df_expectation_counts, 
    x='Expectation', 
    y='Count',
    color='Expectation', 
    text='Count',  
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'Did Medical Provider Meet Your Expectations?',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Answer",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Answer',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

expectation_pie = px.pie(
    df_expectation_counts,
    names='Expectation',
    values='Count',
    color='Expectation',
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of Provider Expectations Met?', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Answer',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0)  
).update_traces(
    rotation=-40,
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Care Needs ---------------------------- #

# print("Unique Care Before: \n", df['Care'].unique().tolist())
# print("Care Value Counts: \n", df['Care'].value_counts())

df['Care'] = (
    df['Care']
    .astype(str)
    .str.strip()
    .replace(to_replace=["",], value="N/A")
)

# print("Care Unique After: \n", df['Care'].unique().tolist())

df_care_counts = df['Care'].value_counts().reset_index(name='Count')
# df_care_counts.rename(columns={'index': 'Care'}, inplace=True)

care_fig = px.bar(
    df_care_counts,
    x='Care',
    y='Count',
    color='Care',
    text='Count',
).update_layout(
    # height=600,
    # width=900,
    title=dict(
        text=f'Did Medical Care Meet Your Needs?',
        x=0.5,
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Answer",
            font=dict(size=20),
        ),
        tickangle=0,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20),
        ),
    ),
    legend=dict(
        title='Answer',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),
    textposition='auto',
    textangle=0,
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

care_pie = px.pie(
    df_care_counts,
    names='Care',
    values='Count',
    color='Care',
    custom_data=['Care'],
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of Care Needs Met?',
        font=dict(
            size=22,
            family='Calibri',
            color='black'
        ),
    ),
    legend=dict(
        title='Answer',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=60, l=0)
).update_traces(
    rotation=-40,
    textfont=dict(size=14),
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Outreach Support ---------------------------- #

# print("Unique Outreach Before: \n", df['Outreach'].unique().tolist())
# print("Outreach Value Counts: \n", df['Outreach'].value_counts())

# df['Outreach'] = (
#     df['Outreach']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "": "N/A",
#         "nan": "N/A",
#         pd.NA: "N/A",
#     })
# )

df['Outreach'] = (
    df['Outreach']
    .astype(str)
    .str.strip()
    .replace(to_replace=["", "nan", "None", "<NA>"], value="N/A")
)

# print("Outreach Unique After: \n", df['Outreach'].unique().tolist())

df_outreach_counts = df['Outreach'].value_counts().reset_index(name='Count')

outreach_fig = px.bar(
    df_outreach_counts,
    x='Outreach',
    y='Count',
    color='Outreach',
    text='Count',
).update_layout(
    # height=600,
    # width=900,
    title=dict(
        text=f'Did Outreach Provide a Strong Support System?',
        x=0.5,
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Answer",
            font=dict(size=20),
        ),
        tickangle=0,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20),
        ),
    ),
    legend=dict(
        title='Answer',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),
    textposition='auto',
    textangle=0,
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

outreach_pie = px.pie(
    df_outreach_counts,
    names='Outreach',
    values='Count',
    color='Outreach',
    custom_data=['Outreach'],
    # height=600,
).update_layout(
    title=dict(
        x=0.5,
        text=f'Ratio of Outreach Support Received?',
        font=dict(
            size=22,
            family='Calibri',
            color='black'
        ),
    ),
    legend=dict(
        title='Answer',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=60, l=0)
).update_traces(
    rotation=-70,
    textfont=dict(size=14),
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Movement is Medicine ---------------------------- #

# Clean and normalize MIM column
df['MIM'] = (
    df['MIM']
    .astype(str)
    .str.strip()
    .replace(to_replace=["", "nan", "None", "<NA>"], value="N/A")
)

# Value counts for MIM
df_mim_counts = df['MIM'].value_counts().reset_index(name='Count')
df_mim_counts.rename(columns={'index': 'MIM'}, inplace=True)

# Bar chart for MIM
mim_fig = px.bar(
    df_mim_counts, 
    x='MIM', 
    y='Count',
    color='MIM', 
    text='Count',  
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'Are You a Movement is Medicine Member?',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Response",
            font=dict(size=20), 
        ),
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Response',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Response</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

# Pie chart for MIM
mim_pie = px.pie(
    df_mim_counts,
    names='MIM',
    values='Count',
    color='MIM',
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Are You a Movement is Medicine Member?', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Response',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0)  
).update_traces(
    rotation=-40,
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Clinical Trials ---------------------------- #

df['Trials'] = (
    df['Trials']
    .astype(str)
    .str.strip()
    .replace(to_replace=["", "nan", "None", "<NA>"], value="N/A")
)

df_trials_counts = df['Trials'].value_counts().reset_index(name='Count')
df_trials_counts.rename(columns={'index': 'Trials'}, inplace=True)

trials_fig = px.bar(
    df_trials_counts,
    x='Trials',
    y='Count',
    color='Trials',
    text='Count',
).update_layout(
    # height=600,
    # width=900,
    title=dict(
        text=f'Are You Interested in Clinical Trial Opportunities?',
        x=0.5,
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Response",
            font=dict(size=20),
        ),
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20),
        ),
    ),
    legend=dict(
        title='Response',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),
    textposition='auto',
    textangle=0,
    hovertemplate='<b>Response</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

trials_pie = px.pie(
    df_trials_counts,
    names='Trials',
    values='Count',
    color='Trials',
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio Interested in Clinical Trial Opportunities',
        font=dict(
            size=22,
            family='Calibri',
            color='black'
        ),
    ),
    legend=dict(
        title='Response',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=60, l=0)
).update_traces(
    rotation=-40,
    textfont=dict(size=14),
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Healthy Cuts ---------------------------- #

# print("Unique Healthy Cuts Before: \n", df['Healthy Cuts'].unique().tolist())
# print("Healthy Cuts Value Counts Before: \n", df['Healthy Cuts'].value_counts())

df['Healthy Cuts'] = (
    df['Healthy Cuts']
    .astype(str)
    .str.strip()
    .replace(to_replace=["",], value="N/A")        
)

# print("Healthy Cuts Unique After: \n", df['Healthy Cuts'].unique().tolist())
# print("Healthy Cuts Value Counts After: \n", df['Healthy Cuts'].value_counts())

df_healthy_cuts_counts = df['Healthy Cuts'].value_counts().reset_index(name='Count')
df_healthy_cuts_counts.rename(columns={'index': 'Healthy Cuts'}, inplace=True)

healthy_cuts_fig = px.bar(
    df_healthy_cuts_counts, 
    x='Healthy Cuts', 
    y='Count',
    color='Healthy Cuts', 
    text='Count',  
    category_orders={'Healthy Cuts': rating_order},
    color_discrete_map=rating_colors, 
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'Are You Interested in a Healthy Cuts Membership?',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Rating",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Response',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

healthy_cuts_pie = px.pie(
    df_healthy_cuts_counts,
    names='Healthy Cuts',
    values='Count',
    color='Healthy Cuts',
    color_discrete_map=rating_colors,
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Are You Interested in a Healthy Cuts Membership', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Response',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0)  
).update_traces(
    rotation=-40,
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# ------------------------ Impression of BMHC ---------------------------- #

# print("Unique Impression Before: \n", df['Impression'].unique().tolist())
# print("Impression Value Counts: \n", df['Impression'].value_counts())

df['Impression'] = (
    df['Impression']
    .astype(str)
    .str.strip()
    .replace(to_replace=["",], value="N/A")          
)

# print("Impression Unique After: \n", df['Impression'].unique().tolist())

df_impression_counts = df['Impression'].value_counts().reset_index(name='Count')
# df_impression_counts.rename(columns={'index': 'Impression'}, inplace=True)

impression_fig = px.bar(
    df_impression_counts, 
    x='Impression', 
    y='Count',
    color='Impression', 
    text='Count',  
    category_orders={'Impression': rating_order},
    color_discrete_map=rating_colors, 
).update_layout(
    # height=600, 
    # width=900,
    title=dict(
        text=f'Overall Impression of BMHC?',
        x=0.5, 
        font=dict(
            size=22,
            family='Calibri',
            color='black',
        )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text="Rating",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickangle=0,
        showticklabels=True,
    ),
    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(size=20), 
        ),
    ),
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top"
    ),
    margin=dict(t=60, r=0, b=70, l=0),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=18),  
    textposition='auto', 
    textangle=0, 
    hovertemplate='<b>Rating</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'
)

impression_pie = px.pie(
    df_impression_counts,
    names='Impression',
    values='Count',
    color='Impression',
    color_discrete_map=rating_colors,
).update_layout(
    # height=600,
    title=dict(
        x=0.5,
        text=f'Ratio of Overall Impression of BMHC?', 
        font=dict(
            size=22,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Rating',
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top" 
    ),
    margin=dict(t=60, r=0, b=60, l=0)  
).update_traces(
    rotation=-40,
    textfont=dict(size=14),  
    texttemplate='%{value}<br> (%{percent:.1%})',
    hovertemplate='Rating %{label}: <b>%{value}</b><br>Percent: <b>%{percent:.1%}</b><extra></extra>',
)

# # ========================== Impression DataFrame Table ========================== #

df = df.sort_values('Timestamp', ascending=True)

# New DataFrame for Impression
df_impression = df[['Timestamp', 'Service',  'Impression']].copy()

# create a display index column and prepare table data/columns
# reset index to ensure contiguous numbering after any filtering/sorting upstream
df_indexed = df_impression.reset_index(drop=True).copy()
# Insert '#' as the first column (1-based row numbers)
df_indexed.insert(0, '#', df_indexed.index + 1)

# Convert to records for DataTable
data = df_indexed.to_dict('records')
columns = [{"name": col, "id": col} for col in df_indexed.columns]

# Engagement Table
impression_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df_impression.columns),
        fill_color='#34A853',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=16, color='white', family='Calibri') 
    ),
    cells=dict(
        values=[df[col] for col in df_impression.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

impression_table.update_layout(
    # margin=dict(t=20, r=0, b=0, l=800), 
    # height=1150,
    # width=1350,  
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        shapes=[
        dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="black", width=2),  # Black outside border
            fillcolor="rgba(0,0,0,0)"
        )
    ],
)
# ========================== DataFrame Table ========================== #

# Engagement Table
survey_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

survey_table.update_layout(
    margin=dict(l=50, r=50, t=30, b=60),  # Remove margins
    height=500,
    width=1400,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# ============================== Dash Application ========================== #

app = dash.Dash(__name__)
server= app.server 

app.layout = html.Div(
  children=[ 
            
    html.Div(
        className='divv', 
        children=[ 
            html.H1(
                'BMHC Client Satisfaction Report', 
                className='title'),
            html.H2( 
                f'{report_month} {report_year}', 
                className='title2'),
            html.Div(
                className='btn-box', 
                children=[
                    html.A(
                        'Repo',
                        href= f'https://github.com/CxLos/Survey_{mo}_{report_year}',
                        className='btn'
                    ),
                ]
            ),
        ]
    ),

# ============================ Rollups ========================== #

html.Div(
    className='rollup-row',
    children=[
        
        html.Div(
            className='rollup-box-tl',
            children=[
                html.Div(
                    className='title-box',
                    children=[
                        html.H3(
                            className='rollup-title',
                            children=[f'{report_month} Reviews']
                        ),
                    ]
                ),

                html.Div(
                    className='circle-box',
                    children=[
                        html.Div(
                            className='circle-1',
                            children=[
                                html.H1(
                                className='rollup-number',
                                children=[total_reviews]
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
        html.Div(
            className='rollup-box-tr',
            children=[
                html.Div(
                    className='title-box',
                    children=[
                        html.H3(
                            className='rollup-title',
                            children=[f'{report_month} Reviews Not Captured']
                        ),
                    ]
                ),
                html.Div(
                    className='circle-box',
                    children=[
                        html.Div(
                            className='circle-2',
                            children=[
                                html.H1(
                                className='rollup-number',
                                children=[missing_reviews]
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
    ]
),

html.Div(
    className='rollup-row',
    children=[
        html.Div(
            className='rollup-box-bl',
            children=[
                html.Div(
                    className='title-box',
                    children=[
                        html.H3(
                            className='rollup-title',
                            children=[f'{report_month} Capture Rate']
                        ),
                    ]
                ),

                html.Div(
                    className='circle-box',
                    children=[
                        html.Div(
                            className='circle-3',
                            children=[
                                html.H1(
                                className='rollup-number-2',
                                children=[f'{capture_rate}%']
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
        html.Div(
            className='rollup-box-br',
            children=[
                html.Div(
                    className='title-box',
                    children=[
                        html.H3(
                            className='rollup-title',
                            children=[f'Placeholder']
                        ),
                    ]
                ),
                html.Div(
                    className='circle-box',
                    children=[
                        html.Div(
                            className='circle-4',
                            children=[
                                html.H1(
                                className='rollup-number',
                                children=['-']
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
    ]
),

# ============================= Rating Row ========================== #

html.Div(
    className='rating_row',
    children=[
        
        html.Div(
            className='rating_box',
            children=[
                html.Div(
                    className='rating_outline1',
                    children=[
                        html.Div(
                            className='rating1',
                            children=[
                                html.H1(
                                    className='ratingg',
                                    children=['1']
                                )
                            ]  
                        ),
                    ],
                ),
                html.Div(
                    className='rating_title',
                    children=[
                        html.H1(
                            className='rating_title_text',
                            children=['Poor']
                        )
                    ],
                ),
            ],    
        ),
        html.Div(
            className='rating_box',
            children=[
                html.Div(
                    className='rating_outline2',
                    children=[
                        html.Div(
                            className='rating2',
                            children=[
                                html.H1(
                                    className='ratingg',
                                    children=['2']
                                )
                            ]  
                        ),
                    ],
                ),
                html.Div(
                    className='rating_title',
                    children=[
                        html.H1(
                            className='rating_title_text',
                            children=['Bad']
                        )
                    ],
                ),
            ],    
        ),
        html.Div(
            className='rating_box',
            children=[
                html.Div(
                    className='rating_outline3',
                    children=[
                        html.Div(
                            className='rating3',
                            children=[
                                html.H1(
                                    className='ratingg',
                                    children=['3']
                                )
                            ]  
                        ),
                    ],
                ),
                html.Div(
                    className='rating_title',
                    children=[
                        html.H1(
                            className='rating_title_text',
                            children=['OK']
                        )
                    ],
                ),
            ],    
        ),
        html.Div(
            className='rating_box',
            children=[
                html.Div(
                    className='rating_outline4',
                    children=[
                        html.Div(
                            className='rating4',
                            children=[
                                html.H1(
                                    className='ratingg',
                                    children=['4']
                                )
                            ]  
                        ),
                    ],
                ),
                html.Div(
                    className='rating_title',
                    children=[
                        html.H1(
                            className='rating_title_text',
                            children=['Good']
                        )
                    ],
                ),
            ],    
        ),
        html.Div(
            className='rating_box',
            children=[
                html.Div(
                    className='rating_outline5',
                    children=[
                        html.Div(
                            className='rating5',
                            children=[
                                html.H1(
                                    className='ratingg',
                                    children=['5']
                                )
                            ]  
                        ),
                    ],
                ),
                html.Div(
                    className='rating_title',
                    children=[
                        html.H1(
                            className='rating_title_text',
                            children=['Excellent']
                        )
                    ],
                ),
            ],    
        ),
    ]
),

# ============================= Graphs ========================== #

html.Div(
    className='graph-container',
    children=[
        
        html.H1(
            className='visuals-text',
            children='Visuals'
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=health_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=health_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=stress_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=stress_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=mental_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=mental_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=expectation_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=expectation_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=care_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=care_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=outreach_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=outreach_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=mim_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=mim_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=trials_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=trials_pie
                        )
                    ]
                ),
            ]
        ),
        
        html.Div(
            className='graph-row',
            children=[
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=healthy_cuts_fig
                        )
                    ]
                ),
                html.Div(
                    className='graph-box',
                    children=[
                        dcc.Graph(
                            className='graph',
                            figure=healthy_cuts_pie
                        )
                    ]
                ),
            ]
        ),
    ]
),

# ============================= Data Table ========================== #


            
    html.Div(
        className='data-box',
        children=[
            html.H1(
                className='data-title',
                children=f'Client Feedback Table'
            ),
            # html.Div(  
            #     className='table-scroll',
            #     children=[
            #         dcc.Graph(
            #             className='data',
            #             figure=df_table,
            #                 # style={'height': '800px'}, 
            #                 config={'responsive': True}
            #         )
            #     ]
            # )
            
            dash_table.DataTable(
                id='applications-table',
                data=data,
                columns=columns,
                page_size=14,
                sort_action='native',
                filter_action='native',
                row_selectable='multi',
                style_table={
                    'overflowX': 'auto',
                    # 'border': '3px solid #000',
                    # 'borderRadius': '0px'
                },
                style_cell={
                    'textAlign': 'left',
                    'minWidth': '100px', 
                    'whiteSpace': 'normal'
                },
                style_header={
                    'textAlign': 'center', 
                    'fontWeight': 'bold',
                    'backgroundColor': '#34A853', 
                    'color': 'white'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell_conditional=[
                    # make the index column narrow and centered
                    {'if': {'column_id': '#'},
                    'width': '20px', 'minWidth': '60px', 'maxWidth': '60px', 'textAlign': 'center'},
                    {'if': {'column_id': 'Timestamp'},
                    'width': '170px', 'minWidth': '100px', 'maxWidth': '200px', 'textAlign': 'center'},
                    {'if': {'column_id': 'Impression'},
                    'width': '650px', 'minWidth': '650px', 'maxWidth': '650px', 'textAlign': 'left'},
                ]
            ),
        ]
    ),
])

if __name__ == '__main__':
    print(f"Serving Flask app '{current_file}'! 🚀")
    app.run(debug=
                   True)
                #    False)
# =================================== Updated Database ================================= #

# updated_path = f'data/Survey_{current_quarter}_{report_year}.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# df.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path1 = 'data/service_tracker_q4_2024_cleaned.csv'
# data_path1 = os.path.join(script_dir, updated_path1)
# df.to_csv(data_path1, index=False)
# print(f"DataFrame saved to {data_path1}")

# -------------------------------------------- KILL PORT ---------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application -------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn impact_11_2024:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv 
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# pywin32
# jupytercore

# ----------------------------------------------------

# Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.

# Heroku Setup:
# heroku login
# heroku create survey-jun-25
# heroku git:remote -a survey-jun-25
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a mc-impact-11-2024

# Set buildpack for heroku
# heroku buildpacks:set heroku/python

# Heatmap Colorscale colors -----------------------------------------------------------------------------

#   ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
            #  'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
            #  'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
            #  'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            #  'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
            #  'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
            #  'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
            #  'ylorrd'].