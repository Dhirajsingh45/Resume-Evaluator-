import streamlit as st

from utils.file_handler import extract_text
from services.llm_services import extract_candidate
from services.jd_services import extract_job_description
from services.scoring_services import calculate_score


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Evaluator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Evaluator")
st.caption("AI-powered resume and job description alignment analysis")


# ============================================================
# RESUME SECTION
# ============================================================

st.header("1️⃣ Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "jpg", "jpeg", "png"]
)


if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🔍 Analyze Resume"):

        try:

            # Extract text
            with st.spinner("Extracting resume text..."):

                resume_text = extract_text(uploaded_file)

            if not resume_text.strip():

                st.error(
                    "Could not extract text from the resume."
                )

            else:

                # Analyze resume with LLM
                with st.spinner("Analyzing resume with AI..."):

                    candidate = extract_candidate(resume_text)

                # Store candidate in session
                st.session_state["candidate"] = candidate

                # Store raw resume text
                st.session_state["resume_text"] = resume_text

                st.success(
                    "Resume analyzed successfully! ✅"
                )

        except Exception as e:

            st.error(f"Error analyzing resume: {e}")


# ============================================================
# DISPLAY CANDIDATE INFORMATION
# ============================================================

if "candidate" in st.session_state:

    candidate = st.session_state["candidate"]

    st.divider()

    st.header("👤 Candidate Profile")

    # -------------------------
    # Basic Information
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Personal Information")

        st.write("**Name:**", candidate.name)

        st.write("**Email:**", candidate.email)

        st.write("**Phone:**", candidate.phone)

        st.write("**Location:**", candidate.location)

    with col2:

        st.subheader("Skills")

        if candidate.skills:

            for skill in candidate.skills:

                st.write(f"• {skill}")

        else:

            st.write("No skills found.")

    # -------------------------
    # Education
    # -------------------------

    st.subheader("🎓 Education")

    if candidate.education:

        for education in candidate.education:

            st.write(f"• {education}")

    else:

        st.write("No education information found.")

    # -------------------------
    # Experience
    # -------------------------

    st.subheader("💼 Experience")

    if candidate.experience:

        for experience in candidate.experience:

            st.write(f"• {experience}")

    else:

        st.write("No experience information found.")

    # -------------------------
    # Projects
    # -------------------------

    st.subheader("🚀 Projects")

    if candidate.projects:

        for project in candidate.projects:

            st.write(f"• {project}")

    else:

        st.write("No projects found.")

    # -------------------------
    # Certifications
    # -------------------------

    st.subheader("📜 Certifications")

    if candidate.certifications:

        for certification in candidate.certifications:

            st.write(f"• {certification}")

    else:

        st.write("No certifications found.")


# ============================================================
# JOB DESCRIPTION SECTION
# ============================================================

st.divider()

st.header("2️⃣ Job Description")

jd_text = st.text_area(
    "Paste the Job Description",
    height=300,
    placeholder="Paste the complete job description here..."
)


if st.button("📋 Analyze Job Description"):

    if not jd_text.strip():

        st.warning(
            "Please enter a job description first."
        )

    else:

        try:

            with st.spinner(
                "Analyzing job description with AI..."
            ):

                job = extract_job_description(jd_text)

            # Store job in session
            st.session_state["job"] = job

            st.success(
                "Job description analyzed successfully! ✅"
            )

        except Exception as e:

            st.error(
                f"Error analyzing job description: {e}"
            )


# ============================================================
# DISPLAY JOB INFORMATION
# ============================================================

if "job" in st.session_state:

    job = st.session_state["job"]

    st.divider()

    st.header("📋 Structured Job Requirements")

    st.write(
        "**Job Title:**",
        job.job_title
    )

    st.write(
        "**Experience Required:**",
        job.experience_required
    )

    st.subheader("Requirements")

    for requirement in job.requirements:

        st.write(
            f"**{requirement.skill}** — "
            f"{requirement.importance} — "
            f"{requirement.weight}%"
        )


# ============================================================
# MATCHING SECTION
# ============================================================

st.divider()

st.header("3️⃣ Resume ↔ Job Matching")


if st.button("🎯 Calculate JD Alignment"):

    # Check resume
    if "candidate" not in st.session_state:

        st.warning(
            "Please analyze the resume first."
        )

    # Check JD
    elif "job" not in st.session_state:

        st.warning(
            "Please analyze the job description first."
        )

    else:

        try:

            candidate = st.session_state["candidate"]

            job = st.session_state["job"]

            with st.spinner(
                "Comparing resume with job requirements..."
            ):

                result = calculate_score(
                    candidate,
                    job
                )

            # Store result
            st.session_state["result"] = result

            st.success(
                "Matching completed successfully! ✅"
            )

        except Exception as e:

            st.error(
                f"Error calculating alignment: {e}"
            )


# ============================================================
# DISPLAY MATCHING RESULTS
# ============================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.header("📊 JD Alignment Results")

    # -------------------------
    # Overall Score
    # -------------------------

    score = result["score"]

    st.metric(
        label="JD Alignment",
        value=f"{score}%"
    )

    # Progress bar
    st.progress(
        min(score / 100, 1.0)
    )

    # -------------------------
    # Matched Requirements
    # -------------------------

    st.subheader("✅ Matched Requirements")

    if result["matched"]:

        for item in result["matched"]:

            st.write(
                f"**{item['skill']}**"
            )

            st.write(
                f"Weight: {item['weight']}%  |  "
                f"Semantic Similarity: "
                f"{item['similarity']}"
            )

            st.caption(
                f"Evidence: {item['evidence']}"
            )

            st.divider()

    else:

        st.info(
            "No matching requirements found."
        )

    # -------------------------
    # Missing Requirements
    # -------------------------

    st.subheader("❌ Missing / Weak Requirements")

    if result["missing"]:

        for item in result["missing"]:

            st.write(
                f"**{item['skill']}**"
            )

            st.write(
                f"Weight: {item['weight']}%  |  "
                f"Best Similarity: "
                f"{item['similarity']}"
            )

            st.divider()

    else:

        st.success(
            "No missing requirements detected."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Resume Evaluator • "
    "Semantic matching is intended as an explainable "
    "job-description alignment aid, not an automated hiring decision."
)