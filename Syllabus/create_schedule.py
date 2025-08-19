import datetime as dt
import pandas as pd
import os, re
import numpy as np

#################################################
# Function to get dates for the semester
#################################################

# Dictionary to map weekdays to their index
day_to_index = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


# Function to get dates for a specific weekday
def get_dates(start, end, weekdays, year):
    """
    Returns a list of dates that fall on a specific weekday between two dates.
        - start: The start date of the semester.
        - end: The end date of the semester.
        - weekdays: Weekdays to filter the dates (e.g., 'Tue', 'Thu').
        - year: The year of the semester.
    """
    weekdaysnum = [day_to_index[day] for day in weekdays]
    start_date = dt.datetime.strptime(start + "/" + str(year), "%m/%d/%Y")
    end_date = dt.datetime.strptime(end + "/" + str(year), "%m/%d/%Y")
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in weekdaysnum:
            dates.append(current_date.strftime("%a %m/%d"))
        current_date += dt.timedelta(days=1)
    return dates


#################################################
# Function to write table to latex
#################################################


def latex(df, filename=None):
    lines = []
    if filename is None:
        for i in range(df.shape[0]):
            lines.append(" & ".join([str(x) for x in df.iloc[i]]) + " \\\\")
        return lines
    else:
        with open(filename, "w") as f:
            for i in range(df.shape[0]):
                f.write(" & ".join([str(x) for x in df.iloc[i]]) + " \\\\\n")


#################################################
# Functions for the html table
#################################################


def icon(doctype):
    if doctype == "notes":
        return "📔"
    if doctype == "slides":
        return "🖥️"
    if doctype == "ws":
        return "🗒️"
    if doctype == "hw":
        return "✍️"
    if doctype == "sol":
        return "📖"


def material_str(x):
    if x != "" and int(x) != 12:
        x = int(x)
    else:
        return ""
    dest = f"Lectures/Lecture{x}"
    files = os.listdir(dest)
    material = {}
    material["slides"] = f"Slides{x}.pdf"
    material["ws"] = [f for f in files if re.match(r"Handout-.*\.pdf", f)]
    material["hw"] = f"homework{x}.pdf"
    material["sol"] = f"homework{x}_solutions.pdf"
    material_str = ""
    for key, value in material.items():
        if type(value) == list:
            for v in value:
                material_str += f"<a href='{dest}/{v}'>{icon(key)}</a> "
        else:
            material_str += f"<a href='{dest}/{value}'>{icon(key)}</a> "
    return material_str


#################################################
# Specify syllabus content
#################################################

# Modules
modules = {}
modules["prelim"] = "Preliminaries"
modules["linal"] = "Linear Algebra"
modules["calc"] = "Calculus"
modules["opt"] = "Optimization"
modules["add"] = "Add. Topics"

# Topics
topics = {}

# Topics: Preliminaries
prelim1 = (
    "Numbers and sets; "
    "Relations and functions; "
    "Summation notation; "
    "Necessary and sufficient conditions"
)
topics["prelim"] = [prelim1]

# Topics: Linear Algebra
linal1 = (
    "Matrices: Addition, Subtraction, and Scalar Multiplication; "
    "Matrix Multiplication; "
    "Vectors; "
    "Identity and Null Matrices; "
    "Transpose and Inverse of a Matrix"
)
linal2 = "Conditions for Nonsingularity of a Matrix; " "Determinant of a Matrix"
linal3 = "Finding the Inverse of a Matrix; " "Cramer’s Rule; " "Applications"
topics["linal"] = [linal1, linal2, linal3]

# Topics: Calculus
calc1 = (
    "Limit Definition of a Derivative; "
    "Limits; "
    "Continuity; "
    "Rules of Differentiation"
)
calc2 = (
    "Exponential and Log Functions; "
    "Partial Derivatives; "
    "Total Differential and Derivative"
)
calc3 = "Implicit Function Theorem; " "Integration"
topics["calc"] = [calc1, calc2, calc3]

# Topics: Optimization
opt1 = "Unconstrained Single-Variable Optimization; " "Concave and Convex Functions"
opt2 = "Multivariable Optimization"
opt3 = "Constrained Optimization"
opt4 = "Envelope Theorem; " "Quasiconcavity; " "Convex sets; " "Homogenous Functions"
topics["opt"] = [opt1, opt2, opt3, opt4]

# Topics: Additional Topics
add1 = "TBA"
topics["add"] = [add1]

