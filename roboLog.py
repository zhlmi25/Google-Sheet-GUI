import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Robot Deployment System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= THEME TOGGLE =================
# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ================= CUSTOM CSS - DARK BLUE THEME =================
# Main color: #163859 (Dark Blue)
dark_theme_css = """
<style>
    /* Dark Mode - Dark Blue Theme */
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    
    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 9999;
        background-color: #163859;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(22, 56, 89, 0.3);
        transition: all 0.3s;
    }
    
    .theme-toggle:hover {
        background-color: #1F4A6F;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(22, 56, 89, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #163859 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #0F2942;
        color: white;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    /* Main content text */
    p, span, div, label {
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #163859;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1F4A6F;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(22, 56, 89, 0.3);
    }
    
    /* Primary button */
    .stButton>button[kind="primary"] {
        background-color: #2A5F85;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: #356F95;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #5BA3D0 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    /* Tables */
    .dataframe {
        background-color: #2a2a2a !important;
        color: white !important;
        border: 1px solid #163859 !important;
    }
    
    .dataframe th {
        background-color: #163859 !important;
        color: white !important;
    }
    
    .dataframe td {
        color: white !important;
        background-color: #2a2a2a !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input {
        background-color: #2a2a2a !important;
        color: white !important;
        border-color: #163859 !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        border-color: #1F4A6F !important;
        box-shadow: 0 0 0 1px #1F4A6F !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #1a4d2e;
        color: white !important;
        border-left: 4px solid #28a745;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #4d3a1a;
        color: white !important;
        border-left: 4px solid #ffc107;
    }
    
    /* Error messages */
    .stError {
        background-color: #4d1a1a;
        color: white !important;
        border-left: 4px solid #dc3545;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #1a2d4d;
        color: white !important;
        border-left: 4px solid #17a2b8;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2a2a2a;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: white !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #163859 !important;
        color: white !important;
    }
    
    /* Multiselect */
    .stMultiSelect>div>div {
        background-color: #2a2a2a;
        color: white;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #0F2942;
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #2a2a2a;
        color: white !important;
    }
</style>
"""

light_theme_css = """
<style>
    /* Light Mode - Dark Blue Theme */
    .stApp {
        background-color: #f5f5f5;
        color: #1a1a1a;
    }
    
    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 9999;
        background-color: #163859;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(22, 56, 89, 0.3);
        transition: all 0.3s;
    }
    
    .theme-toggle:hover {
        background-color: #1F4A6F;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(22, 56, 89, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #163859 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #0F2942;
        color: white;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    
    /* Main content text */
    p, span, div, label {
        color: #1a1a1a !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #163859;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1F4A6F;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(22, 56, 89, 0.3);
    }
    
    /* Primary button */
    .stButton>button[kind="primary"] {
        background-color: #2A5F85;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: #356F95;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #163859 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #1a1a1a !important;
    }
    
    /* Tables */
    .dataframe {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 1px solid #163859 !important;
    }
    
    .dataframe th {
        background-color: #163859 !important;
        color: white !important;
    }
    
    .dataframe td {
        color: #1a1a1a !important;
        background-color: white !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input {
        background-color: white !important;
        color: #1a1a1a !important;
        border-color: #163859 !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        border-color: #1F4A6F !important;
        box-shadow: 0 0 0 1px #1F4A6F !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #d4edda;
        color: #1a1a1a !important;
        border-left: 4px solid #28a745;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fff3cd;
        color: #1a1a1a !important;
        border-left: 4px solid #ffc107;
    }
    
    /* Error messages */
    .stError {
        background-color: #f8d7da;
        color: #1a1a1a !important;
        border-left: 4px solid #dc3545;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #d1ecf1;
        color: #1a1a1a !important;
        border-left: 4px solid #17a2b8;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e0e0e0;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #163859 !important;
        color: white !important;
    }
    
    /* Multiselect */
    .stMultiSelect>div>div {
        background-color: white;
        color: #1a1a1a;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #0F2942;
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white;
        color: #1a1a1a !important;
    }
</style>
"""

# Apply theme based on session state
if st.session_state.theme == 'dark':
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# ================= CONFIG =================
SERVICE_ACCOUNT_FILE = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_ID = "1DpQkaLbjoF86CjwiJymPY3e7EHYH6Qh6dUL0o7IbDiQ"

# ================= AUTH =================
@st.cache_resource
def get_google_sheet():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID)

try:
    sheet = get_google_sheet()
except Exception as e:
    st.error(f"Failed to connect to Google Sheets: {e}")
    st.stop()

# ================= HELPERS =================
def get_worksheet(name):
    try:
        return sheet.worksheet(name)
    except gspread.WorksheetNotFound:
        st.error(f"❌ Worksheet '{name}' not found")
        return None

