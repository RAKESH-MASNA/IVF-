import pandas as pd

df = pd.read_csv(r"C:\Users\HP\Downloads\Dataset (4)\ivf_equipment_utilization_2yrs.csv")

#FIRST MOMENT BUSINESS DECISION
#MEAN,MEDIAN,MODE

for col in df.select_dtypes(include='number').columns:
    mean_val = df[col].mean()
    median_val = df[col].median()
    mode_val = df[col].mode()[0] if not df[col].mode().empty else "No Mode"
    print(f"{col} → \n Mean: {mean_val},\n Median: {median_val},\n Mode: {mode_val}")
   

#SECOND MOMENT BUSINESS DECISION
#VARIANCE,STANDARD DEVIATION,RANGE
 
for col in df.select_dtypes(include='number').columns:
    variance_val = df[col].var()
    range_val = df[col].max() - df[col].min()         
    std_dev_val = df[col].std()
    print(f"{col} → \n Variance: {variance_val:.2f},\n Std Dev: {std_dev_val:.2f},\n Range: {range_val:.2f}")

#THIRD MOMENT BUSINESS DECISION
#SKEWNESS
for col in df.select_dtypes(include='number').columns:
    skew_val = df[col].var()
    print(f"{col} → \n Skewness: { skew_val:.2f}")

#FOURTH MOMENT BUSINESS DECISION
#KURTOSIS
for col in df.select_dtypes(include='number').columns:
    kurt_val = df[col].kurt()
    print(f"{col} → \n Kurtosis: {kurt_val:.2f}")
    
    
#GRAPHICAL REPRESENTATION 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
   
#So your plots should answer only these questions:
# How much is each equipment used?
#Which equipment is underused?
#How usage changes with time?

#UNIVARIATE
#BAR PLOT
# How much is each equipment used?

df['equipment_type'].value_counts().plot(kind='bar',color = 'orange')
plt.title("Count of Equipment Types")
plt.xlabel("Equipment Type")
plt.ylabel("Count")
plt.show()

#HISTOGRAM
#Which equipment is underused?

plt.hist(df['utilization_pct'],bins = 20,color = 'orange')
plt.title("Distribution of Utilization Percentage")
plt.xlabel("Utilization Percentage")
plt.ylabel("Frequency")
plt.show()

#BIVARIATE
#SCATTERPLOT
plt.scatter(df['utilization_hrs'], df['idle_hrs'],color = 'green')
plt.title("Utilization hrs vs Idle hrs")
plt.xlabel("Utilization hrs")

plt.show()


#MULTIVARIATE
#PAIRPLOT
cols = [
    'utilization_hrs',
    'idle_hrs',
    'utilization_pct',
    'technical_downtime_hrs'
]
sns.pairplot(df[cols],plot_kws={'color':'orange'})
plt.show()

#SWEERVIZ
import sweetviz as sv
report = sv.analyze(df)
report.show_html()

#AUTOVIZ
from autoviz.AutoViz_Class import AutoViz_Class
av = AutoViz_Class()
av.AutoViz(df)

#D-TALE
import dtale
d = dtale.show(df)
d.open_browser()


#PANDAS PROFILING
from ydata_profiling import ProfileReport
profile = ProfileReport(df)
profile.to_file("report.html")

df.describe()
df.shape
df.info()


df2 = pd.read_csv(r"C:\Users\HP\Downloads\Dataset (4)\ivf_equipment_master.csv")
#**************DATA CLEANING********************
# TYPE CASTING

# Strip spaces
df = df.apply(
    lambda col: col.str.strip() if col.dtype == 'object' else col
)

# Date
df['date'] = pd.to_datetime(df['date'])

# Categorical columns
cat_cols = [
    'lab_id', 'equipment_id', 'equipment_type',
    'primary_procedure'
]

for col in cat_cols:
    df[col] = df[col].astype('category')

# Boolean
df['redundancy_available'] = (
    df['redundancy_available'].astype(bool)
)

# Integer columns
int_cols = ['max_capacity_hrs', 'workflow_delay_events', 'total_cases_day_lab']
df[int_cols] = df[int_cols].astype(int)

# Float columns
float_cols = [
    'utilization_hrs', 'utilization_pct', 'idle_hrs',
    'technical_downtime_hrs', 'planned_maintenance_hrs',
    'avg_delay_minutes'
]
df[float_cols] = df[float_cols].astype(float)

print(df.info())


# DROP NULL VALUES

#checking null values
df.isnull().sum()
df2.isnull().sum()

#Check NULLs before
df["date"].isnull().sum()

#Drop NULL dates (your line)
df = df.dropna(subset=["date"])


#Confirm NULLs are gone
df["date"].isnull().sum()
df2["date"].isnull().sum()

#Now lets check shape of dataset
df.shape
df2.shape

# HANDLING DUPLICATES

#count of duplicates
df.duplicated().sum()
df2.duplicated().sum()

