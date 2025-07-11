import streamlit as st
import datetime
import math

st.set_page_config(page_title="📘 CA Exam Planner", layout="centered")

st.title("📚 CA Exam Planner")
group = st.radio("Select the group you are preparing for:", ["Group I", "Group II", "Both Groups"])

exam_date = st.date_input("📅 Select your CA Exam Date", min_value=datetime.date.today())
today = datetime.date.today()
remaining_days = (exam_date - today).days

if remaining_days <= 0:
    st.warning("Please select a valid future date for the exam.")
    st.stop()

# ---------- Subject and Chapter Data (Full Final Version) ----------
subjects_data = {
    "Group I": {
        "Advance Accounting": [
            "Accounting Policies (AS-1)", "Valuation of Inventories (AS-2)", "Cash Flow Statements (AS-3)",
            "Contingencies & Events after BS date (AS-4)", "Net Profits (AS-5)", "Construction Contracts (AS-7)",
            "Revenue Recognition (AS-9)", "PPE (AS-10)", "Foreign Exchange (AS-11)", "Government Grants (AS-12)",
            "Investment Accounts (AS-13)", "Amalgamation of Companies (AS-14)", "Retirement Benefits (AS-15)",
            "Borrowing Cost (AS-16)", "Segment Reporting (AS-17)", "Related Party Disclosures (AS-18)",
            "Lease Accounting (AS-19)", "Earning Per Share (AS-20)", "Consolidation of Accounts (AS-21)",
            "Accounting for Taxes on Income (AS-22)", "Associates (AS-23)", "Discontinuing Operation (AS-24)",
            "Interim Financial Reporting (AS-25)", "Intangible Assets (AS-26)", "Joint Ventures (AS-27)",
            "Impairment of Assets (AS-28)", "Provisions & Contingent Liability (AS-29)",
            "Branch Accounting", "Buy Back of Shares", "Company Final Accounts", "Internal Reconstruction", "Schedule III"
        ],
        "Corporate and Other Laws": [
            "Preliminary", "Incorporation of Company & Matters Incidental Thereto",
            "Prospectus and Allotment of Securities", "Share Capital & Debentures",
            "Acceptance of Deposits by Companies", "Registration of Charges",
            "Management & Administration", "Declaration and Payment of Dividend",
            "Accounts of Companies", "Audit & Auditors", "Companies Incorporated Outside India",
            "The LLP Act, 2008", "The FEMA, 1999", "The GCA, 1897", "Interpretation of Statutes"
        ],
        "Taxation": {
            "Income Tax": [
                "Basic Concepts", "Residence & Scope of Total Income", "Income from Salary",
                "Income from House Property", "PGBP", "Capital Gain", "IFOS",
                "Income of Other Persons Included in Assessee's Total Income",
                "Set off and Carry Forward of Losses", "Deductions from GTI",
                "Advance Tax, TDS and TCS", "Provisions for Filing Return of Income and Self Assessment",
                "Income Tax Liability Computation and Optimisation"
            ],
            "GST": [
                "Introduction and Constitution", "Definitions", "Chargeability and Goods & Services",
                "Supply", "Place of Supply", "Taxable Person", "Exemption", "Valuation",
                "Reverse Charge Mechanism", "Invoice", "Time of Supply", "Registration",
                "Input Tax Credit", "Manner of Payment", "TDS, TCS", "Filing of Return",
                "Accounts and Records", "E-Way Bill"
            ]
        }
    },
    "Group II": {
        "Cost and Management Accounting": [
            "Introduction to CMA", "Material Cost", "Employee Cost", "Overheads – Absorption Costing Method",
            "Activity Based Costing", "Cost Sheet", "Cost Accounting System", "Unit and Batch Costing",
            "Job Costing", "Process and Operation Costing", "Joint & By-products", "Service Costing",
            "Standard Costing", "Marginal Costing", "Budget and Budgetary Controls"
        ],
        "Auditing & Ethics": [
            "Nature, Objectives & Scope of Audit", "Introduction", "SA 210", "SQC-1/SA 220 + Ethics",
            "Audit Strategy, Planning & Programme", "Audit Documentation", "Risk Assessment & Internal Control",
            "Audit Procedures", "Materiality", "Materiality SA 320", "Sampling SA 530",
            "Evaluation of Misstatements(SA 450)", "Automated Environment", "SA 500/501/505/510",
            "SA 500", "SA 501", "SA 505", "SA 510", "SA 550/560/570/580", "SA 550", "SA 560", "SA 570",
            "SA 580", "Communication with Mgmt & TCWG(SA 260/265)", "Analytical Procedures",
            "Audit Report", "SA 700", "SA 701", "SA 705", "SA 706", "SA 710", "Branch Audit & SA 600",
            "SA 299", "CARO & Company Audit", "CARO 2020", "Company Audit", "Bank Audit",
            "Government Audit", "Cooperative Society Audit", "Other Audit", "Local Bodies", "NGOs",
            "Sole trader & Firm", "LLP", "Charitable Institution", "Educational Institutions",
            "Hospitals", "Club", "Cinema", "Hire Purchase & Leases", "Hotels", "Trusts & Societies",
            "Audit of Items of FS", "Internal Audit & SA 610"
        ],
        "FMSM": {
            "Financial Management": [
                "Scope and Objectives of FM", "Types of Financing", "Ratio Analysis",
                "Cost of Capital", "Capital Structure", "Leverage",
                "Investment Decisions – Capital Budgeting", "Dividend Decisions",
                "Management of Working Capital"
            ],
            "Strategic Management": [
                "Introduction to Strategic Management", "Strategic Analysis: External Environment",
                "Strategic Analysis: Internal Environment", "Strategic Choices",
                "Strategy Implementation & Evaluation"
            ]
        }
    }
}

