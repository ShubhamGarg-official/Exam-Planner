# ✅ Final CA Exam Planner App – All-In-One Version
# Features:
# - Study Hours input
# - Group selection (Group I / II / Both)
# - Start & End Dates
# - Subject & Chapter selection (with Select All)
# - Auto time-based chapter allocation
# - Excel export
# - Reset button

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="CA Exam Planner", layout="wide")
st.title("📘 CA Exam Planner")
st.markdown("Plan your revisions based on your available time, subjects, and goals.")

# ------------------ Full Subject Data ------------------
data = {
    "Group I": {
        "Advance Accounting": {
            "AS-1: Accounting Policies (1 hr)": 1,
            "AS-2: Valuation of Inventories (4 hrs)": 4,
            "AS-3: Cash Flow Statements (8 hrs)": 8,
            "AS-4: Contingencies & Events after Balance Sheet Date (2 hrs)": 2,
            "AS-5: Net Profits (2 hrs)": 2,
            "AS-7: Construction Contracts (4 hrs)": 4,
            "AS-9: Revenue Recognition (1 hr)": 1,
            "AS-10: Property, Plant and Equipment (3 hrs)": 3,
            "AS-11: Effects of Changes in Foreign Exchange Rates (4 hrs)": 4,
            "AS-12: Government Grants (3 hrs)": 3,
            "AS-13: Investments (6 hrs)": 6,
            "AS-14: Amalgamation of Companies (14 hrs)": 14,
            "AS-15: Retirement Benefits (2 hrs)": 2,
            "AS-16: Borrowing Costs (6 hrs)": 6,
            "AS-17: Segment Reporting (2 hrs)": 2,
            "AS-18: Related Party Disclosures (2 hrs)": 2,
            "AS-19: Leases (6 hrs)": 6,
            "AS-20: Earnings Per Share (4 hrs)": 4,
            "AS-21: Consolidated Financial Statements (12 hrs)": 12,
            "AS-22: Accounting for Taxes on Income (3 hrs)": 3,
            "AS-23: Investments in Associates (2 hrs)": 2,
            "AS-24: Discontinuing Operations (2 hrs)": 2,
            "AS-25: Interim Financial Reporting (2 hrs)": 2,
            "AS-26: Intangible Assets (3 hrs)": 3,
            "AS-27: Joint Ventures (2 hrs)": 2,
            "AS-28: Impairment of Assets (2 hrs)": 2,
            "AS-29: Provisions, Contingent Liabilities & Assets (2 hrs)": 2,
            "Schedule III (2 hrs)": 2,
            "Company Final Accounts (12 hrs)": 12,
            "Buy Back of Shares (4 hrs)": 4,
            "Internal Reconstruction (8 hrs)": 8,
            "Branch Accounting (16 hrs)": 16
        },
        "Corporate and Other Laws": {
            "Preliminary (2.5 hrs)": 2.5,
            "Incorporation of Company & Matters Incidental thereto (5 hrs)": 5,
            "Prospectus and Allotment of Securities (4 hrs)": 4,
            "Share Capital & Debentures (5 hrs)": 5,
            "Acceptance of Deposits by Companies (3 hrs)": 3,
            "Registration of Charges (2.5 hrs)": 2.5,
            "Management & Administration (7 hrs)": 7,
            "Declaration and Payment of Dividend (3 hrs)": 3,
            "Accounts of Companies (6 hrs)": 6,
            "Audit & Auditors (5 hrs)": 5,
            "Companies Incorporated Outside India (2 hrs)": 2,
            "The LLP Act, 2008 (4 hrs)": 4,
            "The FEMA, 1999 (3.5 hrs)": 3.5,
            "The General Clauses Act, 1897 (3.5 hrs)": 3.5,
            "Interpretation of Statutes (3.5 hrs)": 3.5
        },
        "Taxation": {
            "Income Tax": {
                "Basic Concepts (2 hrs)": 2,
                "Residence & Scope of Total Income (2 hrs)": 2,
                "Income from Salary (4 hrs)": 4,
                "Income from House Property (2 hrs)": 2,
                "Profits and Gains of Business or Profession (8 hrs)": 8,
                "Capital Gain (8 hrs)": 8,
                "Income from Other Sources (4 hrs)": 4,
                "Income of Other Persons (2 hrs)": 2,
                "Set-off & Carry Forward (2 hrs)": 2,
                "Deductions from GTI (6 hrs)": 6,
                "Advance Tax, TDS & TCS (5 hrs)": 5,
                "Return Filing & Self Assessment (2 hrs)": 2,
                "Tax Liability Computation & Optimisation (10 hrs)": 10
            },
            "GST": {
                "Introduction and Constitution (1 hr)": 1,
                "Definitions (1 hr)": 1,
                "Chargeability and Goods & Services (1 hr)": 1,
                "Supply (1 hr)": 1,
                "Place of Supply (1 hr)": 1,
                "Taxable Person (1 hr)": 1,
                "Exemption (3 hrs)": 3,
                "Valuation (1 hr)": 1,
                "Reverse Charge Mechanism (2 hrs)": 2,
                "Invoice (1 hr)": 1,
                "Time of Supply (1 hr)": 1,
                "Registration (1 hr)": 1,
                "Input Tax Credit (2 hrs)": 2,
                "Manner of Payment (1 hr)": 1,
                "TDS, TCS (1 hr)": 1,
                "Filing of Return (1 hr)": 1,
                "Accounts and Records (1 hr)": 1,
                "E-Way Bill (1 hr)": 1
            }
        }
    },
    "Group II": {
        "Auditing & Ethics": {
            "Nature, Objectives & Scope of Audit (4.5 hrs)": 4.5,
            "Audit Strategy, Planning & Programme (2 hrs)": 2,
            "Audit Documentation (1 hr)": 1,
            "Risk Assessment & Internal Control (3 hrs)": 3,
            "Audit Procedures (1 hr)": 1,
            "SA 320 / 450 / 530 (3.5 hrs)": 3.5,
            "Automated Environment (1.5 hrs)": 1.5,
            "SA 500 / 501 / 505 / 510 (3.5 hrs)": 3.5,
            "SA 550 / 560 / 570 / 580 (3 hrs)": 3,
            "Communication with Mgmt & TCWG (1 hr)": 1,
            "Analytical Procedures (1 hr)": 1,
            "Audit Report & Branch Audit (5 hrs)": 5,
            "CARO & Company Audit (1.5 hrs)": 1.5,
            "Bank Audit (3 hrs)": 3,
            "Government Audit (1 hr)": 1,
            "Cooperative Society Audit (1 hr)": 1,
            "Other Entities Audit (3 hrs)": 3,
            "Audit of Items of Financial Statements (6 hrs)": 6,
            "Internal Audit & SA 610 (1 hr)": 1
        },
        "Cost and Management Accounting": {
            "Introduction to CMA (3 hrs)": 3,
            "Material Cost (7 hrs)": 7,
            "Employee Cost (6 hrs)": 6,
            "Overheads – Absorption Costing (7.5 hrs)": 7.5,
            "Activity Based Costing (6 hrs)": 6,
            "Cost Sheet (5 hrs)": 5,
            "Cost Accounting System (6 hrs)": 6,
            "Unit and Batch Costing (3.5 hrs)": 3.5,
            "Job Costing (2.5 hrs)": 2.5,
            "Process and Operation Costing (6.5 hrs)": 6.5,
            "Joint & By Products (5 hrs)": 5,
            "Service Costing (7.5 hrs)": 7.5,
            "Standard Costing (8.5 hrs)": 8.5,
            "Marginal Costing (9 hrs)": 9,
            "Budget and Budgetary Controls (8 hrs)": 8
        },
        "FMSM": {
            "FM": {
                "Scope and Objectives of FM (1.5 hrs)": 1.5,
                "Types of Financing (2 hrs)": 2,
                "Ratio Analysis (3.5 hrs)": 3.5,
                "Cost of Capital (4 hrs)": 4,
                "Capital Structure (4 hrs)": 4,
                "Leverage (4 hrs)": 4,
                "Investment Decisions – Capital Budgeting (4 hrs)": 4,
                "Dividend Decisions (4 hrs)": 4,
                "Management of Working Capital (4 hrs)": 4
            },
            "SM": {
                "Introduction to Strategic Management (6 hrs)": 6,
                "Strategic Analysis: External Environment (6 hrs)": 6,
                "Strategic Analysis: Internal Environment (6 hrs)": 6,
                "Strategic Choices (7 hrs)": 7,
                "Strategy Implementation & Evaluation (10 hrs)": 10
            }
        }
    }
}

