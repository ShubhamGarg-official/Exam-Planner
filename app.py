import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import io
from fpdf import FPDF
from collections import defaultdict, deque

# Import your data
from ca_exam_data import data

# ---------------------------- Streamlit Page Setup ----------------------------
st.set_page_config(page_title="CA Exam Planner", layout="wide")
st.title("📘 CA Exam Planner")
st.markdown("Plan your CA exam revisions based on your time and topic preferences.")

# ---------------------------- User Inputs ----------------------------
study_hours = st.number_input("🕒 How many hours can you study per day?", min_value=1, max_value=16, value=14) # Changed default to 14
max_subjects_per_day = st.selectbox(
    "🔢 Max number of subjects per day:",
    [1, 2, 3], # Options for 1, 2, or 3 subjects max
    index=0 # Default to 1 subject per day for "at a stretch" behavior
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
ordered_subjects = []
if selected_subjects:
    st.markdown("---")
    st.subheader("Subject Revision Order")
    st.info("Drag and drop to arrange the order in which you want to study subjects. This will primarily dictate the sequence of subjects in your plan.")
    
    ordered_subjects = st.multiselect(
        "Set your preferred subject order:",
        options=selected_subjects,
        default=selected_subjects, # Default to the order they were selected in or alphabetical
        key="subject_order_multiselect"
    )

# Stores all selected chapters with their original hours, full path, and subject name
# Will be populated with (full_chapter_key, hours, priority_level_int, main_subject_name)
all_selected_chapters_with_meta = [] 

# Iterate through selected subjects to get their chapters and assign importance
for main_subject in selected_subjects:
    chapters_in_main_subject = selected_data[main_subject]

    # Handle subjects that contain sub-subjects (like Taxation, FMSM)
    # Check if any value in chapters_in_main_subject is a dictionary, indicating nesting
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
                
                # Get importance lists for the SUB-SUBJECT (e.g., Income Tax_High_Importance)
                # Pass chapters_in_main_subject as it contains the _High_Importance lists for sub-subjects
                high_imp_list, medium_imp_list, least_imp_list = get_importance_lists(chapters_in_main_subject, sub_subject)

                for full_ch_key in selected_chapters_from_sub:
                    original_chapter_name = full_ch_key.split(' - ')[-1] # Extract just the chapter name
                    hours = sub_chapters_or_lists[original_chapter_name]
                    
                    priority_int = 3 # Default to 'Other'
                    if original_chapter_name in high_imp_list:
                        priority_int = 0
                    elif original_chapter_name in medium_imp_list:
                        priority_int = 1
                    elif original_chapter_name in least_imp_list:
                        priority_int = 2
                    
                    all_selected_chapters_with_meta.append((full_ch_key, float(hours), priority_int, main_subject)) 

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
        
        # Get importance lists for the MAIN SUBJECT (e.g., Advance Accounting_High_Importance)
        # Pass selected_data as it contains the _High_Importance lists for top-level subjects
        high_imp_list, medium_imp_list, least_imp_list = get_importance_lists(selected_data, main_subject)

        for full_ch_key in selected_chapters_from_main:
            original_chapter_name = full_ch_key.split(' - ')[-1] # Extract just the chapter name
            hours = chapters_in_main_subject[original_chapter_name]

            priority_int = 3
            if original_chapter_name in high_imp_list:
                priority_int = 0
            elif original_chapter_name in medium_imp_list:
                priority_int = 1
            elif original_chapter_name in least_imp_list:
                priority_int = 2
            
            all_selected_chapters_with_meta.append((full_ch_key, float(hours), priority_int, main_subject)) 


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


# ---------------------------- Generate Plan Function (Refactored for "Subject at a Stretch") ----------------------------
def generate_plan(chapters_by_subject_dict, ordered_subjects_list, hours_per_day, start_date, end_date, max_subjects_per_day):
    plan = []
    current_day = start_date

    # Create a deque for each subject's chapters, maintaining internal priority
    # Only include subjects from the ordered list that actually have selected chapters
    subject_queues = {
        subject: deque(chapters_by_subject_dict[subject])
        for subject in ordered_subjects_list if subject in chapters_by_subject_dict and chapters_by_subject_dict[subject]
    }

    # Filter ordered_subjects_list to only include subjects that actually have selected chapters initially
    active_ordered_subjects = [
        s for s in ordered_subjects_list 
        if s in subject_queues and subject_queues[s]
    ]

    subject_index_in_order = 0 # Index to pick the primary subject from active_ordered_subjects

    while current_day <= end_date and active_ordered_subjects:
        available_time = hours_per_day
        today_topics = []
        subjects_scheduled_today_count = 0
        
        # Determine the current primary subject for today based on the ordered list
        # This subject will be prioritized for study "at a stretch"
        current_primary_subject = active_ordered_subjects[subject_index_in_order % len(active_ordered_subjects)]
        
        # --- PHASE 1: Try to fill the day with the current primary subject ---
        if subject_queues[current_primary_subject]: # Ensure the primary subject still has chapters
            subjects_scheduled_today_count += 1
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
            
            # If the primary subject's queue is now empty, remove it from active list
            if not subject_queues[current_primary_subject]:
                # Rebuild active_ordered_subjects to remove the completed subject
                active_ordered_subjects = [s for s in active_ordered_subjects if s != current_primary_subject]
                # If there are still active subjects, adjust the index. If all are done, index becomes irrelevant.
                if active_ordered_subjects:
                    subject_index_in_order = subject_index_in_order % len(active_ordered_subjects) # Ensure index is valid for new list size
                else:
                    subject_index_in_order = -1 # Indicate no more subjects
        
        # --- PHASE 2: Fill remaining hours with other subjects if allowed and necessary ---
        # This only happens if max_subjects_per_day > 1 AND there's still time left AND there are other active subjects
        if available_time > 0 and subjects_scheduled_today_count < max_subjects_per_day and active_ordered_subjects:
            
            # Iterate through subjects, starting from the one *after* the current primary subject in the ordered list,
            # to fill remaining time, respecting max_subjects_per_day.
            # This ensures we pick distinct subjects for the secondary slots if allowed.
            
            # Start search for next subject from the one after the primary one in the ordered list
            start_search_idx = (ordered_subjects_list.index(current_primary_subject) + 1) % len(ordered_subjects_list) if current_primary_subject in ordered_subjects_list else 0
            
            # Use a loop to cycle through ordered subjects to find next available ones
            for _ in range(len(ordered_subjects_list)): # Max iterations to prevent infinite loop
                candidate_subject_name = ordered_subjects_list[start_search_idx]
                
                # Only consider if it's an active subject (has chapters remaining) AND not the primary subject already scheduled
                if candidate_subject_name in active_ordered_subjects and subject_queues[candidate_subject_name] and candidate_subject_name != current_primary_subject:
                    
                    if subjects_scheduled_today_count >= max_subjects_per_day:
                        break # Reached max subjects for the day
                    
                    # Schedule chapters from this secondary subject
                    while available_time > 0 and subject_queues[candidate_subject_name]:
                        chapter_full_name, remaining_ch_time, priority_int = subject_queues[candidate_subject_name][0] # Peek
                        
                        if remaining_ch_time <= available_time:
                            chapter_item = subject_queues[candidate_subject_name].popleft()
                            today_topics.append((chapter_item[0], chapter_item[1]))
                            available_time -= chapter_item[1]
                        else:
                            chapter_item = subject_queues[candidate_subject_name].popleft()
                            today_topics.append((f"{chapter_item[0]} (Part)", available_time))
                            subject_queues[candidate_subject_name].appendleft((chapter_item[0], chapter_item[1] - available_time, chapter_item[2]))
                            available_time = 0
                            
                    subjects_scheduled_today_count += 1 # Increment only once per secondary subject added
                    
                    # If this subject's queue is now empty, remove it from active list
                    if not subject_queues[candidate_subject_name]:
                        active_ordered_subjects.remove(candidate_subject_name)
                        if not active_ordered_subjects: # All subjects completed
                            break # Exit outer loop if no more subjects
                
                start_search_idx = (start_search_idx + 1) % len(ordered_subjects_list) # Move to next in ordered list


        plan.append((current_day.strftime("%d-%b-%Y"), today_topics))
        current_day += timedelta(days=1)
        
        # If all subjects are completed, stop the main loop
        if not active_ordered_subjects:
            break
        
        # If the primary subject for the day was completely studied, move to the next in the ordered list for the next day
        # Otherwise, the same subject remains the primary focus.
        if current_primary_subject not in active_ordered_subjects: # If the primary subject for today got exhausted and removed
            # The subject_index_in_order already points to the correct "next" primary subject due to the removal logic above
            pass # Index correctly adjusted
        elif subject_queues[current_primary_subject]: # If primary subject still has chapters, it remains the focus
            pass 
        else: # If primary subject somehow became empty but wasn't removed (shouldn't happen with current logic)
            # This is a safeguard, means primary subject's queue is empty, move to next.
            subject_index_in_order = (subject_index_in_order + 1) % len(active_ordered_subjects)


    # Fill remaining days as free if all chapters are done before end_date
    while current_day <= end_date:
        plan.append((current_day.strftime("%d-%b-%Y"), [])) # Free day
        current_day += timedelta(days=1)


    # Check for remaining chapters after the end date (should be few now)
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
        # Pass the chapters organized by subject and the user's subject order
        # Convert chapters_by_subject to deques as expected by generate_plan
        subject_queues_for_plan = {subject: deque(chapters) for subject, chapters in chapters_by_subject.items()}
        plan = generate_plan(subject_queues_for_plan, ordered_subjects, study_hours, start_date, end_date, max_subjects_per_day)

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
        df_export[["FullTopic", "Estimated Hours"]] = df_export["Plan"].str.extract(r'(.*)\((\d+(?:\.\d+)?) hrs\)')
        
        # Further refine 'Topic' to just the chapter name, removing subject/subtopic prefixes
        def extract_chapter_name(full_topic):
            parts = full_topic.split(' - ')
            # If it's "Subject - Subsubject - Chapter" or "Subject - Chapter", take the last part
            if len(parts) > 1:
                return parts[-1].replace(" (Part)", "").strip()
            # If it's just "Chapter" (unlikely with current naming but for safety)
            return full_topic.replace(" (Part)", "").strip()

        df_export["Topic"] = df_export["FullTopic"].apply(extract_chapter_name)
        df_export["Estimated Hours"] = pd.to_numeric(df_export["Estimated Hours"]) # Ensure numerical
        df_export = df_export[["Date", "Topic", "Estimated Hours"]]


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
