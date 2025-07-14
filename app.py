import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import io
from fpdf import FPDF

# Your ca_exam_data.py content goes here, updated with importance lists
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
        "Advance Accounting_High_Importance": [
            "Branch Accounting",
            "Internal Reconstruction",
            "AS-14: Amalgamation of Companies",
            "AS-3: Cash Flow Statements",
            "AS-13: Investments",
            "Buy Back of Shares",
            "Company Final Accounts",
            "AS-4: Contingencies & Events after Balance Sheet Date",
            "AS-5: Net Profits",
            "AS-10: Property, Plant and Equipment",
            "AS-11: Effects of Changes in Foreign Exchange Rates",
            "AS-16: Borrowing Costs",
            "AS-18: Related Party Disclosures",
            "AS-25: Interim Financial Reporting"
        ],
        "Advance Accounting_Medium_Importance": [
            "AS-21: Consolidated Financial Statements",
            "AS-22: Accounting for Taxes on Income",
            "AS-15: Retirement Benefits",
            "AS-19: Leases",
            "AS-20: Earnings Per Share",
            "AS-26: Intangible Assets",
            "AS-28: Impairment of Assets",
            "Schedule III"
        ],
        "Advance Accounting_Least_Importance": [
            "AS-23: Accounting for Investments in Associates",
            "AS-27: Joint Ventures",
            "AS-1: Accounting Policies",
            "AS-2: Valuation of Inventories",
            "AS-7: Construction Contracts",
            "AS-9: Revenue Recognition",
            "AS-12: Government Grants",
            "AS-17: Segment Reporting",
            "AS-24: Discontinuing Operations",
            "AS-29: Provisions, Contingent Liabilities & Contingent Assets"
        ],
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
        "Corporate and Other Laws_High_Importance": [
            "Share Capital & Debentures",
            "Mgmt & Adminstration",
            "Accounts of Companies",
            "Audit & Auditors"
        ],
        "Corporate and Other Laws_Medium_Importance": [],
        "Corporate and Other Laws_Least_Importance": [],
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
            "Income Tax_High_Importance": [
                "PGBP",
                "Capital Gain",
                "Deduction from GTI",
                "Income Tax Liability Computation and Optimisation"
            ],
            "Income Tax_Medium_Importance": [],
            "Income Tax_Least_Importance": [],
            "GST": {
                "Introduction and Constitution": 0.5,
                "Definitions": 0.5,
                "Chargeability and Goods & Services": 0.75,
                "Supply": 1,
                "Place of supply": 1,
                "Taxable Person": 0.75,
                "Exemption": 3,
                "Valuation": 0.75,
                "Reverse Charge Mechanism": 2,
                "Invoice": 0.75,
                "Time of Supply": 0.5,
                "Registration": 1,
                "Input Tax Credit": 2,
                "Manner of Payment": 0.5,
                "TDS, TCS": 0.75,
                "Filing of Return": 0.5,
                "Accounts and Records": 0.5,
                "E-Way Bill": 0.5
            },
            "GST_High_Importance": [
                "Taxable Person",
                "Registration",
                "Supply",
                "Input Tax Credit",
                "Reverse Charge Mechanism",
                "Exemption",
                "Place of supply",
                "Time of Supply",
                "Valuation"
            ],
            "GST_Medium_Importance": [
                "E-Way Bill",
                "TDS, TCS",
                "Invoice",
                "Manner of Payment"
            ],
            "GST_Least_Importance": [
                "Introduction and Constitution",
                "Definitions",
                "Chargeability and Goods & Services",
                "Filing of Return",
                "Accounts and Records"
            ]
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
        "Auditing and Ethics_High_Importance": [
            "Audit Report (SA 700 / 701 / 705 / 706 / 710), Branch Audit & SA 600, SA 299",
            "Bank Audit",
            "Audit of Items of Financial Statements"
        ],
        "Auditing and Ethics_Medium_Importance": [], # Add your lists here if applicable
        "Auditing and Ethics_Least_Importance": [], # Add your lists here if applicable
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
        "Cost and Management Accounting_High_Importance": [
            "Material Cost",
            "Activity Based Costing",
            "Process and Operation Costing",
            "Standard Costing",
            "Marginal Costing",
            "Budget and Budgetary Controls"
        ],
        "Cost and Management Accounting_Medium_Importance": [], # Add your lists here if applicable
        "Cost and Management Accounting_Least_Importance": [], # Add your lists here if applicable
        "FMSM": {
            "FM": {
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
            "FM_High_Importance": [
                "Ratio Analysis",
                "Cost of Capital",
                "Capital Structure",
                "Leverage",
                "Investment Decisions- Capital Budgeting",
                "Management of Working Capital"
            ],
            "FM_Medium_Importance": [],
            "FM_Least_Importance": [],
            "SM": {
                "Introduction to Strategic Management": 6,
                "Strategic Analysis: External Environment": 6,
                "Strategic Analysis: Internal Environment": 6,
                "Strategic Choices": 7,
                "Strategy Implementation & Evaluation": 10
            },
            "SM_High_Importance": [
                "Strategic Choices",
                "Strategy Implementation & Evaluation"
            ],
            "SM_Medium_Importance": [],
            "SM_Least_Importance": []
        }
    }
}