#View duplicate rows
df[df.duplicated()]
df2[df.duplicated()]

#Drop duplicates rows 
df = df.drop_duplicates()
df2 = df2.drop_duplicates()

#After remove duplicates once check the data set shape
df.shape
df2.shape



#For all numerical columns

numeric_cols = df.select_dtypes(include="number").columns
#APPLY WINSORIZATION (IQR-BASED) TO ALL NUMERIC COLUMNS

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[col] = df[col].clip(lower, upper)


#BOXPLOT AFTER WINSORIZATION
plt.figure(figsize=(14, 7))
df[numeric_cols].boxplot()
plt.title("Box Plots for All Numeric Columns (After Winsorization)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#INDIVIDUAL BOXPLOTS
for col in numeric_cols:
    plt.figure(figsize=(6, 4))
    plt.boxplot(df[col].dropna())
    plt.title(f"Box Plot of {col} (After Winsorization)")
    plt.ylabel(col)
    plt.tight_layout()
    plt.show()


#*************AFTER CLEANING MOMENTS *********************
#FIRST MOMENT BUSINESS DECISION
#MEAN,MEDIAN,MODE

for col in df.select_dtypes(include='number').columns:
    mean_val = df[col].mean()
    median_val = df[col].median()
    mode_val = df[col].mode()[0] if not df[col].mode().empty else "No Mode"
    print(f"{col} → \n Mean: {mean_val},\n Median: {median_val},\n Mode: {mode_val}")
   

#SECOND MOMENT BUSINESS DECISION
#VARIANCE,STANDARD DEVIATION,RANGE
 
for col in df.select_dtypes(include='number').columns:
    variance_val = df[col].var()
    range_val = df[col].max() - df[col].min()         
    std_dev_val = df[col].std()
    print(f"{col} → \n Variance: {variance_val:.2f},\n Std Dev: {std_dev_val:.2f},\n Range: {range_val:.2f}")

#THIRD MOMENT BUSINESS DECISION
#SKEWNESS
for col in df.select_dtypes(include='number').columns:
    skew_val = df[col].var()
    print(f"{col} → \n Skewness: { skew_val:.2f}")

#FOURTH MOMENT BUSINESS DECISION
#KURTOSIS
for col in df.select_dtypes(include='number').columns:
    kurt_val = df[col].kurt()
    print(f"{col} → \n Kurtosis: {kurt_val:.2f}")
    

#Box plot for all numerical columns
for col in df.select_dtypes(include='number').columns:
    plt.figure()
    plt.boxplot(df[col])
    plt.title(f"Box Plot of {col}")
    plt.ylabel(col)
    plt.show()

#D-TALE
import dtale
dtale.show(df)

import dtale

dtale.show(df)
import dtale
dtale.show(df, open_browser=True)


df.to_csv("ivf_equipment_utilization_cleaned.csv", index=False)
import os
os.getcwd()

df.to_csv(
    r"C:\Users\HP\Downloads\ivf_equipment_utilization_cleaned.csv",
    index=False
)


#*************UNI VARIANT PLOTS*******************
#*************BOX PLOT***********

#Box plot without colour
import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
plt.boxplot(df["utilization_pct"].dropna())
plt.ylabel("Utilization Percentage")
plt.title("Box Plot of Utilization Percentage")
plt.show()

#Box plot with filled colour 
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["utilization_pct"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("Utilization Percentage")
plt.title("Box Plot of Utilization Percentage")
plt.show()

#max_capacity_hrs
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["max_capacity_hrs"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("Max Capacity hrs")
plt.title("Box Plot of Max Capacity hrs")
plt.show()



#utilization_hrs
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["utilization_hrs"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("utilization_hrs")
plt.title("Box Plot of Utilization_hrs")
plt.show()



#idle_hrs
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["idle_hrs"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("idle_hrs")
plt.title("Box Plot of Idle_hrs")
plt.show()

#techical_downtime_hrs
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["technical_downtime_hrs"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("technical_downtime_hrs")
plt.title("Box Plot of technical_downtime_hrs")
plt.show()


#planned_maintenance_hrs
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["planned_maintenance_hrs"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("planned_maintenance_hrs")
plt.title("Box Plot of planned_maintenance_hrs")
plt.show()



#workflow_delay_events 
plt.figure(figsize=(6, 4))

plt.boxplot(
    df["workflow_delay_events"].dropna(),
    patch_artist=True,# enables fill color
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("workflow_delay_events ")
plt.title("Box Plot of workflow_delay_events")
plt.show()


#avg_delay_minutes  
plt.figure(figsize=(6,4))

plt.boxplot(
    df["avg_delay_minutes"].dropna(),
    patch_artist=True,
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red")
)

plt.title("Box Plot of Average Delay Minutes")
plt.ylabel("Minutes")
plt.show()


#total_cases_day_lab 
plt.figure(figsize=(6,4))

plt.boxplot(
    df["total_cases_day_lab"].dropna(),
    patch_artist=True,
    boxprops=dict(facecolor="skyblue"),
    medianprops=dict(color="red")
)

plt.title("Box Plot of total_cases_day_lab")
plt.ylabel("total_cases_day_lab")
plt.show()
#*******************************


#************BIVARIANT PLOTS*************

#************SCATTERPLOT********
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

scatter_pairs = [
    ("max_capacity_hrs", "utilization_hrs"),
    ("utilization_hrs", "total_cases_day_lab"),
    ("utilization_hrs", "utilization_pct"),
    ("utilization_hrs", "idle_hrs"),
    ("idle_hrs", "technical_downtime_hrs"),
    ("technical_downtime_hrs", "planned_maintenance_hrs"),
    ("workflow_delay_events", "avg_delay_minutes"),
    ("avg_delay_minutes", "workflow_delay_events"),
    ("utilization_hrs", "total_cases_day_lab")
]

for x, y in scatter_pairs:
    plt.figure(figsize=(6,4))
    plt.scatter(df[x], df[y], alpha=0.6)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{y} vs {x}")
    plt.grid(True)
    plt.show()
#********************************* 
    
a#*****************MULTIVARIANT PLOTS***********8

#max_capacity_hrs (Capacity vs Usage & Workload)

plt.figure(figsize=(6,4))
plt.scatter(df["utilization_hrs"], df["total_cases_day_lab"],
            c=df["max_capacity_hrs"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Total Cases per Day")
plt.title("Capacity vs Utilization & Workload")
plt.colorbar(label="Max Capacity Hours")
plt.show()


#utilization_hrs (Usage vs Workload & Idle)

plt.figure(figsize=(6,4))
plt.scatter(df["utilization_hrs"], df["total_cases_day_lab"],
            c=df["idle_hrs"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Total Cases per Day")
plt.title("Utilization vs Workload & Idle Time")
plt.colorbar(label="Idle Hours")
plt.show()


#utilization_pct (Efficiency vs Usage & Idle)

plt.figure(figsize=(6,4))
plt.scatter(df["utilization_hrs"], df["idle_hrs"],
            c=df["utilization_pct"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Idle Hours")
plt.title("Efficiency vs Usage & Idle Time")
plt.colorbar(label="Utilization Percentage")
plt.show()


#idle_hrs (Idle vs Usage & Downtime)

plt.figure(figsize=(6,4))
plt.scatter(df["utilization_hrs"], df["idle_hrs"],
            c=df["technical_downtime_hrs"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Idle Hours")
plt.title("Idle Time vs Usage & Downtime")
plt.colorbar(label="Technical Downtime Hours")
plt.show()


#technical_downtime_hrs (Downtime vs Idle & Maintenance)
plt.figure(figsize=(6,4))
plt.scatter(df["idle_hrs"], df["technical_downtime_hrs"],
            c=df["planned_maintenance_hrs"], alpha=0.6)
plt.xlabel("Idle Hours")
plt.ylabel("Technical Downtime Hours")
plt.title("Downtime vs Idle & Maintenance")
plt.colorbar(label="Planned Maintenance Hours")
plt.show()


#planned_maintenance_hrs (Maintenance vs Downtime & Idle)

plt.figure(figsize=(6,4))
plt.scatter(df["technical_downtime_hrs"], df["idle_hrs"],
            c=df["planned_maintenance_hrs"], alpha=0.6)
plt.xlabel("Technical Downtime Hours")
plt.ylabel("Idle Hours")
plt.title("Maintenance Impact on Downtime & Idle")
plt.colorbar(label="Planned Maintenance Hours")
plt.show()

#workflow_delay_events (Delays vs Delay Time & Usage)

plt.figure(figsize=(6,4))
plt.scatter(df["workflow_delay_events"], df["avg_delay_minutes"],
            c=df["utilization_hrs"], alpha=0.6)
plt.xlabel("Workflow Delay Events")
plt.ylabel("Average Delay Minutes")
plt.title("Workflow Delays vs Delay Duration & Usage")
plt.colorbar(label="Utilization Hours")
plt.show()

#avg_delay_minutes (Delay Time vs Events & Idle)

plt.figure(figsize=(6,4))
plt.scatter(df["workflow_delay_events"], df["avg_delay_minutes"],
            c=df["idle_hrs"], alpha=0.6)
plt.xlabel("Workflow Delay Events")
plt.ylabel("Average Delay Minutes")
plt.title("Delay Duration vs Events & Idle Time")
plt.colorbar(label="Idle Hours")
plt.show()


#total_cases_day_lab (Workload vs Usage & Efficiency)

plt.figure(figsize=(6,4))
plt.scatter(df["utilization_hrs"], df["total_cases_day_lab"],
            c=df["utilization_pct"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Total Cases per Day")
plt.title("Workload vs Usage & Efficiency")
plt.colorbar(label="Utilization Percentage")
plt.show()






