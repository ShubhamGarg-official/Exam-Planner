import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import io
from fpdf import FPDF
from collections import defaultdict, deque

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
        "Taxation": { # This is a meta-subject containing sub-subjects
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
        "Auditing and Ethics_Medium_Importance": [],
        "Auditing and Ethics_Least_Importance": [],
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
        "Cost and Management Accounting_Medium_Importance": [],
        "Cost and Management Accounting_Least_Importance": [],
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

# ---------------------------- User Inputs ----------------------------
study_hours = st.number_input("🕒 How many hours can you study per day?", min_value=1, max_value=16, value=6)
max_subjects_per_day = st.selectbox(
    "🔢 Max number of subjects per day:",
    [1, 2, 3, 4], # Added more options for flexibility
    index=0 # Default to 1 subject per day
)

group_choice = st.radio("🧠 Which Group are you preparing for?", ["Group I", "Group II", "Both Groups"])

if group_choice == "Group I":
    selected_data = data["Group I"]
elif group_choice == "Group II":
    selected_data = data["Group II"]
else:
    # Merge both groups, ensuring keys are distinct if there are overlaps (though unlikely with subject names)
    selected_data = {**data["Group I"], **data["Group II"]}

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 Revision Start Date", datetime.today())
with col2:
    end_date = st.date_input("🗓️ Revision End Date", datetime.today() + timedelta(days=30))


# Function to get importance lists from subject data
def get_importance_lists(subject_data_dict, subject_name):
    high = subject_data_dict.get(f"{subject_name}_High_Importance", [])
    medium = subject_data_dict.get(f"{subject_name}_Medium_Importance", [])
    least = subject_data_dict.get(f"{subject_name}_Least_Importance", [])
    return high, medium, least

# Collect all possible subjects for multiselect, excluding importance lists
all_subjects_for_selection = [s for s in list(selected_data.keys()) if not s.endswith(('_High_Importance', '_Medium_Importance', '_Least_Importance'))]
select_all_subjects = st.checkbox("📚 Select All Subjects")
selected_subjects = st.multiselect("Choose Subjects", all_subjects_for_selection, default=all_subjects_for_selection if select_all_subjects else [])

# Allow user to specify the order of selected subjects
if selected_subjects:
    st.markdown("---")
    st.subheader("Subject Revision Order")
    st.info("Drag and drop to arrange the order in which you want to study subjects. This will primarily dictate the sequence of subjects in your plan.")
    
    # Create a list of (subject_name, order_index) for reordering
    # Use selected_subjects directly for ordering if they are already selected
    ordered_subjects = st.multiselect(
        "Set your preferred subject order:",
        options=selected_subjects,
        default=selected_subjects, # Default to the order they were selected in or alphabetical
        key="subject_order_multiselect"
    )
else:
    ordered_subjects = []

# Stores all selected chapters with their original hours, full path, and subject name
# Will be populated with (full_chapter_key, hours, priority_level_int, main_subject_name)
all_selected_chapters_with_meta = [] 

# Iterate through selected subjects to get their chapters and assign importance
for main_subject in selected_subjects:
    chapters_in_main_subject = selected_data[main_subject]

    # Handle subjects that contain sub-subjects (like Taxation, FMSM)
    if any(isinstance(val, dict) for val in chapters_in_main_subject.values()):
        st.subheader(f"Chapters for {main_subject}")
        for sub_subject, sub_chapters_or_lists in chapters_in_main_subject.items():
            if isinstance(sub_chapters_or_lists, dict): # It's a sub-subject (e.g., Income Tax, GST, FM, SM)
                chapter_names_in_sub = list(sub_chapters_or_lists.keys())
                full_keys_for_multiselect_sub = [f"{main_subject} - {sub_subject} - {ch}" for ch in chapter_names_in_sub]
                
                select_all_sub = st.checkbox(f"Select all chapters for {sub_subject}", key=f"select_all_{main_subject}_{sub_subject}")
                selected_chapters_from_sub = st.multiselect(
                    f"📄 Chapters from {main_subject} - {sub_subject}",
                    full_keys_for_multiselect_sub,
                    default=full_keys_for_multiselect_sub if select_all_sub else [],
                    key=f"multiselect_{main_subject}_{sub_subject}"
                )
                
                high_imp_list, medium_imp_list, least_imp_list = get_importance_lists(chapters_in_main_subject, sub_subject)

                for full_ch_key in selected_chapters_from_sub:
                    original_chapter_name = full_ch_key.split(' - ')[-1]
                    hours = sub_chapters_or_lists[original_chapter_name]
                    
                    priority_int = 3 # Default to 'Other'
                    if original_chapter_name in high_imp_list:
                        priority_int = 0
                    elif original_chapter_name in medium_imp_list:
                        priority_int = 1
                    elif original_chapter_name in least_imp_list:
                        priority_int = 2
                    
                    all_selected_chapters_with_meta.append((full_ch_key, hours, priority_int, main_subject)) 

    else: # Direct subjects (e.g., Advance Accounting, Corporate and Other Laws, Auditing, Costing)
        chapter_names_in_main = list(chapters_in_main_subject.keys())
        full_keys_for_multiselect_main = [f"{main_subject} - {ch}" for ch in chapter_names_in_main]

        st.subheader(f"Chapters for {main_subject}")
        select_all_main = st.checkbox(f"Select all chapters for {main_subject}", key=f"select_all_{main_subject}")
        selected_chapters_from_main = st.multiselect(
            f"📄 Chapters from {main_subject}",
            full_keys_for_multiselect_main,
            default=full_keys_for_multiselect_main if select_all_main else [],
            key=f"multiselect_{main_subject}"
        )

        high_imp_list, medium_imp_list, least_imp_list = get_importance_lists(selected_data, main_subject)

        for full_ch_key in selected_chapters_from_main:
            original_chapter_name = full_ch_key.split(' - ')[-1]
            hours = chapters_in_main_subject[original_chapter_name]

            priority_int = 3
            if original_chapter_name in high_imp_list:
                priority_int = 0
            elif original_chapter_name in medium_imp_list:
                priority_int = 1
            elif original_chapter_name in least_imp_list:
                priority_int = 2
            
            all_selected_chapters_with_meta.append((full_ch_key, hours, priority_int, main_subject)) 


# Organize chapters by subject and then sort within each subject
chapters_by_subject = defaultdict(list)
for ch_key, hours, priority_int, subject in all_selected_chapters_with_meta:
    chapters_by_subject[subject].append((ch_key, hours, priority_int))

# Sort chapters within each subject by priority (int) and then by hours (descending)
for subject in chapters_by_subject:
    chapters_by_subject[subject].sort(key=lambda x: (x[2], -x[1]))


total_selected_hours = sum(ch[1] for ch in all_selected_chapters_with_meta)
total_days = (end_date - start_date).days + 1
total_available_hours = total_days * study_hours

st.markdown(f"### 🧮 Total Selected Hours: `{total_selected_hours}` | Total Available Hours: `{total_available_hours}`")


# ---------------------------- Generate Plan Function (Refactored) ----------------------------
def generate_plan(chapters_by_subject_dict, ordered_subjects_list, hours_per_day, start_date, end_date):
    plan = []
    current_day = start_date

    # Create a deque for each subject's chapters, maintaining internal priority
    subject_queues = {
        subject: deque(chapters_by_subject_dict[subject])
        for subject in ordered_subjects_list if subject in chapters_by_subject_dict and chapters_by_subject_dict[subject]
    }

    # Filter ordered_subjects_list to only include subjects that actually have selected chapters
    active_ordered_subjects = [
        s for s in ordered_subjects_list 
        if s in subject_queues and subject_queues[s]
    ]

    subject_idx = 0 # To track which subject we are currently focusing on in the ordered list

    while current_day <= end_date and active_ordered_subjects:
        available_time = hours_per_day
        today_topics = []
        
        # Determine the current primary subject for today
        current_primary_subject = None
        if active_ordered_subjects:
            current_primary_subject = active_ordered_subjects[subject_idx % len(active_ordered_subjects)]
            # Ensure the chosen primary subject still has chapters
            while current_primary_subject not in subject_queues or not subject_queues[current_primary_subject]:
                subject_idx += 1
                if subject_idx >= len(active_ordered_subjects): # All subjects done or looped through
                    current_primary_subject = None
                    break
                current_primary_subject = active_ordered_subjects[subject_idx % len(active_ordered_subjects)]
        
        if current_primary_subject is None: # All chapters for all subjects are done
            plan.append((current_day.strftime("%d-%b-%Y"), [])) # Free day
            current_day += timedelta(days=1)
            continue


        # Try to fill the day with chapters from the current_primary_subject
        while available_time > 0 and subject_queues[current_primary_subject]:
            chapter_full_name, remaining_ch_time, priority_int = subject_queues[current_primary_subject][0] # Peek

            if remaining_ch_time <= available_time:
                # Chapter fits entirely
                chapter_item = subject_queues[current_primary_subject].popleft()
                today_topics.append((chapter_item[0], chapter_item[1]))
                available_time -= chapter_item[1]
            else:
                # Chapter needs to be split
                chapter_item = subject_queues[current_primary_subject].popleft()
                today_topics.append((f"{chapter_item[0]} (Part)", available_time))
                # Push the remaining part back to the front of the deque
                subject_queues[current_primary_subject].appendleft((chapter_item[0], chapter_item[1] - available_time, chapter_item[2]))
                available_time = 0 # No more time left for today
        
        # After trying the primary subject, if there's still time and max_subjects_per_day allows more,
        # fill with other subjects in order of overall priority
        # This is where the 'max_subjects_per_day' comes into play, but primarily when a subject finishes
        # This part ensures daily hours are fully utilized AFTER the primary subject is handled.
        
        # Collect all remaining available chapters from other subjects, sorted by priority, for potential filling
        remaining_chapters_overall = []
        for s in active_ordered_subjects:
            if s != current_primary_subject and subject_queues[s]: # Only consider other subjects
                for ch_item in subject_queues[s]:
                    remaining_chapters_overall.append((ch_item[0], ch_item[1], ch_item[2], s)) # Add subject name back for filtering

        # Sort these by priority (int) and then hours (descending)
        remaining_chapters_overall.sort(key=lambda x: (x[2], -x[1]))
        
        # Keep track of subjects already added to today's plan
        subjects_for_today = {current_primary_subject} if current_primary_subject else set()

        temp_remaining_chapters_for_reschedule = deque()

        for ch_key, ch_hours, ch_priority, ch_subject in remaining_chapters_overall:
            if available_time <= 0:
                # No more time left for today, push back chapters to their respective queues
                temp_remaining_chapters_for_reschedule.append((ch_key, ch_hours, ch_priority, ch_subject))
                continue

            if ch_subject not in subjects_for_today and len(subjects_for_today) >= max_subjects_per_day:
                # Max subjects reached for today, push back
                temp_remaining_chapters_for_reschedule.append((ch_key, ch_hours, ch_priority, ch_subject))
                continue

            # This chapter can be added
            # We need to find and remove it from its original subject_queue first
            
            # This is a bit inefficient for a deque, might need to rebuild or find index
            # A more robust solution might use a heap/priority queue for overall chapters
            # and then filter by subject. For now, let's make sure it's removed.
            
            # Find and remove the chapter from its specific subject_queue
            original_queue_list = list(subject_queues[ch_subject])
            found_idx = -1
            for i, (q_ch_key, q_ch_hours, q_ch_priority) in enumerate(original_queue_list):
                if q_ch_key == ch_key and q_ch_hours == ch_hours: # Match by chapter key and current remaining hours
                    found_idx = i
                    break
            
            if found_idx != -1: # Chapter found in its original queue
                del original_queue_list[found_idx]
                subject_queues[ch_subject] = deque(original_queue_list) # Reassign deque

                if ch_hours <= available_time:
                    today_topics.append((ch_key, ch_hours))
                    available_time -= ch_hours
                    subjects_for_today.add(ch_subject)
                else:
                    # Split chapter
                    today_topics.append((f"{ch_key} (Part)", available_time))
                    remaining_part_hours = ch_hours - available_time
                    # Add remaining part back to the front of its subject's queue
                    subject_queues[ch_subject].appendleft((ch_key, remaining_part_hours, ch_priority))
                    available_time = 0
                    subjects_for_today.add(ch_subject)
            else:
                # This should ideally not happen if logic is perfect; indicates chapter wasn't found where expected
                temp_remaining_chapters_for_reschedule.append((ch_key, ch_hours, ch_priority, ch_subject))


        # Re-add temporarily unscheduled chapters to their respective subject queues
        for ch_key, ch_hours, ch_priority, ch_subject in temp_remaining_chapters_for_reschedule:
            subject_queues[ch_subject].appendleft((ch_key, ch_hours, ch_priority)) # Add back to front to maintain priority


        plan.append((current_day.strftime("%d-%b-%Y"), today_topics))
        current_day += timedelta(days=1)

        # Move to the next primary subject for the next day
        subject_idx += 1

        # Clean up subject_queues (remove subjects that are now empty)
        active_ordered_subjects = [s for s in active_ordered_subjects if s in subject_queues and subject_queues[s]]


    # Check for remaining chapters after the end date
    remaining_hours_uncovered = 0
    for subject_q in subject_queues.values():
        for ch_item in subject_q:
            remaining_hours_uncovered += ch_item[1]

    if remaining_hours_uncovered > 0:
        st.warning(f"Note: Not all selected chapters could be scheduled within the given date range. Remaining hours: {remaining_hours_uncovered:.2f}")

    return plan


# ---------------------------- Planner Display ----------------------------
if st.button("✅ Generate Study Plan"):
    # Pre-check: Ensure selected subjects match ordered subjects for consistency
    if set(selected_subjects) != set(ordered_subjects):
        st.error("❌ The 'Choose Subjects' and 'Subject Revision Order' lists must contain the same subjects.")
    elif start_date >= end_date:
        st.error("❌ End date must be after start date.")
    elif not all_selected_chapters_with_meta:
        st.warning("⚠️ Please select at least one chapter.")
    elif total_selected_hours > total_available_hours:
        st.warning("⚠️ Selected content exceeds available time. Please reduce selection or increase study hours/date range.")
    else:
        # Pass the pre-sorted chapters organized by subject and the user's subject order
        plan = generate_plan(chapters_by_subject, ordered_subjects, study_hours, start_date, end_date)

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
            # If it's "Subj - Subsubj - Chapter" or "Subj - Chapter", take the last part
            if len(parts) > 1:
                return parts[-1].replace(" (Part)", "").strip()
            # If it's just "Chapter" (unlikely with current naming but for safety)
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
        pdf.multi_cell(0, 8, f"Max Subjects per Day: {max_subjects_per_day}")
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