# Collect modules
mods = ["prelim", "linal", "calc", "opt", "add"]
n_lecs = sum(len(topics[mod]) for mod in mods)

## Code here slightly more general than Econ340 (can edit that)

#################################################
# Create Syllabus
#################################################

# Initialize
sem = "fall"
class_days = ["Mon"]

# Fall semester dates
if sem == "fall":
    dates = get_dates("08/23", "12/12", class_days, 2025)
    break_ = get_dates("11/24", "11/30", class_days, 2025)
    examday = "Mon 12/15"
    add_holidays = ["Mon 09/01"]
    holiday_names = ["Labor Day"]

# Spring semester dates
if sem == "spring":
    dates = get_dates("01/18", "05/09", class_days, 2025)
    break_ = get_dates("03/31", "04/06", class_days, 2025)
    examday = "Thu 05/13"
    add_holidays = []
    holiday_names = []

# Set the midterm date
midterm_idx = 9

# Add final exam date
dates.append(examday)

# Collect indices for breaks, review classes, and exams
mid_review_idx = midterm_idx - 1
add_holidays_idx = [dates.index(add_holiday) for add_holiday in add_holidays]
break_idx = dates.index(break_[0])
final_review_idx = len(dates) - 2
final_idx = len(dates) - 1

# Create list with just lecture dates
rm_idxs = [
    break_idx,
    mid_review_idx,
    midterm_idx,
    final_review_idx,
    final_idx,
] + add_holidays_idx
lec_dates = [date for i, date in enumerate(dates) if i not in rm_idxs]
n_lec_dates = len(lec_dates)

# Review class and midterm index
if n_lec_dates < n_lecs:
    mods = mods[:-1]
    n_lecs = sum(len(topics[mod]) for mod in mods)
if n_lec_dates < n_lecs:
    raise ValueError(f"Not enough lecture dates for the number of lectures ({n_lecs}).")

# If only one class day, remove the day from dates column
if len(class_days) == 1:
    dates = [date[4:] for date in dates]
    lec_dates = [date[4:] for date in lec_dates]

# Create a DataFrame with the dates
df = pd.DataFrame(
    {
        "Date": lec_dates,
        "Lecture": range(1, n_lecs + 1),
        "Module": "",
        "Topics": "",
        "References": "",
        "Quiz": "",
    },
    dtype="object",
)

# Insert modules and topics
mod_idx = [sum(len(topics[mod]) for mod in mods[:i]) for i in range(len(mods))]
for i, mod in enumerate(mods):
    df.loc[mod_idx[i], "Module"] = modules[mod]
    for j, topic in enumerate(topics[mod]):
        df.loc[mod_idx[i] + j, "Topics"] = topic

# Add references
df.loc[df["Lecture"] == 1, "References"] = "2.2, 2.3, 2.4-2.6, pg 163, 5.1"
df.loc[df["Lecture"] == 2, "References"] = "4.1-4.6"
df.loc[df["Lecture"] == 3, "References"] = "4.7, 5.1-5.3"
df.loc[df["Lecture"] == 4, "References"] = "5.3-5.5"
df.loc[df["Lecture"] == 5, "References"] = "6.2-6.4, 6.7, 7.1-7.3"
df.loc[df["Lecture"] == 6, "References"] = "10.5, 7.4, 8.1, 8.2, 8.4"
df.loc[df["Lecture"] == 7, "References"] = "8.5, 14.1-14.3"
df.loc[df["Lecture"] == 8, "References"] = "9.1, 9.2, 9.3, 9.4"
df.loc[df["Lecture"] == 9, "References"] = "11.1, 11.2"
df.loc[df["Lecture"] == 10, "References"] = "12.1, 12.2"
df.loc[df["Lecture"] == 11, "References"] = "11.5, 12.4, 12.6"
df.loc[df["Lecture"] == 12, "References"] = ""

# Add quizzes
df.loc[df["Lecture"] == 3, "Quiz"] = "Quiz 1"
df.loc[df["Lecture"] == 5, "Quiz"] = "Quiz 2"
df.loc[df["Lecture"] == 7, "Quiz"] = "Quiz 3"
df.loc[df["Lecture"] == 10, "Quiz"] = "Quiz 4"
df.loc[df["Lecture"] == 12, "Quiz"] = "Quiz 5"

# Add back all original dates
df_tmp = pd.DataFrame({"Date": dates})
df = df_tmp.merge(df, on="Date", how="left")

# Add description for additional dates
# df.loc[break_idx, "Date"] = ""
if sem == "fall":
    df.loc[break_idx, "Topics"] = "Fall Recess"