# ------------------ UI + Planner Logic ------------------

st.subheader("🔢 Step 1: Study Hours")
study_hours = st.number_input("How many hours can you study per day?", min_value=1, max_value=16, value=6)

st.subheader("🧠 Step 2: Select Group")
group_choice = st.radio("Which Group are you preparing for?", ["Group I", "Group II", "Both Groups"])

st.subheader("📆 Step 3: Select Revision Dates")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Revision Start Date", datetime.today())
with col2:
    end_date = st.date_input("Revision End Date", datetime.today() + timedelta(days=30))

st.subheader("📚 Step 4: Select Subjects")
if group_choice == "Group I":
    selected_data = data["Group I"]
elif group_choice == "Group II":
    selected_data = data["Group II"]
else:
    selected_data = {**data["Group I"], **data["Group II"]}

all_subjects = list(selected_data.keys())
select_all_subjects = st.checkbox("Select All Subjects")
selected_subjects = st.multiselect("Choose Subjects", all_subjects, default=all_subjects if select_all_subjects else [])

# Chapter Selection
final_chapter_dict = {}

for subject in selected_subjects:
    chapters = selected_data[subject]

    # Handle sub-categorized subjects like Income Tax or FMSM
    if any(isinstance(v, dict) for v in chapters.values()):
        combined = {}
        for k, v in chapters.items():
            if isinstance(v, dict):
                combined.update({f"{k} - {sk} ({sv} hrs)": sv for sk, sv in v.items()})
        chapters = combined
    else:
        chapters = {f"{k} ({v} hrs)": v for k, v in chapters.items()}

    st.markdown(f"**{subject}**")
    select_all = st.checkbox(f"Select All Chapters for {subject}", key=f"chk_{subject}")
    
    # ✅ Default all chapters if 'Select All' or if user hasn’t selected anything manually
    default_chaps = list(chapters.keys()) if select_all else []
    selected_chapters = st.multiselect(
        f"Select Chapters for {subject}",
        list(chapters.keys()),
        default=default_chaps,
        key=f"ch_{subject}"
    )

    # ✅ Add selected chapters to final dict
    for ch in selected_chapters:
        final_chapter_dict[ch] = chapters[ch]


