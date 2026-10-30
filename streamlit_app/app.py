
import logging

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
)

st.title("Employee and HR Analytics Dashboard")
st.caption("Snowflake-powered HR reporting")


@st.cache_data(ttl=60)
def load_data(query: str) -> pd.DataFrame:
    connection = st.connection("snowflake")
    return connection.query(query, ttl=60)


try:
    headcount = load_data("""
        SELECT DEPARTMENT, EMPLOYEE_COUNT
        FROM HR_ANALYTICS_DB.REPORTING.VW_DEPARTMENT_HEADCOUNT
        ORDER BY DEPARTMENT
    """)

    salary = load_data("""
        SELECT DEPARTMENT, AVG_SALARY, MIN_SALARY, MAX_SALARY
        FROM HR_ANALYTICS_DB.REPORTING.VW_DEPARTMENT_SALARY
        ORDER BY DEPARTMENT
    """)

    hiring = load_data("""
        SELECT HIRE_MONTH, HIRES
        FROM HR_ANALYTICS_DB.REPORTING.VW_MONTHLY_HIRING
        ORDER BY HIRE_MONTH
    """)

    # Normalize column names returned by Snowflake.
    for df in (headcount, salary, hiring):
        df.columns = df.columns.str.upper()

    total_employees = (
        int(headcount["EMPLOYEE_COUNT"].fillna(0).sum())
        if not headcount.empty else 0
    )

    department_count = (
        int(headcount["DEPARTMENT"].nunique())
        if not headcount.empty else 0
    )

    average_salary = (
        float(salary["AVG_SALARY"].mean())
        if not salary.empty else 0.0
    )

    total_hires = (
        int(hiring["HIRES"].fillna(0).sum())
        if not hiring.empty else 0
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Employees", f"{total_employees:,}")
    c2.metric("Departments", f"{department_count:,}")
    c3.metric("Average Department Salary", f"{average_salary:,.2f}")
    c4.metric("Total Hires in Dataset", f"{total_hires:,}")

    st.subheader("Department-wise Headcount")

    if not headcount.empty:
        fig = px.bar(
            headcount,
            x="DEPARTMENT",
            y="EMPLOYEE_COUNT",
            color="DEPARTMENT",
            title="Active Employees by Department",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No department headcount data is available.")

    st.subheader("Average Salary by Department")

    if not salary.empty:
        fig = px.bar(
            salary,
            x="DEPARTMENT",
            y="AVG_SALARY",
            title="Average Salary by Department",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No salary data is available.")

    st.subheader("Monthly Hiring Trends")

    if not hiring.empty:
        fig = px.line(
            hiring,
            x="HIRE_MONTH",
            y="HIRES",
            markers=True,
            title="Employees Hired by Month",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No monthly hiring data is available.")

    with st.expander("View report data"):
        st.write("Department headcount")
        st.dataframe(headcount, use_container_width=True)

        st.write("Salary report")
        st.dataframe(salary, use_container_width=True)

        st.write("Monthly hiring")
        st.dataframe(hiring, use_container_width=True)

except Exception as exc:
    logging.exception("Failed to load HR dashboard data")

    st.error(
        "Unable to load dashboard data. Check the Snowflake "
        "connection, permissions, reporting views, and SQL queries."
    )

    # Show the actual error while troubleshooting locally.
    with st.expander("Technical details"):
        st.code(f"{type(exc).__name__}: {exc}")
