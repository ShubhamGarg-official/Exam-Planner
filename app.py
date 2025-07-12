import streamlit as st
from datetime import datetime, timedelta
import math

st.set_page_config(page_title="CA Exam Planner", layout="wide")

# ------------------------------ Data ------------------------------

data = {
    "Group I": {
        "Advance Accounting": {
            "AS-1: Accounting Policies": 1,
            "AS-2: Valuation of Inventories": 4,
            "AS-3: Cash Flow Statements": 8,
            "AS-4: Contingencies & Events after Balance Sheet Date": 2,
            "AS-5: Net Profits": 2,
            "AS-7: Construction Contracts": 4,
            "AS-9: Revenue Recognition": 1,
            "AS-10: Property, Plant and Equipment": 3,
            "AS-11: Effects of Changes in Foreign Exchange Rates": 4,
            "AS-12: Government Grants": 3,
            "AS-13: Investments": 6,
            "AS-14: Amalgamation of Companies": 14,
            "AS-15: Retirement Benefits": 2,
            "AS-16: Borrowing Costs": 6,
            "AS-17: Segment Reporting": 2,
            "AS-18: Related Party Disclosures": 2,
            "AS-19: Leases": 6,
            "AS-20: Earnings Per Share": 4,
            "AS-21: Consolidated Financial Statements": 12,
            "AS-22: Accounting for Taxes on Income": 3,
            "AS-23: Accounting for Investments in Associates": 2,
            "AS-24: Discontinuing Operations": 2,
            "AS-25: Interim Financial Reporting": 2,
            "AS-26: Intangible Assets": 3,
            "AS-27: Joint Ventures": 2,
            "AS-28: Impairment of Assets": 2,
            "AS-29: Provisions, Contingent Liabilities & Contingent Assets": 2,
            "Schedule III": 2,
            "Company Final Accounts": 12,
            "Buy Back of Shares": 4,
            "Internal Reconstruction": 8,
            "Branch Accounting": 16,
        },
        "Corporate and Other Laws": {
            # Companies Act
            "Preliminary": 2.5,
            "Incorporation of Company & Matters Incidental thereto": 5,
            "Prospectus and Allotment of Securities": 4,
            "Share Capital & Debentures": 5,
            "Acceptance of Deposits by Companies": 3,
            "Registration of Charges": 2.5,
            "Management & Administration": 7,
            "Declaration and Payment of Dividend": 3,
            "Accounts of Companies": 6,
            "Audit & Auditors": 5,
            "Companies Incorporated Outside India": 2,
            # Other Laws
            "The LLP Act, 2008": 4,
            "The FEMA, 1999": 3.5,
            "The General Clauses Act, 1897": 3.5,
            "Interpretation of Statutes": 3.5,
        },
        "Taxation": {
            "Income Tax": {
                "Basic Concepts": 2,
                "Residence & Scope of Total Income": 2,
                "Income from Salary": 4,
                "Income from House Property": 2,
                "Profits and Gains of Business or Profession (PGBP)": 8,
                "Capital Gain": 8,
                "Income from Other Sources (IFOS)": 4,
                "Income of other persons included in Assessee's Total Income": 2,
                "Set-off and Carry Forward of Losses": 2,
                "Deductions from Gross Total Income": 6,
                "Advance Tax, TDS and TCS": 5,
                "Provisions for Filing Return of Income and Self-Assessment": 2,
                "Income Tax Liability Computation and Optimisation": 10,
            },
            "GST": {
                "Introduction and Constitution": 1,
                "Definitions": 1,
                "Chargeability and Goods & Services": 1,
                "Supply": 1,
                "Place of Supply": 1,
                "Taxable Person": 1,
                "Exemption": 3,
                "Valuation": 1,
                "Reverse Charge Mechanism": 2,
                "Invoice": 1,
                "Time of Supply": 1,
                "Registration": 1,
                "Input Tax Credit": 2,
                "Manner of Payment": 1,
                "TDS, TCS": 1,
                "Filing of Return": 1,
                "Accounts and Records": 1,
                "E-Way Bill": 1,
            }
        }
    },
    "Group II": {
        "Cost and Management Accounting": {
            "Introduction to CMA": 3,
            "Material Cost": 7,
            "Employee Cost": 6,
            "Overheads – Absorption Costing Method": 7.5,
            "Activity-Based Costing": 6,
            "Cost Sheet": 5,
            "Cost Accounting System": 6,
            "Unit and Batch Costing": 3.5,
            "Job Costing": 2.5,
            "Process and Operation Costing": 6.5,
            "Joint & By-Products": 5,
            "Service Costing": 7.5,
            "Standard Costing": 8.5,
            "Marginal Costing": 9,
            "Budget and Budgetary Controls": 8,
        },
        "FMSM": {
            "FM": {
                "Scope and Objectives of FM": 1.5,
                "Types of Financing": 2,
                "Ratio Analysis": 3.5,
                "Cost of Capital": 4,
                "Capital Structure": 4,
                "Leverage": 4,
                "Investment Decisions – Capital Budgeting": 4,
                "Dividend Decisions": 4,
                "Management of Working Capital": 4,
            },
            "SM": {
                "Introduction to Strategic Management": 6,
                "Strategic Analysis: External Environment": 6,
                "Strategic Analysis: Internal Environment": 6,
                "Strategic Choices": 7,
                "Strategy Implementation & Evaluation": 10,
            }
        }
    }
}

