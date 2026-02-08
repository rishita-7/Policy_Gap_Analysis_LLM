import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------- Session State Initialization ----------------
if "file_history" not in st.session_state:
    st.session_state.file_history = {}

if "selected_file_name" not in st.session_state:
    st.session_state.selected_file_name = None

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Cybersecurity Policy Gap Analyzer",
    layout="wide"
)

# ---------------- Header ----------------
st.title("Cybersecurity Policy Gap Analyzer")
st.caption("Offline AI-powered dashboard for cybersecurity policy gap analysis")


# ---------------- Sidebar ----------------
st.sidebar.title("Analysis Settings")

# Framework selection
framework = st.sidebar.selectbox(
    "Security Framework",
    ["NIST", "CIS Controls v8"]
)

st.sidebar.markdown("---")
# Controls
if st.sidebar.button("Reset Analysis"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")

# Analysis mode
st.sidebar.markdown("### Analysis Mode")
analysis_mode = st.sidebar.radio(
    "Select analysis depth",
    ["Quick Scan", "Standard Analysis", "Deep Compliance Review"]
)

st.sidebar.markdown("---")
# Risk sensitivity
st.sidebar.markdown("### Risk Sensitivity")
risk_sensitivity = st.sidebar.slider(
    "Detection strictness",
    min_value=1,
    max_value=5,
    value=3
)

st.sidebar.markdown("---")

# Platform capabilities
st.sidebar.markdown("### Platform Capabilities")
st.sidebar.markdown(
    """
    - Fully offline processing  
    - Local LLM-based analysis  
    - No cloud dependency  
    - No external API usage  
    """
)

st.sidebar.markdown("---")

# Model information
st.sidebar.markdown("### Model Information")
st.sidebar.markdown(
    """
    Model type: Local Large Language Model  
    Inference mode: Offline  
    Execution: CPU-based  
    """
)

st.sidebar.markdown("---")

# Analysis metadata
st.sidebar.markdown("### Analysis Metadata")
st.sidebar.markdown(
    """
    Input: Policy document (PDF, DOCX, TXT)  
    Estimated runtime: ~5 seconds  
    Output: Dashboard + CSV report  
    """
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Uploaded Document History")
if st.session_state.file_history:
    for i, name in enumerate(st.session_state.file_history.keys(), start=1):
        st.sidebar.write(f"{i}. {name}")
else:
    st.sidebar.write("No documents uploaded in this session.")



# ---------------- File Upload ----------------
uploaded_file = st.file_uploader(
    "Upload Policy Document",
    type=["pdf", "txt", "docx"]
)

if uploaded_file is not None:
    st.session_state.file_history[uploaded_file.name] = uploaded_file
    st.session_state.selected_file_name = uploaded_file.name

st.markdown("### Previously Uploaded Documents")

if st.session_state.file_history:
    st.session_state.selected_file_name = st.selectbox(
        "Select a document to analyze",
        options=list(st.session_state.file_history.keys()),
        index=list(st.session_state.file_history.keys()).index(
            st.session_state.selected_file_name
        ) if st.session_state.selected_file_name else 0
    )
else:
    st.info("No documents uploaded in this session.")


# ---------------- History Selection (Main Screen) ----------------
st.markdown("### Uploaded Documents (Session History)")

analyze = st.button("Analyze Policy")

if analyze and not st.session_state.selected_file_name:
    st.warning("Please upload or select a policy document to proceed.")

# ---------------- Dummy Backend Output ----------------
result = {
    "summary": {
        "policy_name": "Information Security Policy",
        "framework": framework,
        "compliance_score": 0
    },
    "gaps": {
        "missing": [
            "Multi-factor authentication not defined",
            "Incident response testing not documented"
        ],
        "weak": [
            "Access control policy lacks role definitions"
        ],
        "covered": [
            "Password policy defined",
            "User account lifecycle management"
        ]
    },
    "suggestions": [
        "Implement multi-factor authentication for privileged accounts",
        "Conduct incident response simulations annually"
    ]
}

# ---------------- Dynamic Compliance Calculation ----------------

# Base compliance (from gaps)
total_controls = (
    len(result["gaps"]["missing"]) +
    len(result["gaps"]["weak"]) +
    len(result["gaps"]["covered"])
)

if total_controls > 0:
    compliance_score = (
        len(result["gaps"]["covered"]) / total_controls
    ) * 100
else:
    compliance_score = 0

# ---------------- Analysis Mode Adjustment ----------------
# Quick = lenient, Deep = strict
if analysis_mode == "Quick Scan":
    analysis_factor = 0.9
elif analysis_mode == "Standard Analysis":
    analysis_factor = 1.0
else:  # Deep Compliance Review
    analysis_factor = 1.2

compliance_score = compliance_score / analysis_factor

# ---------------- Risk Sensitivity Adjustment ----------------
# Sensitivity range: 1 (low) → 5 (high)
risk_penalty = (risk_sensitivity - 3) * 5
compliance_score = compliance_score - risk_penalty

# ---------------- Final Normalization ----------------
compliance_score = round(max(0, min(100, compliance_score)))

result["summary"]["compliance_score"] = compliance_score


# ---------------- Main Dashboard ----------------
if analyze and uploaded_file:

    with st.spinner("Analyzing policy using offline AI model..."):
        pass

    st.success("Policy analysis completed successfully.")
    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["Overview", "Gap Analysis", "Recommendations"]
    )

    # ================= TAB 1: OVERVIEW =================
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Policy Name", result["summary"]["policy_name"])
        col2.metric("Framework", result["summary"]["framework"])
        col3.metric("Compliance Score", f"{result['summary']['compliance_score']}%")

        st.markdown("### Compliance Level")
        st.progress(result["summary"]["compliance_score"] / 100)

        st.markdown("### Executive Summary")
        score = result["summary"]["compliance_score"]
        risk_level = (
            "High Risk" if score < 50
            else "Moderate Risk" if score < 80
            else "Low Risk"
        )

        st.info(
            f"The policy demonstrates a {risk_level} security posture against "
            f"the {framework} framework. Key gaps exist in authentication and "
            "incident response, increasing compliance and operational risk."
        )

        st.markdown("### Security Maturity Model")
        maturity = pd.DataFrame({
            "Domain": [
                "Access Control",
                "Incident Response",
                "Risk Management",
                "Data Protection",
                "Asset Management"
            ],
            "Maturity Level": [
                "Initial",
                "Initial",
                "Defined",
                "Managed",
                "Defined"
            ]
        })
        st.dataframe(maturity, use_container_width=True)

        st.markdown("### Framework Coverage Mapping")
        framework_map = pd.DataFrame({
            "Framework Function": [
                "Identify", "Protect", "Detect", "Respond", "Recover"
            ],
            "Coverage (%)": [70, 65, 60, 40, 30]
        })

        st.plotly_chart(
            px.line(
                framework_map,
                x="Framework Function",
                y="Coverage (%)",
                markers=True
            ),
            use_container_width=True
        )

   # ================= TAB 2: GAP ANALYSIS =================
    with tab2:
        gap_df = pd.DataFrame({
            "Category": ["Missing", "Weak", "Covered"],
            "Count": [
                len(result["gaps"]["missing"]),
                len(result["gaps"]["weak"]),
                len(result["gaps"]["covered"])
            ]
        })

        col1, col2 = st.columns(2)

        # -------- Pie Chart (Colored) --------
        col1.plotly_chart(
            px.pie(
                gap_df,
                values="Count",
                names="Category",
                color="Category",
                color_discrete_map={
                    "Missing": "#C01E1E",   # red
                    "Weak": "#0A909F",      # orange
                    "Covered": "#1BB01B"    # green
                }
            ),
            use_container_width=True
        )

        # -------- Bar Chart (Colored) --------
        col2.plotly_chart(
            px.bar(
                gap_df,
                x="Category",
                y="Count",
                text="Count",
                color="Category",
                color_discrete_map={
                    "Missing": "#940606",
                    "Weak": "#DBB80B",
                    "Covered": "#2ca02c"
                }
            ),
            use_container_width=True
        )

        # -------- Domain-wise Gap Distribution --------
        st.markdown("### Domain-wise Gap Distribution")

        domain_data = pd.DataFrame({
            "Domain": [
                "Access Control",
                "Incident Response",
                "Risk Management",
                "Data Protection",
                "Asset Management"
            ],
            "Missing Controls": [2, 2, 1, 0, 1],
            "Weak Controls": [1, 1, 0, 1, 0]
        })

        st.plotly_chart(
            px.bar(
                domain_data,
                x="Domain",
                y=["Missing Controls", "Weak Controls"],
                barmode="group",
                color_discrete_sequence=["#210090", "#b01e04"]
            ),
            use_container_width=True
        )

        # -------- Risk Heatmap --------
        st.markdown("### Risk Heatmap by Domain")

        heatmap_data = pd.DataFrame({
            "Domain": domain_data["Domain"],
            "Risk Score": [90, 85, 60, 40, 55]
        })

        st.plotly_chart(
            px.imshow(
                heatmap_data.set_index("Domain"),
                color_continuous_scale=["#2ca02c", "#ffbf00", "#d62728"]
            ),
            use_container_width=True
        )

        # -------- Control-Level Mapping --------
        st.markdown("### Control-Level Mapping")

        control_map = pd.DataFrame({
            "Control ID": ["PR.AC-1", "PR.AC-7", "IR-4", "ID.RA-1"],
            "Description": [
                "Identities and credentials managed",
                "User authentication enforced",
                "Incident response executed",
                "Risk assessment conducted"
            ],
            "Status": ["Missing", "Weak", "Missing", "Covered"]
        })

        st.dataframe(control_map, use_container_width=True)


     # ================= TAB 3: RECOMMENDATIONS =================
    with tab3:
        st.subheader("AI-Generated Recommendations")
        for rec in result["suggestions"]:
            st.success(rec)

        st.markdown("### Before vs After Policy Comparison")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Original Policy")
            st.markdown(
                """
                - Access is provided to authorized users.
                - Authentication relies only on passwords.
                - No role-based access control is defined.
                - No multi-factor authentication requirement.
                """
            )

        with col2:
            st.markdown("#### AI-Improved Policy")
            st.markdown(
                """
                - Access is enforced using role-based access control (RBAC).
                - Multi-factor authentication is mandatory for privileged and remote access.
                - Passwords must meet defined complexity and rotation standards.
                - Access rights are reviewed periodically.
                """
            )


        st.markdown("### Audit Checklist")
        checklist = pd.DataFrame({
            "Item": [
                "MFA implemented",
                "Incident response plan documented",
                "Incident response drills conducted",
                "RBAC enforced",
                "Encryption policy defined"
            ],
            "Status": ["No❌", "No❌", "No❌", "Partial⚠️", "Yes✅"]
        })
        st.table(checklist)

        st.markdown("### Remediation Roadmap")
        roadmap = pd.DataFrame({
            "Phase": ["Phase 1", "Phase 2", "Phase 3"],
            "Focus": [
                "Critical security gaps",
                "Medium risk controls",
                "Policy optimization"
            ],
            "Timeline": [
                "0–30 Days",
                "31–60 Days",
                "61–90 Days"
            ]
        })
        st.table(roadmap)

        st.markdown("### Explanation of Identified Gaps")
        st.info(
            "Gaps were identified because the policy lacks explicit requirements "
            "for multi-factor authentication, incident response testing, and "
            "role-based access control when evaluated against framework standards."
        )

        st.markdown("### Compliance Verdict")
        if score >= 80:
            st.success("The policy is largely compliant.")
        elif score >= 50:
            st.warning("The policy is partially compliant and requires improvements.")
        else:
            st.error("The policy is non-compliant and requires immediate remediation.")

        # ---------------- FIXED DOWNLOAD SECTION ----------------
        gap_rows = []
        for gap_type, controls in result["gaps"].items():
            for control in controls:
                gap_rows.append({
                    "Gap Type": gap_type.capitalize(),
                    "Control Description": control
                })

        gap_report_df = pd.DataFrame(gap_rows)

        st.download_button(
            "Download Gap Report (CSV)",
            gap_report_df.to_csv(index=False),
            "policy_gap_report.csv",
            "text/csv"
        )