# ---------------------------- Streamlit Page Setup ----------------------------
st.set_page_config(page_title="CA Exam Planner", layout="wide")
st.title("📘 CA Exam Planner")
st.markdown("Plan your CA exam revisions based on your time and topic preferences.")

# ---------------------------- Study Hours Per Day ----------------------------
study_hours = st.number_input("🕒 How many hours can you study per day?", min_value=1, max_value=16, value=6)

# ---------------------------- Group Selection ----------------------------
group_choice = st.radio("🧠 Which Group are you preparing for?", ["Group I", "Group II", "Both Groups"])

if group_choice == "Group I":
    selected_data = data["Group I"]
elif group_choice == "Group II":
    selected_data = data["Group II"]
else:
    selected_data = {**data["Group I"], **data["Group II"]}

# ---------------------------- Date Range Inputs ----------------------------
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 Revision Start Date", datetime.today())
with col2:
    end_date = st.date_input("🗓️ Revision End Date", datetime.today() + timedelta(days=30))

# ---------------------------- Subject and Chapter Selection ----------------------------
# Filter out the importance lists keys when displaying subjects for selection
all_subjects = [s for s in list(selected_data.keys()) if not s.endswith(('_High_Importance', '_Medium_Importance', '_Least_Importance'))]
select_all_subjects = st.checkbox("📚 Select All Subjects")
selected_subjects = st.multiselect("Choose Subjects", all_subjects, default=all_subjects if select_all_subjects else [])

final_chapter_dict = {} # Stores all selected chapters and their original hours
# These lists will temporarily hold selected chapters, categorized by their importance level
selected_high_importance_chapters = []
selected_medium_importance_chapters = []
selected_least_importance_chapters = []
selected_other_chapters = [] # For chapters not explicitly in any importance list

for subject in selected_subjects:
    chapters_in_subject = selected_data[subject]
    flat_chapters = {}

    # Get importance lists for the current subject (or sub-subject for nested structures)
    # Using .get() with an empty list as default to avoid KeyError if no importance list exists
    subject_high_imp_list = selected_data.get(f"{subject}_High_Importance", [])
    subject_medium_imp_list = selected_data.get(f"{subject}_Medium_Importance", [])
    subject_least_imp_list = selected_data.get(f"{subject}_Least_Importance", [])

    if any(isinstance(val, dict) for val in chapters_in_subject.values()):
        # Handle nested subjects (like "Taxation" -> "Income Tax" / "GST")
        for subtopic, subchaps in chapters_in_subject.items():
            if isinstance(subchaps, dict): # Check if it's a sub-subject dictionary
                # Get importance lists specific to the sub-subject
                subtopic_high_imp_list = selected_data.get(f"{subtopic}_High_Importance", [])
                subtopic_medium_imp_list = selected_data.get(f"{subtopic}_Medium_Importance", [])
                subtopic_least_imp_list = selected_data.get(f"{subtopic}_Least_Importance", [])

                for ch, hr in subchaps.items():
                    key = f"{subject} - {subtopic} - {ch}"
                    flat_chapters[key] = hr
                    # Categorize *all* chapters for potential prioritization later
                    if ch in subtopic_high_imp_list:
                        selected_high_importance_chapters.append((key, hr))
                    elif ch in subtopic_medium_imp_list:
                        selected_medium_importance_chapters.append((key, hr))
                    elif ch in subtopic_least_imp_list:
                        selected_least_importance_chapters.append((key, hr))
                    else:
                        selected_other_chapters.append((key, hr))
            else: # This path might not be taken given the current structure of your 'data'
                # but it's here for robustness if a subject directly contains a chapter (not a sub-subject)
                key = f"{subject} - {subtopic}" # Here subtopic is actually chapter name
                flat_chapters[key] = subchaps # Here subchaps is hours
                if subtopic in subject_high_imp_list:
                    selected_high_importance_chapters.append((key, subchaps))
                elif subtopic in subject_medium_imp_list:
                    selected_medium_importance_chapters.append((key, subchaps))
                elif subtopic in subject_least_imp_list:
                    selected_least_importance_chapters.append((key, subchaps))
                else:
                    selected_other_chapters.append((key, subchaps))
    else:
        # Handle direct chapters (like "Advance Accounting" or "Corporate and Other Laws")
        for ch, hr in chapters_in_subject.items():
            key = f"{subject} - {ch}"
            flat_chapters[key] = hr
            # Categorize *all* chapters for potential prioritization later
            if ch in subject_high_imp_list:
                selected_high_importance_chapters.append((key, hr))
            elif ch in subject_medium_imp_list:
                selected_medium_importance_chapters.append((key, hr))
            elif ch in subject_least_imp_list:
                selected_least_importance_chapters.append((key, hr))
            else:
                selected_other_chapters.append((key, hr))

    chapter_names = list(flat_chapters.keys())
    select_all = st.checkbox(f"Select all chapters for {subject}", key=f"select_all_{subject}")
    selected_chapters_for_subject = st.multiselect(f"📄 Chapters from {subject}", chapter_names, default=chapter_names if select_all else [], key=f"multiselect_{subject}")

    # Populate final_chapter_dict only with chapters ACTUALLY selected by the user
    for ch_key in selected_chapters_for_subject:
        final_chapter_dict[ch_key] = flat_chapters[ch_key]

