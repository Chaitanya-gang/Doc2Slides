"""
newd2p - Slide Outline Preview & Human-in-the-loop Generation

This page:
- Takes an uploaded document (or an existing file_id)
- Calls /api/outline to get the narrative JSON from the backend
- Lets the user preview & edit slide titles
- Then calls /api/generate_from_outline to build the PPT from the edited outline
"""

import json

import requests
import streamlit as st

API_URL = "http://localhost:8000"


st.set_page_config(page_title="newd2p - Outline", page_icon="📝", layout="wide")

st.title("📝 Slide Outline Preview")
st.caption("Preview and edit the AI-generated slide structure before building the presentation.")

st.markdown("---")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("1️⃣ Upload or Reference Document")

    uploaded_file = st.file_uploader(
        "Upload a new document (or skip if you already have a File ID)",
        type=["pdf", "docx", "doc", "txt"],
    )

    file_id_input = st.text_input(
        "Existing File ID (optional)",
        help="If you previously uploaded a file from another page, paste the file_id here.",
    )

    if uploaded_file:
        if st.button("📤 Upload & Get File ID"):
            with st.spinner("Uploading document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    upload_resp = requests.post(f"{API_URL}/api/upload", files=files)
                except requests.ConnectionError:
                    st.error("Cannot connect to API. Make sure the FastAPI backend is running.")
                    st.stop()

                data = upload_resp.json()
                if upload_resp.status_code != 200:
                    st.error(f"Upload failed: {data.get('detail', 'Unknown error')}")
                    st.stop()

                st.success(f"Uploaded. File ID: {data['file_id']}")
                st.session_state["outline_file_id"] = data["file_id"]

with col_right:
    st.subheader("2️⃣ Outline Configuration")
    style = st.selectbox(
        "Presentation Style",
        ["ted_talk", "executive_summary", "training", "storytelling", "pitch_deck"],
        format_func=lambda x: x.replace("_", " ").title(),
    )
    slide_count = st.slider("Target number of slides", 6, 15, 8)

st.markdown("---")

file_id = st.session_state.get("outline_file_id") or file_id_input.strip()

if file_id:
    st.info(f"Using File ID: {file_id}")

    if st.button("🧠 Generate Slide Outline (No PPT yet)"):
        with st.spinner("Calling backend to generate outline..."):
            payload = {"file_id": file_id, "style": style, "slide_count": slide_count}
            try:
                resp = requests.post(f"{API_URL}/api/outline", json=payload)
            except requests.ConnectionError:
                st.error("Cannot connect to API. Make sure the FastAPI backend is running.")
                st.stop()

            data = resp.json()
            if resp.status_code != 200:
                st.error(f"Outline generation failed: {data.get('detail', 'Unknown error')}")
                st.stop()

            try:
                narrative_dict = json.loads(data["narrative"])
            except Exception:
                st.error("Backend did not return valid narrative JSON.")
                st.stop()

            st.session_state["outline_file_id"] = file_id
            st.session_state["outline_narrative"] = narrative_dict
            st.session_state["outline_doc_summary"] = data.get("document_summary", "")
            st.success("Outline generated. You can now review and edit slide titles below.")

st.markdown("---")

narrative = st.session_state.get("outline_narrative")
doc_summary = st.session_state.get("outline_doc_summary")

if narrative:
    st.subheader("3️⃣ Edit Slide Titles (Human-in-the-loop)")

    slides = narrative.get("slides", [])
    edited_titles = []

    for slide in slides:
        idx = slide.get("slide_number", len(edited_titles) + 1)
        default_title = slide.get("title", f"Slide {idx}")
        new_title = st.text_input(
            f"Slide {idx} Title",
            value=default_title,
            key=f"slide_title_{idx}",
        )
        slide["title"] = new_title
        edited_titles.append(new_title)

    st.markdown("---")
    st.subheader("4️⃣ Build PPT from Edited Outline")

    theme = st.selectbox(
        "Theme",
        ["vibrant", "ocean", "sunset", "forest", "royal"],
        index=0,
        key="outline_theme",
    )
    image_mode = st.checkbox("Generate Illustrative Images", value=False, key="outline_image_mode")
    diagram_mode = st.checkbox("Enable Diagram Hints from Slides", value=True, key="outline_diagram_mode")

    export_pdf = st.checkbox("Also export PDF", value=False, key="outline_export_pdf")
    export_markdown = st.checkbox("Also export Markdown", value=False, key="outline_export_md")

    if st.button("🚀 Generate Presentation from Outline", type="primary"):
        export_formats = []
        if export_pdf:
            export_formats.append("pdf")
        if export_markdown:
            export_formats.append("markdown")

        payload = {
            "file_id": file_id,
            "theme": theme,
            "image_mode": image_mode,
            "diagram_mode": diagram_mode,
            "include_speaker_notes": True,
            "export_formats": export_formats or None,
            "narrative_json": narrative,
            "doc_summary": doc_summary or "",
        }

        with st.spinner("Building PPT and exports from edited outline..."):
            try:
                resp = requests.post(f"{API_URL}/api/generate_from_outline", json=payload)
            except requests.ConnectionError:
                st.error("Cannot connect to API. Make sure the FastAPI backend is running.")
                st.stop()

            data = resp.json()
            if resp.status_code != 200:
                st.error(f"Generation failed: {data.get('detail', 'Unknown error')}")
                st.stop()

        st.success("Presentation generated from your edited outline!")

        st.markdown("### 📥 Download")
        dcol1, dcol2 = st.columns(2)

        with dcol1:
            ppt_resp = requests.get(f"{API_URL}/api/download/ppt/{file_id}")
            if ppt_resp.status_code == 200:
                st.download_button(
                    "📊 Download PPT",
                    data=ppt_resp.content,
                    file_name=f"{file_id}_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                )

        with dcol2:
            json_resp = requests.get(f"{API_URL}/api/download/json/{file_id}")
            if json_resp.status_code == 200:
                st.download_button(
                    "📋 Download JSON",
                    data=json_resp.content,
                    file_name=f"{file_id}_handover.json",
                    mime="application/json",
                    use_container_width=True,
                )

