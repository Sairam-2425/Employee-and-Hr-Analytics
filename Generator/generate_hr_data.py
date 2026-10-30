
from pathlib import Path
import pandas as pd
import numpy as np

OUTPUT = Path("data")
OUTPUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)
n = 200
ids = np.arange(1001, 1001 + n)

departments = pd.DataFrame({
    "department_id": [1, 2, 3, 4, 5],
    "department_name": [
        "Engineering", "HR", "Finance",
        "Sales", "Marketing"
    ]
})

dept_names = departments["department_name"].to_numpy()
employee_depts = rng.choice(dept_names, n)
join_dates = pd.to_datetime(
    rng.choice(pd.date_range("2022-01-01", "2026-06-30"), n)
)

employees = pd.DataFrame({
    "employee_id": ids,
    "first_name": [f"Employee{i}" for i in ids],
    "last_name": [f"User{i}" for i in ids],
    "department": employee_depts,
    "salary": rng.integers(30000, 120001, n),
    "hire_date": join_dates.strftime("%Y-%m-%d"),
    "employment_status": rng.choice(
        ["ACTIVE", "ACTIVE", "ACTIVE", "RESIGNED"], n
    ),
    "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
})

attendance = pd.DataFrame({
    "attendance_id": np.arange(1, n + 1),
    "employee_id": ids,
    "attendance_date": "2026-09-01",
    "days_present": rng.integers(15, 23, n),
    "days_absent": rng.integers(0, 5, n)
})

performance = pd.DataFrame({
    "review_id": np.arange(1, n + 1),
    "employee_id": ids,
    "review_date": "2026-09-30",
    "rating": rng.integers(1, 6, n)
})

recruitment = pd.DataFrame({
    "candidate_id": np.arange(5001, 5001 + n),
    "recruitment_source": rng.choice(
        ["LinkedIn", "Referral", "Website", "Campus"], n
    ),
    "application_date": join_dates.strftime("%Y-%m-%d"),
    "hiring_status": rng.choice(
        ["HIRED", "REJECTED", "IN_PROGRESS"], n
    )
})

salary_history = pd.DataFrame({
    "salary_record_id": np.arange(1, n + 1),
    "employee_id": ids,
    "effective_date": join_dates.strftime("%Y-%m-%d"),
    "salary": employees["salary"]
})

files = {
    "employees.csv": employees,
    "departments.csv": departments,
    "attendance.csv": attendance,
    "performance.csv": performance,
    "recruitment.csv": recruitment,
    "salary_history.csv": salary_history
}

for filename, df in files.items():
    df.to_csv(OUTPUT / filename, index=False)
    print(f"Created {OUTPUT / filename}: {len(df)} rows")

print("HR sample data generation completed.")