# Filter the previously categorized importance lists to only include chapters that the user *actually selected*
# This prevents scheduling chapters that were marked important but not chosen by the user
# And ensures no duplicates across priority lists
seen_chapters = set()

filtered_high_importance = []
for ch, hr in selected_high_importance_chapters:
    if ch in final_chapter_dict and ch not in seen_chapters:
        filtered_high_importance.append((ch, hr))
        seen_chapters.add(ch)

filtered_medium_importance = []
for ch, hr in selected_medium_importance_chapters:
    if ch in final_chapter_dict and ch not in seen_chapters:
        filtered_medium_importance.append((ch, hr))
        seen_chapters.add(ch)

filtered_least_importance = []
for ch, hr in selected_least_importance_chapters:
    if ch in final_chapter_dict and ch not in seen_chapters:
        filtered_least_importance.append((ch, hr))
        seen_chapters.add(ch)

filtered_other_chapters = []
for ch, hr in selected_other_chapters:
    if ch in final_chapter_dict and ch not in seen_chapters:
        filtered_other_chapters.append((ch, hr))
        seen_chapters.add(ch)

# Combine all chapters, ordered by priority (High -> Medium -> Least -> Other)
# Within each priority level, sort by hours (descending) as a secondary sorting criterion
prioritized_chapters_list = sorted(filtered_high_importance, key=lambda x: x[1], reverse=True) + \
                           sorted(filtered_medium_importance, key=lambda x: x[1], reverse=True) + \
                           sorted(filtered_least_importance, key=lambda x: x[1], reverse=True) + \
                           sorted(filtered_other_chapters, key=lambda x: x[1], reverse=True)

# Create an OrderedDict or just use this list directly for plan generation.
# For generate_plan to work sequentially, a list of tuples is more direct.
# The previous `final_chapter_dict_prioritized` was a dictionary, but now
# the `prioritized_chapters_list` will directly control the order.


# ---------------------------- Display Totals ----------------------------
# Calculate total selected hours from the user's actual selections (final_chapter_dict)
total_selected_hours = sum(final_chapter_dict.values())
total_days = (end_date - start_date).days + 1
total_available_hours = total_days * study_hours

st.markdown(f"### 🧮 Total Selected Hours: `{total_selected_hours}` | Total Available Hours: `{total_available_hours}`")