if sem == "spring":
    df.loc[break_idx, "Topics"] = "Spring Recess"
for i, add_holiday in enumerate(add_holidays_idx):
    df.loc[add_holiday, "Date"] = dates[add_holiday]
    df.loc[add_holiday, "Topics"] = holiday_names[i]
df.loc[mid_review_idx, "Topics"] = "Midterm Review"
df.loc[midterm_idx, "Topics"] = "Midterm Exam"
df.loc[final_review_idx, "Topics"] = "Final Review"
df.loc[final_idx, "Topics"] = "Final Exam"

# Replace missing values with empty strings
df = df.fillna("")

#################################################
# Create latex table
#################################################

# Get the latex lines
lines = latex(df)

# Module beginnings and endings
mdlbegs = np.array(df[df["Module"] != ""].index)
n_tops = [len(topics[mod]) for mod in mods]
mdlends = mdlbegs + n_tops

# Specify indices for bold lines
mdlends[-1] += 1  # Manual adjustment for the last module
bold_lines = set(mdlends - 1) | set(mdlbegs - 1)
bold_lines = bold_lines | {len(lines) - 1}

# Full line pist midterm and final review
full_lines = [mid_review_idx, final_review_idx, break_idx, break_idx - 1]

# # Multirow for Module column
bs = [8, 18, 14, 20]  # manually set
for i, row in enumerate(mdlbegs):
    row_content = df.loc[row].copy()
    mod = df.loc[row, "Module"]
    row_content["Module"] = f"\\multirow{{{n_tops[i]}}}[{bs[i]}]{{*}}{{{mod}}}"
    lines[row] = " & ".join([str(x) for x in row_content]) + " \\\\\n"

# Special multicolumn rows
splrows = df[df["Lecture"] == ""].index
for row in splrows:
    lines[row] = (
        df.loc[row, "Date"]
        + " & "
        + f'\\multicolumn{{4}}{{c}}{{{df.loc[row, "Topics"]}}}'
        + " & "
        + " \\\\"
    )

# Add horizontal lines
for row in range(len(lines)):
    if row in bold_lines:
        lines[row] += "\\Xhline{1.75\\arrayrulewidth} "
    elif row in full_lines:
        lines[row] += "\\hline "
    else:
        lines[row] += " \\cline{1-2} \\cline{4-6}"

# Write to file
with open("Syllabus/schedule.tex", "w") as f:
    for line in lines:
        f.write(line + "\n")


#################################################
# Create HTML version
#################################################

# Convert dates from 08/27 to Aug 27
# df = df[df["Date"] != ""].copy()
df["Date"] = df["Date"].apply(
    lambda x: dt.datetime.strptime(x, "%m/%d").strftime("%b %d") if x != "" else ""
)

# Add lecture number and links to Date column (remove lecture col)
df.loc[df["Lecture"] != "", "Date"] = (
    df.loc[df["Lecture"] != "", "Date"]
    + "<br><a href='Lectures/Lecture"
    + df.loc[df["Lecture"] != "", "Lecture"].astype(str)
    + "/lecture"
    + df.loc[df["Lecture"] != "", "Lecture"].astype(str)
    + ".qmd'>Lecture "
    + df.loc[df["Lecture"] != "", "Lecture"].astype(str)
    + "</a>"
)

# Add Material column
df["Material"] = df["Lecture"].apply(material_str)

# Add notes links to each module
notes = {}
notes["prelim"] = []
notes["linal"] = ["Linear-Algebra.pdf"]
notes["calc"] = ["Calculus.pdf", "Log-and-Exponential-Functions.pdf"]
notes["opt"] = ["Optimization.pdf"]
for mod, nnotes in notes.items():
    mod_idx = df[df["Module"] == modules[mod]].index[0]
    df.loc[mod_idx, "Module"] += "<br>"
    for note in nnotes:
        df.loc[mod_idx, "Module"] += f"<a href='Notes/{note}'>{icon('notes')}</a> "

# Assessment column
df.loc[df.index[-1], "Topics"] = "Final Exam"
df["Assessment"] = df["Quiz"]
df.loc[df["Topics"].str.contains("Exam"), "Assessment"] = df["Topics"]
df.loc[df["Topics"].str.contains("Exam"), "Topics"] = ""

# Remove Lecture, References, and Quiz columns
df = df.drop(columns=["Lecture", "References", "Quiz"])

# save to html
df.to_html("Syllabus/schedule.html", index=False, escape=False)

#################################################