# ------------------------------ UI ------------------------------

st.title("📘 CA Exam Planner – Time-Based Study Schedule")

group_choice = st.selectbox("Select Group:", ["Group I", "Group II", "Both Groups"])

if group_choice == "Both Groups":
    selected_data = {**data["Group I"], **data["Group II"]}
elif group_choice == "Group I":
    selected_data = data["Group I"]
else:
    selected_data = data["Group II"]

# Subject selection
selected_subjects = st.multiselect("Select Subjects:", list(selected_data.keys()))

custom_chapters = {}
for subject in selected_subjects:
    sub_data = selected_data[subject]
    if isinstance(sub_data, dict) and all(isinstance(v, dict) for v in sub_data.values()):
        # Nested (e.g., Taxation)
        st.subheader(subject)
        for subpart, chapters in sub_data.items():
            selected = st.multiselect(f"Select chapters from {subpart}:", list(chapters.keys()))
            for ch in selected:
                custom_chapters[f"{ch} ({subpart})"] = chapters[ch]
    else:
        selected = st.multiselect(f"Select chapters from {subject}:", list(sub_data.keys()))
        for ch in selected:
            custom_chapters[ch] = sub_data[ch]

study_hours_per_day = st.slider("How many hours can you study per day?", 1, 16, 6)

rev_start = st.date_input("Revision Start Date")
rev_end = st.date_input("Revision End Date")
exam_start = st.date_input("Exam Start Date")

if st.button("Generate Study Plan"):
    if rev_end >= exam_start:
        st.error("⚠️ Revision End Date must be before Exam Start Date.")
    elif rev_start >= rev_end:
        st.error("⚠️ Revision Start Date must be before Revision End Date.")
    else:
        available_days = (rev_end - rev_start).days + 1
        total_hours = sum(custom_chapters.values())
        daily_plan = {}
        current_day = rev_start
        chapter_list = list(custom_chapters.items())

        idx = 0
        while current_day <= rev_end and idx < len(chapter_list):
            hours_left = study_hours_per_day
            daily_plan[current_day.strftime("%d-%b")] = []
            while hours_left > 0 and idx < len(chapter_list):
                chapter, time = chapter_list[idx]
                if time <= hours_left:
                    daily_plan[current_day.strftime("%d-%b")].append(f"{chapter} ({time} hrs)")
                    hours_left -= time
                    idx += 1
                else:
                    break
            current_day += timedelta(days=1)

        st.success("📅 Study Plan Generated:")
        for day, tasks in daily_plan.items():
            st.write(f"**{day}:**")
            for task in tasks:
                st.markdown(f"- {task}")
            st.markdown("---")