# -------- Group-wise Subject Load --------
if group == "Group I":
    selected_subjects_data = subjects_data["Group I"]
elif group == "Group II":
    selected_subjects_data = subjects_data["Group II"]
else:
    selected_subjects_data = {**subjects_data["Group I"], **subjects_data["Group II"]}

# -------- Subject Selection (Max 6) --------
st.subheader("✅ Select Subjects You Want to Study (Max 6)")
subject_options = list(selected_subjects_data.keys())
chosen_subjects = st.multiselect("Choose subjects:", subject_options)

if len(chosen_subjects) > 6:
    st.error("You can select up to 6 subjects only.")
    st.stop()
elif len(chosen_subjects) == 0:
    st.warning("Please select at least one subject to continue.")
    st.stop()

# -------- Chapter Selection Under Each Subject --------
st.subheader("📌 Select Chapters under Each Subject")
final_selected_chapters = []

for subject in chosen_subjects:
    content = selected_subjects_data[subject]
    if isinstance(content, dict):
        for sub_part, chapters in content.items():
            selected = st.multiselect(f"{subject} - {sub_part}", chapters, key=f"{subject}_{sub_part}")
            final_selected_chapters.extend([f"{subject} - {sub_part}: {ch}" for ch in selected])
    else:
        selected = st.multiselect(subject, content, key=subject)
        final_selected_chapters.extend([f"{subject}: {ch}" for ch in selected])

# -------- Study Plan Generator --------
if len(final_selected_chapters) == 0:
    st.warning("Please select at least one chapter to generate plan.")
    st.stop()

chapters_per_day = math.ceil(len(final_selected_chapters) / remaining_days)
st.success(f"📆 Study Plan Generated for {len(final_selected_chapters)} Chapters over {remaining_days} days!")

st.subheader("🗓️ Daily Study Plan")
chapter_index = 0
for day in range(remaining_days):
    st.markdown(f"### Day {day + 1} – {today + datetime.timedelta(days=day)}")
    for _ in range(chapters_per_day):
        if chapter_index < len(final_selected_chapters):
            st.markdown(f"✅ {final_selected_chapters[chapter_index]}")
            chapter_index += 1