def normalize(value):
    return str(value).strip().lower()

def append_row_by_header(sheet_name, data: dict):
    ws = get_worksheet(sheet_name)
    if not ws:
        return False
    headers = ws.row_values(1)
    row = [""] * len(headers)
    for key, value in data.items():
        if key in headers:
            row[headers.index(key)] = str(value)
    ws.append_row(row)
    return True

def fetch_all(sheet_name):
    ws = get_worksheet(sheet_name)
    if not ws:
        return []
    return ws.get_all_records()

# Add caching wrapper with longer TTL
@st.cache_data(ttl=300)  # Cache for 5 minutes (300 seconds) to avoid rate limits
def fetch_all_cached(sheet_name):
    """Cached version of fetch_all to reduce API calls. Data refreshes every 5 minutes."""
    import time
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            return fetch_all(sheet_name)
        except Exception as e:
            if "429" in str(e) or "RATE_LIMIT" in str(e):
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    st.warning(f"⏳ Rate limit reached. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    st.error("❌ Rate limit exceeded. Please wait a minute and refresh the page.")
                    return []
            else:
                raise e
    return []

def find_robot(serial_number):
    ws = get_worksheet("Robot Log")
    if not ws:
        return None
    headers = ws.row_values(1)
    serial_col = None
    for i, h in enumerate(headers):
        if h.strip().lower() == "serial number":
            serial_col = i
            break
    if serial_col is None:
        return None
    target = normalize(serial_number)
    rows = ws.get_all_values()
    for row in rows[1:]:
        if normalize(row[serial_col]) == target:
            return dict(zip(headers, row))
    return None

def update_robot(serial_number, updates: dict):
    ws = get_worksheet("Robot Log")
    if not ws:
        return False
    headers = ws.row_values(1)
    serial_col = None
    for i, h in enumerate(headers):
        if h.strip().lower() == "serial number":
            serial_col = i
            break
    if serial_col is None:
        return False
    target = normalize(serial_number)
    rows = ws.get_all_values()
    for row_idx, row in enumerate(rows[1:], start=2):
        if normalize(row[serial_col]) == target:
            for key, value in updates.items():
                for col_idx, h in enumerate(headers, start=1):
                    if h.strip().lower() == key.strip().lower():
                        ws.update_cell(row_idx, col_idx, str(value))
            return True
    return False

def check_mac_exists(mac_address, exclude_serial=None):
    robots = fetch_all_cached("Robot Log")
    for r in robots:
        if normalize(r.get("MAC Address", "")) == normalize(mac_address):
            if exclude_serial and normalize(r.get("Serial Number", "")) == normalize(exclude_serial):
                continue
            return True
    return False

def delete_robot_row(serial_number):
    """Actually delete the row from Robot Log sheet"""
    ws = get_worksheet("Robot Log")
    if not ws:
        return False
    headers = ws.row_values(1)
    serial_col = None
    for i, h in enumerate(headers):
        if h.strip().lower() == "serial number":
            serial_col = i
            break
    if serial_col is None:
        return False
    target = normalize(serial_number)
    rows = ws.get_all_values()
    for row_idx, row in enumerate(rows[1:], start=2):
        if normalize(row[serial_col]) == target:
            ws.delete_rows(row_idx)
            return True
    return False

def set_client_inactive_by_serial(serial_number):
    """Set Deployment Status to Inactive for all client rows matching a serial number"""
    ws = get_worksheet("Client Log")
    if not ws:
        return
    headers = ws.row_values(1)
    serial_col = None
    status_col = None
    for i, h in enumerate(headers):
        if h.strip().lower() == "serial number":
            serial_col = i
        if h.strip().lower() == "deployment status":
            status_col = i
    if serial_col is None or status_col is None:
        return
    target = normalize(serial_number)
    rows = ws.get_all_values()
    for row_idx, row in enumerate(rows[1:], start=2):
        if normalize(row[serial_col]) == target:
            ws.update_cell(row_idx, status_col + 1, "Inactive")

def delete_client_row(row_index):
    """Delete a client row. row_index is 0-based index from get_all_records list"""
    ws = get_worksheet("Client Log")
    if not ws:
        return False
    # +2 because: +1 for header row, +1 because sheet rows are 1-based
    ws.delete_rows(row_index + 2)
    return True

def update_client_row(row_index, updates: dict):
    """Update a client row. row_index is 0-based index from get_all_records list"""
    ws = get_worksheet("Client Log")
    if not ws:
        return False
    headers = ws.row_values(1)
    sheet_row = row_index + 2  # +2: header + 1-based
    for key, value in updates.items():
        for col_idx, h in enumerate(headers, start=1):
            if h.strip().lower() == key.strip().lower():
                ws.update_cell(sheet_row, col_idx, str(value))
    return True

# ================= MAIN APP =================
# Theme toggle button (top left)
col_toggle, col_title, col_refresh = st.columns([1, 9, 2])
with col_toggle:
    if st.session_state.theme == 'dark':
        if st.button("☀️ Light", key="theme_toggle", help="Switch to Light Mode"):
            st.session_state.theme = 'light'
            st.cache_data.clear()
            st.rerun()
    else:
        if st.button("🌙 Dark", key="theme_toggle", help="Switch to Dark Mode"):
            st.session_state.theme = 'dark'
            st.cache_data.clear()
            st.rerun()

with col_title:
    st.title("🤖 Robot Deployment System")

with col_refresh:
    if st.button("🔄 Refresh Data", help="Clear cache and reload data from Google Sheets"):
        st.cache_data.clear()
        st.success("✅ Cache cleared!")
        st.rerun()

# Show cache info
st.caption("💡 Data is cached for 5 minutes to avoid API limits. Click 'Refresh Data' to force update.")

# Check if there's a page in query params (from quick actions)
query_params = st.query_params
if "page" in query_params:
    default_menu = query_params["page"]
else:
    default_menu = "Home"

menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Add Robot", "Deploy Robot", "Add Maintenance",
     "View Robot Log", "View Client Log", "View Maintenance Log"],
    index=["Home", "Add Robot", "Deploy Robot", "Add Maintenance",
           "View Robot Log", "View Client Log", "View Maintenance Log"].index(default_menu) if default_menu in ["Home", "Add Robot", "Deploy Robot", "Add Maintenance", "View Robot Log", "View Client Log", "View Maintenance Log"] else 0
)