# ---------------------------- Generate Plan ----------------------------
# The generate_plan function now takes the pre-prioritized list of chapters
def generate_plan(chapters_to_schedule_list, hours_per_day, start_date, end_date):
    plan = []
    current_day = start_date
    
    idx = 0

    while current_day <= end_date:
        available_time = hours_per_day
        today_topics = []
        
        while available_time > 0 and idx < len(chapters_to_schedule_list):
            chapter_name, ch_time = chapters_to_schedule_list[idx]

            if ch_time <= available_time:
                # Chapter fits entirely
                today_topics.append((chapter_name, ch_time))
                available_time -= ch_time
                idx += 1
            else:
                # Chapter needs to be split
                today_topics.append((f"{chapter_name} (Part)", available_time))
                # Update the remaining time for the current chapter in the list
                chapters_to_schedule_list[idx] = (chapter_name, ch_time - available_time)
                available_time = 0 # No more time left for today

        plan.append((current_day.strftime("%d-%b-%Y"), today_topics))
        current_day += timedelta(days=1)
    
    # Handle any remaining chapters if end_date is reached but not all chapters are covered
    if idx < len(chapters_to_schedule_list):
        remaining_hours_uncovered = sum(t for _, t in chapters_to_schedule_list[idx:])
        st.warning(f"Note: Not all selected chapters could be scheduled within the given date range. Remaining hours: {remaining_hours_uncovered:.2f}")

    return plan


# ---------------------------- Planner Display ----------------------------
if st.button("✅ Generate Study Plan"):
    if start_date >= end_date:
        st.error("❌ End date must be after start date.")
    elif not prioritized_chapters_list: # Check if the prioritized list is empty
        st.warning("⚠️ Please select at least one chapter.")
    elif total_selected_hours > total_available_hours:
        st.warning("⚠️ Selected content exceeds available time. Please reduce selection or increase study hours/date range.")
    else:
        # Pass the pre-prioritized list to the generate_plan function
        plan = generate_plan(prioritized_chapters_list, study_hours, start_date, end_date)

        st.success("✅ Study Planner Generated!")
        export_data = []
        for day, topics in plan:
            st.subheader(f"📆 {day}")
            if topics:
                for topic, hr in topics:
                    st.markdown(f"- {topic} ({hr} hrs)")
                    export_data.append({"Date": day, "Plan": f"{topic} ({hr} hrs)"})
            else:
                st.write("🔸 Free / Buffer Day")
                export_data.append({"Date": day, "Plan": "Free / Buffer Day"})

        df_export = pd.DataFrame(export_data)

        # Remove "Free / Buffer Day" rows for export clarity
        df_export = df_export[df_export["Plan"] != "Free / Buffer Day"]

        # Extract topic and hours
        # This regex handles cases like "Subject - Subtopic - Chapter (Part)" or "Subject - Chapter (Part)"
        df_export[["FullTopic", "Estimated Hours"]] = df_export["Plan"].str.extract(r'(.*)\((\d+(?:\.\d+)?) hrs\)')
        
        # Further refine 'Topic' to just the chapter name, removing subject/subtopic prefixes
        def extract_chapter_name(full_topic):
            parts = full_topic.split(' - ')
            if len(parts) > 1:
                return parts[-1].replace(" (Part)", "").strip() # Also remove "(Part)"
            return full_topic.replace(" (Part)", "").strip()

        df_export["Topic"] = df_export["FullTopic"].apply(extract_chapter_name)
        df_export = df_export[["Date", "Topic", "Estimated Hours"]]
        df_export["Estimated Hours"] = pd.to_numeric(df_export["Estimated Hours"])


        # ---------------------------- Export to Excel ----------------------------
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Planner')
        st.download_button("📥 Download as Excel", data=buffer.getvalue(), file_name="study_plan.xlsx")

        # ---------------------------- Export to PDF ----------------------------
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "CA Exam Planner", 0, 1, "C")
                self.ln(5)

            def chapter_title(self, title):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, title, ln=True)

            def chapter_body(self, lines):
                self.set_font("Arial", "", 11)
                for line in lines:
                    # Use multi_cell for automatic line breaks if content is too long
                    self.multi_cell(0, 8, f"- {line}")
                self.ln(3)

        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, f"Study Hours per Day: {study_hours}")
        pdf.multi_cell(0, 8, f"Revision Period: {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}")
        pdf.multi_cell(0, 8, f"Total Selected Hours: {total_selected_hours} | Total Available Hours: {total_available_hours}")
        pdf.ln(5)

        for day, topics in plan:
            pdf.chapter_title(day)
            if topics:
                lines = [f"{topic} ({hr} hrs)" for topic, hr in topics]
            else:
                lines = ["Free / Buffer Day"]
            pdf.chapter_body(lines)

        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_output,
            file_name="study_plan.pdf",
            mime="application/pdf"
        )
