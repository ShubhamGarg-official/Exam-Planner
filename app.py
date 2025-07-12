# 📘 CA Exam Planner (Final Full Code)

```python
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="CA Exam Planner", layout="wide")
st.title("📘 CA Exam Planner")
st.markdown("Plan your CA exam revisions based on time and topic.")

# ------------------ Subject & Chapter Data ------------------
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
            "Branch Accounting": 16
        },
        "Corporate and Other Laws": {
            "Preliminary": 2.5,
            "Inc of Co. & Matters Incidental thereto": 5,
            "Prospectus and allotment of securities": 4,
            "Share Capital & Debentures": 5,
            "Acceptance of Deposits by Cos": 3,
            "Regitration of Charges": 2.5,
            "Mgmt & Adminstration": 7,
            "Declaration and Payment of Dividend": 3,
            "Accounts of Companies": 6,
            "Audit & Auditors": 5,
            "Cos Incorporated outside India": 2,
            "The LLP Act, 2008": 4,
            "The FEMA, 1999": 3.5,
            "The GCA, 1897": 3.5,
            "Interpretation of Statutes": 3.5
        },
        "Taxation": {
            "Income Tax": {
                "Basic Concepts": 2,
                "Residence & Scope of Total Income": 2,
                "Income from Salary": 4,
                "Income from House Property": 2,
                "PGBP": 8,
                "Capital Gain": 8,
                "IFOS": 4,
                "Income of other persons included in Assessee's Total Income": 2,
                "Set off and Carry forward losses": 2,
                "Deduction from GTI": 6,
                "Adv Tax, TDS and TCS": 5,
                "Prov for filing return of Income and Self Assessment": 2,
                "Income Tax Liability Computation and Optimisation": 10
            },
            "GST": {
                "Introduction and Constitution": 0.42,
                "Definitions": 0.58,
                "Chargeability and Goods & Services": 0.67,
                "Supply": 1,
                "Place of supply": 1,
                "Taxable Person": 0.75,
                "Exemption": 3,
                "Valuation": 0.75,
                "Reverse Charge Mechanism": 2,
                "Invoice": 0.67,
                "Time of Supply": 0.5,
                "Registration": 1,
                "Input Tax Credit": 2,
                "Manner of Payment": 0.5,
                "TDS, TCS": 0.75,
                "Filing of Return": 0.5,
                "Accounts and Records": 0.5,
                "E-Way Bill": 0.5
            }
        }
    },
    "Group II": {
        "Auditing and Ethics": {
            "Nature, Objectives & Scope of Audit": 4.5,
            "Audit Strategy, Planning & Programme": 2,
            "Audit Documentation": 1,
            "Risk Assessment & Internal Control": 3,
            "Audit Procedures": 1,
            "SA 320 / 450 / 530": 3.5,
            "Automated Environment": 1.5,
            "SA 500 / 501 / 505 / 510": 3.5,
            "SA 550 / 560 / 570 / 580": 3,
            "Communication with Mgmt & TCWG (SA 260 / 265)": 1,
            "Analytical Procedures": 1,
            "Audit Report (SA 700 / 701 / 705 / 706 / 710), Branch Audit & SA 600, SA 299": 5,
            "CARO & Company Audit": 1.5,
            "Bank Audit": 3,
            "Government Audit": 1,
            "Cooperative Society Audit": 1,
            "Other Entities Audit": 3,
            "Audit of Items of Financial Statements": 6,
            "Internal Audit & SA 610": 1
        },
        "Cost and Management Accounting": {
            "Intro to CMA": 3,
            "Material Cost": 7,
            "Employee Cost": 6,
            "Overheads-Absorption Costing Method": 7.5,
            "Activity Based Costing": 6,
            "Cost Sheet": 5,
            "Cost Accounting System": 6,
            "Unit and Batch Costing": 3.5,
            "Job Costing": 2.5,
            "Process and Operation Costing": 6.5,
            "Joint & By Products": 5,
            "Service Costing": 7.5,
            "Standard Costing": 8.5,
            "Marginal Costing": 9,
            "Budget and Budgetary Controls": 8
        },
        "FMSM": {
            "Financial Management": {
                "Scope and Objectives of FM": 1.5,
                "Types of Financing": 2,
                "Ratio Analysis": 3.5,
                "Cost of Capital": 4,
                "Capital Structure": 4,
                "Leverage": 4,
                "Investment Decisions- Capital Budgeting": 4,
                "Dividend Decisions": 4,
                "Management of Working Capital": 4
            },
            "Strategic Management": {
                "Introduction to Strategic Management": 6,
                "Strategic Analysis: External Environment": 6,
                "Strategic Analysis: Internal Environment": 6,
                "Strategic Choices": 7,
                "Strategy Implementation & Evaluation": 10
            }
        }
    }
}

# ------------------ Helper Function ------------------
def generate_plan(chapters, hours_per_day, start_date, end_date):
    plan = []
    current_day = start_date
    idx = 0
    while current_day <= end_date and idx < len(chapters):
        available = hours_per_day
        today = []
        while available > 0 and idx < len(chapters):
            title, hr = chapters[idx]
            if hr <= available:
                today.append((title, hr))
                available -= hr
                idx += 1
            else:
                break
        plan.append((current_day.strftime("%d-%b-%Y"), today))
        current_day += timedelta(days=1)
    return plan

# ------------------ UI Flow ------------------
study_hours = st.number_input("🕒 How many hours can you study per day?", min_value=1, max_value=16, value=6)
group_choice = st.radio("🧠 Which Group are you preparing for?", ["Group I", "Group II", "Both Groups"])
col1, col2 = st.columns(2)
start_date = col1.date_input("📅 Revision Start Date", datetime.today())
end_date = col2.date_input("🗓️ Revision End Date", datetime.today() + timedelta(days=30))

# Select Subjects
if group_choice == "Group I":
    subject_data = data["Group I"]
elif group_choice == "Group II":
    subject_data = data["Group II"]
else:
    subject_data = {**data["Group I"], **data["Group II"]}

all_subjects = list(subject_data.keys())
select_all_subs = st.checkbox("📚 Select All Subjects")
selected_subjects = st.multiselect("Choose Subjects", all_subjects, default=all_subjects if select_all_subs else [])

# Select Chapters
final_chapters = {}
for subject in selected_subjects:
    chapters = subject_data[subject]
    if any(isinstance(v, dict) for v in chapters.values()):  # nested like IT/GST
        for subcat, subchap in chapters.items():
            for ch, hrs in subchap.items():
                final_chapters[f"{subject} - {subcat} - {ch}"] = hrs
    else:
        for ch, hrs in chapters.items():
            final_chapters[f"{subject} - {ch}"] = hrs

# Select which chapters to include
chapter_list = list(final_chapters.keys())
select_all_chaps = st.checkbox("Select All Chapters")
selected_chaps = st.multiselect("📄 Choose Chapters", chapter_list, default=chapter_list if select_all_chaps else [])
selected_hours = sum([final_chapters[ch] for ch in selected_chaps])
available_hours = (end_date - start_date).days * study_hours

st.markdown(f"🧮 **Total Selected Hours:** {selected_hours} | **Total Available Hours:** {available_hours}")

if st.button("✅ Generate Planner"):
    if selected_hours > available_hours:
        st.error("Selected chapter hours exceed available revision time.")
    elif not selected_chaps:
        st.warning("Please select chapters to continue.")
    else:
        plan = generate_plan([(ch, final_chapters[ch]) for ch in selected_chaps], study_hours, start_date, end_date)
        st.success("✅ Planner Ready!")
        for day, items in plan:
            st.subheader(f"📆 {day}")
            if items:
                for ch, hr in items:
                    st.markdown(f"- {ch} ({hr} hrs)")
            else:
                st.write("🔸 Free / Buffer Day")

        # Export to Excel
        df = pd.DataFrame([{"Date": d, "Chapter": ch, "Estimated Hours": hr} for d, chs in plan for ch, hr in chs])
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Study Plan')
            writer.close()
        st.download_button("📥 Export as Excel", data=buffer.getvalue(), file_name="CA_Exam_Plan.xlsx")

        # Export to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="CA Exam Planner", ln=True, align='C')
        for day, topics in plan:
            pdf.ln()
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt=day, ln=True)
            pdf.set_font("Arial", size=11)
            if topics:
                for ch, hr in topics:
                    pdf.cell(200, 10, txt=f"- {ch} ({hr} hrs)", ln=True)
            else:
                pdf.cell(200, 10, txt="🔸 Free / Buffer Day", ln=True)
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        st.download_button("📄 Export as PDF", data=pdf_buffer.getvalue(), file_name="CA_Exam_Plan.pdf")
        
