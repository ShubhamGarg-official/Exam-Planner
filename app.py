# 📘 Final app.py for CA Exam Planner
# Includes: Time-based planner, group-wise selection, subject/chapter selection, Excel+PDF export

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from fpdf import FPDF
from ca_exam_data import data  # <- Your subject & chapter data

st.set_page_config(page_title="CA Exam Planner", layout="wide")
st.title("📘 CA Exam Planner")
st.markdown("Plan your CA exam revisions based on time and topic.")

# 1. Study Hours Input
study_hours = st.number_input("🕒 How many hours can you study per day?", min_value=1, max_value=16, value=6)

# 2. Group Selection
group_choice = st.radio("🧠 Which Group are you preparing for?", ["Group I", "Group II", "Both Groups"])
if group_choice == "Group I":
    selected_data = data["Group I"]
elif group_choice == "Group II":
    selected_data = data["Group II"]
else:
    selected_data = {**data["Group I"], **data["Group II"]}

# 3. Date Inputs
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 Revision Start Date", datetime.today())
with col2:
    end_date = st.date_input("🗓️ Revision End Date", datetime.today() + timedelta(days=30))

# 4. Subject Selection
all_subjects = list(selected_data.keys())
select_all_subjects = st.checkbox("📚 Select All Subjects")
selected_subjects = st.multiselect("Choose Subjects", all_subjects, default=all_subjects if select_all_subjects else [])

# 5. Chapter Selection
final_chapters = {}
total_selected_hours = 0

for subject in selected_subjects:
    chapters = selected_data[subject]
    flat_chapters = {}

    if any(isinstance(v, dict) for v in chapters.values()):
        for part, subtopics in chapters.items():
            for ch, hr in subtopics.items():
                flat_chapters[f"{part} - {ch}"] = hr
    else:
        flat_chapters = chapters

    chapter_names = list(flat_chapters.keys())
    select_all_chapters = st.checkbox(f"Select all chapters for {subject}")
    selected_chaps = st.multiselect(f"📄 Chapters from {subject}", chapter_names, default=chapter_names if select_all_chapters else [])

    for ch in selected_chaps:
        final_chapters[f"{subject} - {ch}"] = flat_chapters[ch]
        total_selected_hours += flat_chapters[ch]

# 6. Generate Plan
if st.button("📅 Generate Study Planner"):
    total_days = (end_date - start_date).days + 1
    total_available_hours = total_days * study_hours

    st.markdown(f"### 🧮 Total Selected Hours: {total_selected_hours} | Total Available Hours: {total_available_hours}")

    if total_selected_hours > total_available_hours:
        st.error("Selected content requires more hours than available. Please adjust.")
    elif total_selected_hours == 0:
        st.warning("Please select at least one chapter.")
    else:
        chapters_list = list(final_chapters.items())
        plan = []
        idx = 0
        current_day = start_date

        while current_day <= end_date:
            day_plan = []
            available_time = study_hours

            while idx < len(chapters_list) and available_time >= chapters_list[idx][1]:
                day_plan.append(f"{chapters_list[idx][0]} ({chapters_list[idx][1]} hrs)")
                available_time -= chapters_list[idx][1]
                idx += 1

            plan.append((current_day.strftime("%d-%b-%Y"), day_plan))
            current_day += timedelta(days=1)

        st.success("✅ Planner Ready!")
        plan_data = []

        for day, topics in plan:
            st.subheader(f"📆 {day}")
            if topics:
                for topic in topics:
                    st.markdown(f"- {topic}")
                    plan_data.append({"Date": day, "Plan": topic})
            else:
                st.write("🔸 Free / Buffer Day")
                plan_data.append({"Date": day, "Plan": "Free / Buffer Day"})

        df_export = pd.DataFrame(plan_data)

        # Excel Export
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name="Study Plan")
            worksheet = writer.sheets["Study Plan"]
            worksheet.set_column("A:B", 40)
        st.download_button("⬇️ Download Excel", data=buffer.getvalue(), file_name="CA_Study_Plan.xlsx")

        # PDF Export
from fpdf import FPDF
import io

# Create the PDF
from fpdf import FPDF
import io

# Calculate totals
total_selected_hours = sum(final_chapter_dict.values())
total_available_hours = (end_date - start_date).days * study_hours

# Create the PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="CA Exam Planner", ln=True, align='C')
pdf.ln(5)
pdf.cell(200, 8, txt=f"Study Hours per Day: {study_hours}", ln=True)
pdf.cell(200, 8, txt=f"Revision Period: {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}", ln=True)
pdf.cell(200, 8, txt=f"Total Selected Hours: {total_selected_hours} | Total Available Hours: {total_available_hours}", ln=True)
pdf.ln(5)

for day, topics in plan:
    pdf.set_font("Arial", 'B', size=11)
    pdf.cell(200, 8, txt=f"{day}", ln=True)
    pdf.set_font("Arial", size=11)
    if topics:
        for topic in topics:
            pdf.cell(200, 8, txt=f"- {topic}", ln=True)
    else:
        pdf.cell(200, 8, txt="Free / Buffer Day", ln=True)
    pdf.ln(2)

# Convert to byte stream
pdf_output = pdf.output(dest='S').encode('latin1')
pdf_buffer = io.BytesIO(pdf_output)

st.download_button(
    label="Download Planner as PDF",
    data=pdf_buffer,
    file_name="CA_Exam_Planner.pdf",
    mime="application/pdf"
)



st.markdown("---")
st.caption("Built with ❤️ for CA students by a CA Student")
