import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import io
from fpdf import FPDF
import base64
from ca_exam_data import data  # This should contain the complete subject-chapter dictionary with hours

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
all_subjects = list(selected_data.keys())
select_all_subjects = st.checkbox("📚 Select All Subjects")
selected_subjects = st.multiselect("Choose Subjects", all_subjects, default=all_subjects if select_all_subjects else [])

final_chapter_dict = {}

for subject in selected_subjects:
    chapters = selected_data[subject]
    flat_chapters = {}

    # Handle nested subjects
    if any(isinstance(val, dict) for val in chapters.values()):
        for subtopic, subchaps in chapters.items():
            for ch, hr in subchaps.items():
                key = f"{subject} - {subtopic} - {ch}"
                flat_chapters[key] = hr
    else:
        for ch, hr in chapters.items():
            key = f"{subject} - {ch}"
            flat_chapters[key] = hr

    chapter_names = list(flat_chapters.keys())
    select_all = st.checkbox(f"Select all chapters for {subject}")
    selected_chapters = st.multiselect(f"📄 Chapters from {subject}", chapter_names, default=chapter_names if select_all else [])

    for ch in selected_chapters:
        final_chapter_dict[ch] = flat_chapters[ch]

# ---------------------------- Display Totals ----------------------------
total_selected_hours = sum(final_chapter_dict.values())
total_days = (end_date - start_date).days + 1
total_available_hours = total_days * study_hours

st.markdown(f"### 🧮 Total Selected Hours: `{total_selected_hours}` | Total Available Hours: `{total_available_hours}`")

# ---------------------------- Generate Plan ----------------------------
def generate_plan(chapters, hours_per_day, start_date, end_date):
    plan = []
    current_day = start_date
    idx = 0
    chapters = list(chapters.items())

    while current_day <= end_date and idx < len(chapters):
        available_time = hours_per_day
        today = []
        while available_time > 0 and idx < len(chapters):
            chapter, ch_time = chapters[idx]
            if ch_time <= available_time:
                today.append((chapter, ch_time))
                available_time -= ch_time
                idx += 1
            else:
                # Split the chapter across multiple days
                today.append((f"{chapter} (Part)", available_time))
                chapters[idx] = (chapter, ch_time - available_time)
                available_time = 0
        plan.append((current_day.strftime("%d-%b-%Y"), today))
        current_day += timedelta(days=1)
    return plan


# ---------------------------- Planner Display ----------------------------
if st.button("✅ Generate Study Plan"):
    if start_date >= end_date:
        st.error("❌ End date must be after start date.")
    elif not final_chapter_dict:
        st.warning("⚠️ Please select at least one chapter.")
    elif total_selected_hours > total_available_hours:
        st.warning("⚠️ Selected content exceeds available time. Please reduce selection or increase study hours/date range.")
    else:
        plan = generate_plan(final_chapter_dict, study_hours, start_date, end_date)

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
        # Extract full topic and hours
df_export[["FullTopic", "Estimated Hours"]] = df_export["Plan"].str.extract(r'(.*)\((\d+(?:\.\d+)?) hrs\)')

# Clean the topic name to remove "Advance Accounting - " or similar prefixes
df_export["Topic"] = df_export["FullTopic"].str.extract(r'^[^-]+ - (.*)')

# Drop the extra column
df_export.drop(columns=["FullTopic"], inplace=True)



        # ---------------------------- Export to Excel ----------------------------
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Planner')
            writer.close()
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
                    self.multi_cell(0, 8, f"- {line}")
                self.ln(3)

        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Header info
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, f"Study Hours per Day: {study_hours}")
        pdf.multi_cell(0, 8, f"Revision Period: {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}")
        pdf.multi_cell(0, 8, f"Total Selected Hours: {total_selected_hours} | Total Available Hours: {total_available_hours}")
        pdf.ln(5)

        # Daily Plan
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



  


