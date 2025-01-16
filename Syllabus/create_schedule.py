import datetime as dt
import pandas as pd
import os, re

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

# Specify modules to cover before midterm
midterm_mods = ["prelim", "linal", "calc"]
remaining_mods = ["opt", "add"]

## Code assumes only two modules after the midterm
## Code here slightly more general than Econ340 (can edit that)

#################################################
# Create Syllabus
#################################################

# Initialize
sem = "spring"
class_days = ["Tue"]

# Fall semester dates
if sem == "fall":
    tues_and_thurs = get_dates("08/24", "12/13", class_days, 2024)
    break_ = get_dates("11/26", "12/01", class_days, 2024)
    examday = "Tue 12/17"

# Spring semester dates
if sem == "spring":
    tues_and_thurs = get_dates("01/18", "05/09", class_days, 2025)
    break_ = get_dates("03/31", "04/06", class_days, 2025)
    examday = "Thu 05/13"

# Fall or spring break adjustment
dates = [date for date in tues_and_thurs if date not in break_[1:]]
dates = [date if date != break_[0] else "" for date in dates]

# Add final exam date
dates.append(examday)

# If only one class day, remove the day from dates column
if len(class_days) == 1:
    dates = [date[4:] for date in dates]

# Create a DataFrame with the dates
df = pd.DataFrame(
    {
        "Date": dates,
        "Lecture": "",
        "Module": "",
        "Topics": "",
        "References": "",
        "Quiz": "",
    },
    dtype="object",
)

# Where empty date it's Fall or Spring Recess
break_idx = df[df["Date"] == ""].index[0]
if sem == "fall":
    df.loc[break_idx, "Topics"] = "Fall Recess"
if sem == "spring":
    df.loc[break_idx, "Topics"] = "Spring Recess"

# Add the lecture numbers and topics for lectures before the midterm
counter = 0
for mod in midterm_mods:
    step = len(topics[mod])
    df.loc[counter : counter + step - 1, "Lecture"] = list(
        range(counter + 1, counter + step + 1)
    )
    df.loc[counter, "Module"] = modules[mod]
    df.loc[counter : counter + step - 1, "Topics"] = topics[mod]
    counter += step
lec_counter = counter

# After those lectures: Review Class and Midterm
df.loc[counter, "Topics"] = "Review Class"
counter += 1
df.loc[counter, "Topics"] = "Midterm Exam"
counter += 1

# Split the module following the midterm if needed
next_module = remaining_mods[0]
classes_left = break_idx - counter
# print(f"Classes to break: {classes_left}")
# print(f"Topics in {modules[next_module]} Module: {len(topics[next_module])}")
if classes_left < len(topics[next_module]):
    next_topics = topics[next_module]
    topics[next_module] = next_topics[:classes_left]
    topics[f"{next_module}2"] = next_topics[classes_left:]
    modules[f"{next_module}2"] = f"{modules[next_module]} "

# Add the lecture numbers and topics for the next module
step = len(topics[next_module])
df.loc[counter : counter + step - 1, "Lecture"] = list(
    range(lec_counter + 1, lec_counter + step + 1)
)
df.loc[counter, "Module"] = modules[next_module]
df.loc[counter : counter + step - 1, "Topics"] = topics[next_module]
counter += step
lec_counter += step
counter += 1  # For the break

# Add continued module if next module was broken up (Spring only probably)
if f"{next_module}2" in topics:
    step = len(topics[f"{next_module}2"])
    df.loc[counter : counter + step - 1, "Lecture"] = list(
        range(lec_counter + 1, lec_counter + step + 1)
    )
    df.loc[counter, "Module"] = modules[f"{next_module}2"]
    df.loc[counter : counter + step - 1, "Topics"] = topics[f"{next_module}2"]
    counter += step
    lec_counter += step

# Add the lecture numbers and topics for remaining modules
last_module = remaining_mods[-1]
step = len(topics[last_module])
df.loc[counter : counter + step - 1, "Lecture"] = list(
    range(lec_counter + 1, lec_counter + step + 1)
)
df.loc[counter, "Module"] = modules[last_module]
df.loc[counter : counter + step - 1, "Topics"] = topics[last_module]
counter += step
lec_counter += step

# Last two lectures: Review Class and Final Exam
df.loc[counter, "Topics"] = "Review Class"
counter += 1
df.loc[counter, "Topics"] = "Final Exam (7--8.50 pm)"

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

#################################################
# Create latex table
#################################################

# Get the latex lines
lines = latex(df)

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

# Manual adjustment for the following multirow cells to be vertically centered
if sem == "fall":
    bigstruts = [8, 18, 12, 12, 0]
if sem == "spring":
    bigstruts = [8, 18, 12, 4, 6, 0]

# # Adjust rows with module names, also grab module end rows for later
mdlbegs = df[df["Module"] != ""].index
mdlends = [0] * len(mdlbegs)
for i, row in enumerate(mdlbegs):
    mod = df.loc[row, "Module"]
    modkey = [key for key, value in modules.items() if value == mod][0]
    ntops = len(topics[modkey])
    mdlends[i] = mdlbegs[i] + ntops - 1
    row_content = df.loc[row].copy()
    bs = bigstruts[i]
    row_content["Module"] = f"\\multirow{{{ntops}}}[{bs}]{{*}}{{{mod}}}"
    lines[row] = " & ".join([str(x) for x in row_content]) + " \\\\\n"

# Add lines add end of each row and bolder lines at the end of each module
boldlines = list(set(mdlends) | set(mdlbegs[1:] - 1))
for row in range(len(lines)):
    if row not in splrows and row not in boldlines:
        lines[row] += " \\cline{1-2} \\cline{4-6}"
    if row in splrows and row not in boldlines:
        lines[row] += " \\hline"
    if row in boldlines:
        lines[row] += " \\Xhline{1.75\\arrayrulewidth}"

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

# Remove text from Module column

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