# ================= HOME =================
if menu == "Home":
    st.header("Welcome to Robot Deployment System")
    
    # Fetch all data ONCE with caching
    robots = fetch_all_cached("Robot Log")
    clients = fetch_all_cached("Client Log")
    robot_types_data = fetch_all_cached("Robot Model")
    
    # Count unique client names
    unique_clients = set()
    for c in clients:
        client_name = str(c.get("Client Name", "")).strip()
        if client_name:
            unique_clients.add(client_name.lower())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Robots", len(robots))
    with col2:
        active = sum(1 for r in robots if normalize(r.get("Status", "")) == "active")
        st.metric("Active Robots", active)
    with col3:
        st.metric("Unique Clients", len(unique_clients))

    st.markdown("---")
    
    # Robot Type Statistics - Card Layout
    st.subheader("📊 Robot Types Overview")
    
    # Count by robot model
    robot_stats = {}
    for r in robots:
        model = str(r.get("Robot Model", "Unknown")).strip()
        status = normalize(r.get("Status", ""))
        
        if model not in robot_stats:
            robot_stats[model] = {"total": 0, "deployed": 0, "idle": 0, "maintenance": 0, "retired": 0}
        
        robot_stats[model]["total"] += 1
        
        if status == "active":
            robot_stats[model]["deployed"] += 1
        elif status == "idle":
            robot_stats[model]["idle"] += 1
        elif status == "maintenance":
            robot_stats[model]["maintenance"] += 1
        elif status == "retired":
            robot_stats[model]["retired"] += 1
    
    if robot_stats:
        # Create smooth card layout - 3 cards per row
        sorted_models = sorted(robot_stats.items())
        
        # Custom CSS for cards
        st.markdown("""
        <style>
        .robot-card {
            background: linear-gradient(135deg, #163859 0%, #0F2942 100%);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(22, 56, 89, 0.3);
            margin-bottom: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .robot-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(22, 56, 89, 0.5);
        }
        .robot-card-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: white;
            margin-bottom: 15px;
            text-align: center;
        }
        .robot-card-total {
            font-size: 2.5rem;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            margin: 10px 0;
        }
        .robot-card-stats {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
        .robot-stat-item {
            text-align: center;
        }
        .robot-stat-label {
            font-size: 0.8rem;
            color: rgba(255,255,255,0.8);
            margin-bottom: 5px;
        }
        .robot-stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
        }
        .status-deployed { color: #90EE90; }
        .status-idle { color: #87CEEB; }
        .status-maintenance { color: #FFD700; }
        </style>
        """, unsafe_allow_html=True)
        
        # Display cards in rows of 3
        for i in range(0, len(sorted_models), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(sorted_models):
                    model, counts = sorted_models[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="robot-card">
                            <div class="robot-card-title">🤖 {model}</div>
                            <div class="robot-card-total">{counts['total']}</div>
                            <div style="text-align: center; color: rgba(255,255,255,0.9); font-size: 0.9rem;">Total Units</div>
                            <div class="robot-card-stats">
                                <div class="robot-stat-item">
                                    <div class="robot-stat-label">Deployed</div>
                                    <div class="robot-stat-value status-deployed">{counts['deployed']}</div>
                                </div>
                                <div class="robot-stat-item">
                                    <div class="robot-stat-label">Idle</div>
                                    <div class="robot-stat-value status-idle">{counts['idle']}</div>
                                </div>
                                <div class="robot-stat-item">
                                    <div class="robot-stat-label">Maintenance</div>
                                    <div class="robot-stat-value status-maintenance">{counts['maintenance']}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("No robot data available")

    st.markdown("---")
    
    # Manage Robot Types Section
    st.subheader("⚙️ Manage Robot Types")
    
    # Use already fetched robot_types_data
    existing_types = [r.get("Robot Type", "") for r in robot_types_data if r.get("Robot Type", "")]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Add New Robot Type:**")
        new_robot_type = st.text_input("Enter Robot Type Name", placeholder="e.g., Delivery Robot, Cleaning Robot", key="new_robot_type")
        
        if st.button("➕ Add Robot Type", use_container_width=True):
            if new_robot_type.strip():
                # Check if already exists
                if new_robot_type.strip() in existing_types:
                    st.error("❌ This robot type already exists!")
                else:
                    success = append_row_by_header("Robot Model", {
                        "Robot Type": new_robot_type.strip()
                    })
                    if success:
                        st.success(f"✅ Robot type '{new_robot_type}' added successfully!")
                        # Clear cache to refresh data
                        st.cache_data.clear()
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("❌ Failed to add robot type")
            else:
                st.error("❌ Please enter a robot type name")
    
    with col2:
        st.write("**Existing Robot Types:**")
        if existing_types:
            for robot_type in existing_types:
                st.markdown(f"• {robot_type}")
        else:
            st.info("No robot types defined yet")

    st.markdown("---")
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add New Robot", use_container_width=True, key="home_add_robot"):
            # Use query params to navigate
            st.query_params["page"] = "Add Robot"
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button("🚀 Deploy Robot", use_container_width=True, key="home_deploy_robot"):
            st.query_params["page"] = "Deploy Robot"
            st.cache_data.clear()
            st.rerun()
    with col3:
        if st.button("🔧 Add Maintenance", use_container_width=True, key="home_add_maintenance"):
            st.query_params["page"] = "Add Maintenance"
            st.cache_data.clear()
            st.rerun()

# ================= ADD ROBOT =================
elif menu == "Add Robot":
    st.header("➕ Add New Robot")
    
    # Fetch robot types from Robot Model sheet
    robot_types_data = fetch_all_cached("Robot Model")
    available_types = [r.get("Robot Type", "") for r in robot_types_data if r.get("Robot Type", "")]
    
    if not available_types:
        st.warning("⚠️ No robot types available. Please add robot types on the Home page first.")
        if st.button("← Go to Home to Add Robot Types"):
            st.query_params["page"] = "Home"
            st.cache_data.clear()
            st.rerun()
    else:
        with st.form("add_robot_form"):
            col1, col2 = st.columns(2)
            with col1:
                robot_model = st.selectbox("Robot Model *", options=available_types, help="Select from predefined robot types")
                serial_number = st.text_input("Serial Number *", placeholder="e.g., SN123456")
                mac_address = st.text_input("MAC Address *", placeholder="e.g., 00:1B:44:11:3A:B7")
            with col2:
                cloud_period = st.number_input("Cloud Activation Period (Months) *", min_value=1, value=12)
                cloud_date = st.date_input("Cloud Activation Date *", value=datetime.today())
                cloud_store_group = st.text_input("Cloud Store Group (Optional)")

            submitted = st.form_submit_button("Add Robot", use_container_width=True)
            if submitted:
                if not all([robot_model, serial_number, mac_address]):
                    st.error("❌ Please fill in all required fields")
                elif find_robot(serial_number):
                    st.error(f"❌ Serial Number '{serial_number}' already exists!")
                elif check_mac_exists(mac_address, None):
                    st.error(f"❌ MAC Address '{mac_address}' already exists!")
                else:
                    try:
                        activation_date = datetime.combine(cloud_date, datetime.min.time())
                        cloud_expiry = (activation_date + timedelta(days=int(cloud_period) * 30)).strftime("%Y-%m-%d")
                    except:
                        cloud_expiry = ""

                    success = append_row_by_header("Robot Log", {
                        "Robot Model": robot_model,
                        "Serial Number": serial_number,
                        "MAC Address": mac_address,
                        "Cloud Activation Period (Months)": str(cloud_period),
                        "Cloud Activation Date": cloud_date.strftime("%Y-%m-%d"),
                        "Cloud Expiry": cloud_expiry,
                        "Cloud Store Group": cloud_store_group,
                        "Maintenance Plan": "",
                        "Outlet using": "",
                        "Status": "Idle"
                    })
                    if success:
                        st.success(f"✅ Robot '{robot_model}' added successfully!")
                        st.cache_data.clear()
                        st.balloons()
                    else:
                        st.error("❌ Failed to add robot")

# ================= DEPLOY ROBOT =================
elif menu == "Deploy Robot":
    st.header("🚀 Deploy Robot")

    all_robots = fetch_all_cached("Robot Log")
    idle_robots = [r for r in all_robots if normalize(r.get("Status", "")) == "idle"]

    if not idle_robots:
        st.warning("⚠️ No idle robots available for deployment")
    else:
        with st.form("deploy_robot_form"):
            col1, col2 = st.columns(2)
            with col1:
                client_name = st.text_input("Client Name *", placeholder="e.g., ABC Restaurant")
                location = st.text_input("Location *", placeholder="e.g., Kuala Lumpur")
                cloud_store_group = st.text_input("Cloud Store Group *", placeholder="e.g., Group A")

            with col2:
                robot_options = [f"{r['Serial Number']} - {r['Robot Model']}" for r in idle_robots]
                # multiselect allows picking multiple robots
                selected_robots = st.multiselect("Select Robot(s) *", robot_options)
                maintenance_package = st.selectbox("Maintenance Package *", ["Purchased", "Leasing"])

            submitted = st.form_submit_button("Deploy Robot(s)", use_container_width=True)

            if submitted:
                if not all([client_name, location, cloud_store_group]) or len(selected_robots) == 0:
                    st.error("❌ Please fill in all required fields and select at least one robot")
                else:
                    all_ok = True
                    deployed_list = []

                    for sel in selected_robots:
                        robot_serial = sel.split(" - ")[0]
                        robot = find_robot(robot_serial)

                        if not robot:
                            st.error(f"❌ Robot {robot_serial} not found")
                            all_ok = False
                            continue

                        if normalize(robot["Status"]) != "idle":
                            st.error(f"❌ Robot {robot_serial} is not idle (Current: {robot['Status']})")
                            all_ok = False
                            continue

                        # Update robot status + maintenance plan + cloud store group
                        update_robot(robot_serial, {
                            "Status": "Active",
                            "Outlet using": client_name,
                            "Maintenance Plan": maintenance_package,
                            "Cloud Store Group": cloud_store_group
                        })

                        # Add one row per robot in Client Log
                        append_row_by_header("Client Log", {
                            "Client Name": client_name,
                            "Location": location,
                            "Date of deployment": datetime.today().strftime("%Y-%m-%d"),
                            "Deplyoment Type": "Deployment",
                            "Deployment Status": "Active",
                            "Maintance Package": maintenance_package,
                            "Cloud Store Group": cloud_store_group,
                            "Robot Deployed": robot.get("Robot Model", ""),
                            "Serial Number": robot_serial,
                            "MAC Address": robot.get("MAC Address", "")
                        })

                        deployed_list.append(f"{robot_serial} ({robot.get('Robot Model', '')})")

                    if all_ok and deployed_list:
                        st.success(f"✅ Deployed {len(deployed_list)} robot(s) to {client_name}:\n" + "\n".join(f"  • {d}" for d in deployed_list))
                        st.cache_data.clear()
                        st.balloons()
                    elif deployed_list:
                        st.warning(f"⚠️ Deployed {len(deployed_list)} robot(s) but some failed. Check errors above.")

# ================= ADD MAINTENANCE =================
elif menu == "Add Maintenance":
    st.header("🔧 Add Maintenance")

    all_robots = fetch_all_cached("Robot Log")
    active_robots = [r for r in all_robots if normalize(r.get("Status", "")) == "active"]

    if not active_robots:
        st.warning("⚠️ No active robots available for maintenance")
    else:
        with st.form("maintenance_form"):
            col1, col2 = st.columns(2)
            with col1:
                robot_options = [f"{r['Serial Number']} - {r['Robot Model']} ({r.get('Outlet using', 'N/A')})" for r in active_robots]
                selected_robot = st.selectbox("Select Robot *", robot_options)
                problem = st.text_area("Problem Details *", placeholder="Describe the issue...")
            with col2:
                solution = st.text_area("Solution *", placeholder="Describe the solution...")
                remarks = st.text_input("Remarks (Optional)")

            submitted = st.form_submit_button("Add Maintenance Record", use_container_width=True)
            if submitted:
                if not all([selected_robot, problem, solution]):
                    st.error("❌ Please fill in all required fields")
                else:
                    robot_serial = selected_robot.split(" - ")[0]
                    robot = find_robot(robot_serial)
                    if not robot:
                        st.error("❌ Robot not found")
                    else:
                        success = append_row_by_header("Maintenance and troubleshooting log", {
                            "Date of Issue": datetime.today().strftime("%Y-%m-%d"),
                            "Client Name": robot.get("Outlet using", ""),
                            "Location of Robot": "",
                            "Robot Model": robot.get("Robot Model", ""),
                            "Serial Number": robot_serial,
                            "MAC Address": robot.get("MAC Address", ""),
                            "Problem details": problem,
                            "Solution": solution,
                            "Remarks": remarks,
                            "Status": "Open"
                        })
                        if success:
                            st.success("✅ Maintenance record added successfully!")
                            st.cache_data.clear()
                            st.balloons()
                        else:
                            st.error("❌ Failed to add maintenance record")

# ================= VIEW ROBOT LOG =================
elif menu == "View Robot Log":
    st.header("📋 Robot Log")
    robots = fetch_all_cached("Robot Log")

    if not robots:
        st.info("No robots found")
    else:
        df = pd.DataFrame(robots)

        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Filter by Status",
                options=df["Status"].unique().tolist() if "Status" in df.columns else [],
                default=df["Status"].unique().tolist() if "Status" in df.columns else [])
        with col2:
            model_filter = st.multiselect("Filter by Model",
                options=df["Robot Model"].unique().tolist() if "Robot Model" in df.columns else [],
                default=df["Robot Model"].unique().tolist() if "Robot Model" in df.columns else [])
        with col3:
            search = st.text_input("Search Serial Number", "")

        filtered_df = df.copy()
        if "Status" in filtered_df.columns and status_filter:
            filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]
        if "Robot Model" in filtered_df.columns and model_filter:
            filtered_df = filtered_df[filtered_df["Robot Model"].isin(model_filter)]
        if search and "Serial Number" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Serial Number"].str.contains(search, case=False, na=False)]

        st.dataframe(filtered_df, use_container_width=True, height=400)

        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download as CSV", data=csv,
            file_name=f"robot_log_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

        st.markdown("---")
        st.subheader("✏️ Edit or Delete Robot")

        robot_options = [f"{r['Serial Number']} - {r['Robot Model']}" for r in robots]
        selected_robot = st.selectbox("Select Robot to Edit/Delete", [""] + robot_options, key="edit_robot_select")

        if selected_robot:
            robot_serial = selected_robot.split(" - ")[0]
            robot = find_robot(robot_serial)

            if robot:
                tab1, tab2 = st.tabs(["✏️ Edit", "🗑️ Delete"])

                with tab1:
                    with st.form("edit_robot_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_model = st.text_input("Robot Model", value=robot.get("Robot Model", ""))
                            new_mac = st.text_input("MAC Address", value=robot.get("MAC Address", ""))
                            new_cloud_store = st.text_input("Cloud Store Group", value=robot.get("Cloud Store Group", ""))
                        with col2:
                            status_options = ["Idle", "Active", "Maintenance", "Retired"]
                            current_status = normalize(robot.get("Status", "idle"))
                            status_idx = status_options.index(current_status.capitalize()) if current_status.capitalize() in status_options else 0
                            new_status = st.selectbox("Status", status_options, index=status_idx)
                            new_outlet = st.text_input("Outlet using", value=robot.get("Outlet using", ""))
                            new_maintenance_plan = st.text_input("Maintenance Plan", value=robot.get("Maintenance Plan", ""))

                        submit_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                        if submit_edit:
                            if new_mac != robot.get("MAC Address", "") and check_mac_exists(new_mac, robot_serial):
                                st.error("❌ MAC Address already exists!")
                            else:
                                success = update_robot(robot_serial, {
                                    "Robot Model": new_model,
                                    "MAC Address": new_mac,
                                    "Cloud Store Group": new_cloud_store,
                                    "Status": new_status,
                                    "Outlet using": new_outlet,
                                    "Maintenance Plan": new_maintenance_plan
                                })
                                if success:
                                    st.success("✅ Robot updated successfully!")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update robot")

                with tab2:
                    st.warning("⚠️ **Warning:** This will permanently delete the robot from Robot Log.")
                    # Check if this robot exists in Client Log
                    clients = fetch_all_cached("Client Log")
                    linked_clients = [c for c in clients if normalize(str(c.get("Serial Number", ""))) == normalize(robot_serial)]

                    if linked_clients:
                        st.info(f"📋 This robot is linked to **{len(linked_clients)}** client deployment(s). "
                                f"Those deployments will be set to **Inactive** instead of being deleted.")

                    st.write(f"**Serial Number:** {robot.get('Serial Number', '')}")
                    st.write(f"**Model:** {robot.get('Robot Model', '')}")
                    st.write(f"**Status:** {robot.get('Status', '')}")

                    confirm_delete = st.text_input("Type 'DELETE' to confirm:", key="confirm_robot_delete")
                    if st.button("🗑️ Delete Robot", type="primary", use_container_width=True):
                        if confirm_delete == "DELETE":
                            # If linked to client log, set those to Inactive first
                            if linked_clients:
                                set_client_inactive_by_serial(robot_serial)
                            # Now delete the robot row
                            success = delete_robot_row(robot_serial)
                            if success:
                                if linked_clients:
                                    st.success(f"✅ Robot deleted. {len(linked_clients)} client deployment(s) set to Inactive.")
                                else:
                                    st.success("✅ Robot deleted successfully!")
                                    st.cache_data.clear()
                                    st.rerun()
                            else:
                                st.error("❌ Failed to delete robot")
                        else:
                            st.error("❌ Please type 'DELETE' to confirm")

# ================= VIEW CLIENT LOG =================
elif menu == "View Client Log":
    st.header("👥 Client Log")
    clients = fetch_all_cached("Client Log")

    if not clients:
        st.info("No clients found")
    else:
        df = pd.DataFrame(clients)

        col1, col2 = st.columns(2)
        with col1:
            if "Deployment Status" in df.columns:
                status_filter = st.multiselect("Filter by Status",
                    options=df["Deployment Status"].unique().tolist(),
                    default=df["Deployment Status"].unique().tolist())
                filtered_df = df[df["Deployment Status"].isin(status_filter)]
            else:
                filtered_df = df.copy()
        with col2:
            search = st.text_input("Search Client Name", "")
            if search and "Client Name" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["Client Name"].str.contains(search, case=False, na=False)]

        st.dataframe(filtered_df, use_container_width=True, height=400)

        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download as CSV", data=csv,
            file_name=f"client_log_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

        # -------- RETRIEVE ROBOT SECTION --------
        st.markdown("---")
        st.subheader("🔄 Retrieve Robot")
        st.info("Select an active deployment to retrieve the robot. This will set the deployment to Inactive and the robot status back to Idle.")

        # Only show active deployments for retrieval
        active_clients = [c for c in clients if normalize(c.get("Deployment Status", "")) == "active"]
        if not active_clients:
            st.warning("⚠️ No active deployments to retrieve")
        else:
            retrieve_options = [
                f"Row {clients.index(c)+1}: {c.get('Client Name', '')} - {c.get('Serial Number', 'N/A')} ({c.get('Robot Deployed', '')})"
                for c in active_clients
            ]
            selected_retrieve = st.selectbox("Select Deployment to Retrieve", [""] + retrieve_options, key="retrieve_select")

            if selected_retrieve:
                # Find actual index in original clients list
                row_label = selected_retrieve.split(":")[0]  # "Row X"
                retrieve_row_idx = int(row_label.replace("Row ", "")) - 1
                retrieve_client = clients[retrieve_row_idx]
                retrieve_serial = str(retrieve_client.get("Serial Number", ""))

                st.write(f"**Client:** {retrieve_client.get('Client Name', '')}")
                st.write(f"**Location:** {retrieve_client.get('Location', '')}")
                st.write(f"**Robot:** {retrieve_client.get('Robot Deployed', '')} | SN: {retrieve_serial}")

                if st.button("🔄 Retrieve Robot", type="primary", use_container_width=True):
                    # Set client deployment to Inactive
                    client_ok = update_client_row(retrieve_row_idx, {
                        "Deployment Status": "Inactive"
                    })
                    # Set robot status back to Idle and clear outlet
                    robot_ok = update_robot(retrieve_serial, {
                        "Status": "Idle",
                        "Outlet using": ""
                    })

                    if client_ok and robot_ok:
                        st.success(f"✅ Robot {retrieve_serial} retrieved successfully! Deployment set to Inactive, robot set to Idle.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("❌ Failed to retrieve robot. Check logs.")

        # -------- EDIT / DELETE SECTION --------
        st.markdown("---")
        st.subheader("✏️ Edit or Delete Client Deployment")

        client_options = [
            f"Row {i+1}: {c.get('Client Name', '')} - {c.get('Serial Number', 'N/A')}"
            for i, c in enumerate(clients)
        ]
        selected_client = st.selectbox("Select Client Deployment to Edit/Delete", [""] + client_options, key="edit_client_select")

        if selected_client:
            row_idx = int(selected_client.split(":")[0].replace("Row ", "")) - 1
            client = clients[row_idx]

            tab1, tab2 = st.tabs(["✏️ Edit", "🗑️ Delete"])

            with tab1:
                with st.form("edit_client_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_client_name = st.text_input("Client Name", value=client.get("Client Name", ""))
                        new_location = st.text_input("Location", value=client.get("Location", ""))

                        dep_status_options = ["Active", "Inactive", "Completed", "Cancelled"]
                        current_dep = normalize(client.get("Deployment Status", "active"))
                        dep_idx = dep_status_options.index(current_dep.capitalize()) if current_dep.capitalize() in dep_status_options else 0
                        new_deployment_status = st.selectbox("Deployment Status", dep_status_options, index=dep_idx)

                    with col2:
                        maint_options = ["Purchased", "Leasing"]
                        current_maint = normalize(client.get("Maintance Package", "purchased"))
                        maint_idx = maint_options.index(current_maint.capitalize()) if current_maint.capitalize() in maint_options else 0
                        new_maintenance_package = st.selectbox("Maintenance Package", maint_options, index=maint_idx)

                        new_deployment_type = st.text_input("Deployment Type", value=client.get("Deplyoment Type", ""))
                        new_cloud_store_group = st.text_input("Cloud Store Group", value=client.get("Cloud Store Group", ""))

                    submit_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)

                    if submit_edit:
                        # Update client log
                        client_ok = update_client_row(row_idx, {
                            "Client Name": new_client_name,
                            "Location": new_location,
                            "Deployment Status": new_deployment_status,
                            "Maintance Package": new_maintenance_package,
                            "Deplyoment Type": new_deployment_type,
                            "Cloud Store Group": new_cloud_store_group
                        })

                        # Sync Maintenance Plan to Robot Log
                        client_serial = str(client.get("Serial Number", ""))
                        robot_ok = True
                        if client_serial:
                            robot_ok = update_robot(client_serial, {
                                "Maintenance Plan": new_maintenance_package
                            })

                        if client_ok and robot_ok:
                            st.success("✅ Client deployment updated! Maintenance Plan synced to Robot Log.")
                            st.cache_data.clear()
                            st.rerun()
                        elif client_ok:
                            st.warning("⚠️ Client updated but failed to sync Maintenance Plan to Robot Log.")
                        else:
                            st.error("❌ Failed to update client deployment")

            with tab2:
                st.warning("⚠️ **Warning:** This action cannot be undone!")
                st.write(f"**Client Name:** {client.get('Client Name', '')}")
                st.write(f"**Location:** {client.get('Location', '')}")
                st.write(f"**Serial Number:** {client.get('Serial Number', '')}")
                st.write(f"**Status:** {client.get('Deployment Status', '')}")

                confirm_delete = st.text_input("Type 'DELETE' to confirm:", key="confirm_client_delete")
                if st.button("🗑️ Delete Client Deployment", type="primary", use_container_width=True):
                    if confirm_delete == "DELETE":
                        success = delete_client_row(row_idx)
                        if success:
                            st.success("✅ Client deployment deleted successfully!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete client deployment")
                    else:
                        st.error("❌ Please type 'DELETE' to confirm")

# ================= VIEW MAINTENANCE LOG =================
elif menu == "View Maintenance Log":
    st.header("🔧 Maintenance Log")
    maintenance = fetch_all_cached("Maintenance and troubleshooting log")

    if not maintenance:
        st.info("No maintenance records found")
    else:
        df = pd.DataFrame(maintenance)

        col1, col2 = st.columns(2)
        with col1:
            if "Status" in df.columns:
                status_filter = st.multiselect("Filter by Status",
                    options=df["Status"].unique().tolist(),
                    default=df["Status"].unique().tolist())
                df = df[df["Status"].isin(status_filter)]
        with col2:
            search = st.text_input("Search Serial Number or Client", "")
            if search:
                mask = pd.Series([False] * len(df))
                if "Serial Number" in df.columns:
                    mask |= df["Serial Number"].astype(str).str.contains(search, case=False, na=False)
                if "Client Name" in df.columns:
                    mask |= df["Client Name"].astype(str).str.contains(search, case=False, na=False)
                df = df[mask]

        st.dataframe(df, use_container_width=True, height=400)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download as CSV", data=csv,
            file_name=f"maintenance_log_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ================= FOOTER =================
st.sidebar.markdown("---")
st.sidebar.info("💡 Use the navigation menu to access different features")