# Total Study Hour Summary
if final_chapter_dict:
    total_selected_hours = sum(final_chapter_dict.values())
    available_hours = (end_date - start_date).days * study_hours
    st.info(f"Total hours selected: **{total_selected_hours} hrs** | Total available: **{available_hours} hrs**")
    if total_selected_hours > available_hours:
        st.warning("⚠️ Selected chapters need more time than available in given date range.")

# Generate Planner
if st.button("📅 Generate Study Planner"):
    if start_date >= end_date:
        st.error("End date must be after start date.")
    elif not final_chapter_dict:
        st.warning("Please select at least one chapter.")
    else:
        sorted_chapters = list(final_chapter_dict.items())
        plan = []
        idx = 0
        day = start_date
        while day <= end_date and idx < len(sorted_chapters):
            time_left = study_hours
            today = []
            while time_left > 0 and idx < len(sorted_chapters):
                ch, hrs = sorted_chapters[idx]
                if hrs <= time_left:
                    today.append(f"{ch}")
                    time_left -= hrs
                    idx += 1
                else:
                    break
            plan.append((day.strftime("%d-%b-%Y"), today))
            day += timedelta(days=1)

        # Display plan
        st.success("✅ Plan Generated!")
        for d, topics in plan:
            st.subheader(f"📆 {d}")
            if topics:
                for t in topics:
                    st.markdown(f"- {t}")
            else:
                st.write("🔸 Free Day")

       # Export to Excel
df = pd.DataFrame([
    (d, t.split(' (')[0], t.split(' (')[1].replace(' hrs)', ''))
    for d, topics in plan for t in topics
], columns=["Date", "Chapter", "Estimated Hours"])

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name="Study Plan")

buffer.seek(0)
st.download_button(
    label="📥 Download Plan as Excel",
    data=buffer,
    file_name="study_plan.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# Reset Button
if st.button("🔄 Reset Planner"):
    st.experimental_rerun()

st.markdown("---")
st.caption("Made for CA warriors ⚔️ | Plan Smart. Study Sharp. ✨")
