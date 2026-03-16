"""
Enhanced Streamlit frontend for newd2p.
"""

import json
from typing import Dict, List

import requests
import streamlit as st

from frontend.api_client import (
    download_file,
    generate_outline,
    generate_presentation,
    get_styles_metadata,
    upload_document,
)
from frontend.config import DEFAULT_SLIDE_COUNT, DEFAULT_STYLE, DEFAULT_THEME, PIPELINE_STEPS, THEME_PRESETS


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4efe7;
            --panel: rgba(255,255,255,0.82);
            --panel-strong: rgba(255,255,255,0.94);
            --text: #182126;
            --muted: #5e6a70;
            --line: rgba(24,33,38,0.08);
            --accent: #d96c3f;
            --accent-soft: #f6cbb8;
            --accent-2: #206a5d;
        }
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(217,108,63,0.18), transparent 28%),
                radial-gradient(circle at bottom left, rgba(32,106,93,0.16), transparent 32%),
                linear-gradient(180deg, #fbf7f2 0%, #f4efe7 100%);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 1.6rem;
            padding-bottom: 2.4rem;
        }
        .hero-card, .panel-card, .mini-card, .status-card, .preview-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 22px;
            box-shadow: 0 18px 60px rgba(58, 48, 36, 0.08);
            backdrop-filter: blur(14px);
        }
        .hero-card {
            padding: 1.6rem 1.8rem;
            margin-bottom: 1rem;
        }
        .hero-kicker {
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent-2);
            font-weight: 700;
            font-size: 0.76rem;
        }
        .hero-title {
            font-size: 2.4rem;
            line-height: 1.05;
            font-weight: 800;
            color: var(--text);
            margin: 0.4rem 0 0.55rem 0;
        }
        .hero-copy {
            color: var(--muted);
            font-size: 1.02rem;
            max-width: 50rem;
        }
        .hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 1rem;
        }
        .mini-card {
            padding: 0.85rem 1rem;
        }
        .mini-label {
            color: var(--muted);
            font-size: 0.82rem;
            margin-bottom: 0.2rem;
        }
        .mini-value {
            color: var(--text);
            font-size: 1rem;
            font-weight: 700;
        }
        .preset-card {
            border: 1px solid var(--line);
            background: var(--panel-strong);
            border-radius: 16px;
            padding: 0.85rem 0.95rem;
            min-height: 110px;
        }
        .preset-title {
            font-weight: 700;
            color: var(--text);
        }
        .preset-copy {
            color: var(--muted);
            font-size: 0.86rem;
            margin-top: 0.25rem;
        }
        .status-card, .preview-card, .panel-card {
            padding: 1rem 1.1rem;
            margin-bottom: 0.8rem;
        }
        .status-step {
            padding: 0.55rem 0.7rem;
            border-radius: 14px;
            margin-bottom: 0.45rem;
            background: rgba(255,255,255,0.7);
            border: 1px solid var(--line);
            color: var(--muted);
        }
        .status-step.active {
            background: linear-gradient(135deg, rgba(217,108,63,0.12), rgba(32,106,93,0.10));
            color: var(--text);
            border-color: rgba(217,108,63,0.24);
            font-weight: 700;
        }
        .preview-card h4 {
            margin: 0 0 0.3rem 0;
            color: var(--text);
        }
        .preview-card p {
            margin: 0;
            color: var(--muted);
            font-size: 0.93rem;
        }
        .download-strip {
            padding: 0.9rem 1rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(249,243,235,0.94));
            border: 1px solid var(--line);
            margin-bottom: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_state() -> None:
    defaults = {
        "uploaded_file_id": None,
        "uploaded_filename": None,
        "outline_data": None,
        "generation_result": None,
        "selected_preset": "Academic",
        "current_stage": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">AI Document to Presentation</div>
            <div class="hero-title">Turn dense documents into polished, presenter-ready slides.</div>
            <div class="hero-copy">
                Upload your report, preview the slide flow, and generate a themed PowerPoint with
                Ollama support, speaker notes, and optional exports.
            </div>
            <div class="hero-grid">
                <div class="mini-card">
                    <div class="mini-label">Input Formats</div>
                    <div class="mini-value">PDF, DOCX, TXT</div>
                </div>
                <div class="mini-card">
                    <div class="mini-label">Generation Path</div>
                    <div class="mini-value">Ollama + local fallback</div>
                </div>
                <div class="mini-card">
                    <div class="mini-label">Output</div>
                    <div class="mini-value">PPTX, PDF, Markdown</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_panel(active_index: int) -> None:
    st.markdown('<div class="status-card"><h4 style="margin-top:0;">Pipeline Status</h4>', unsafe_allow_html=True)
    for index, step in enumerate(PIPELINE_STEPS):
        active_class = "active" if index <= active_index else ""
        st.markdown(
            f'<div class="status-step {active_class}">{index + 1}. {step}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_presets() -> None:
    st.markdown('<div class="panel-card"><h4 style="margin-top:0;">Quick Presentation Presets</h4>', unsafe_allow_html=True)
    columns = st.columns(len(THEME_PRESETS))
    for column, (name, preset) in zip(columns, THEME_PRESETS.items()):
        with column:
            st.markdown(
                f"""
                <div class="preset-card">
                    <div class="preset-title">{name}</div>
                    <div class="preset-copy">{preset["description"]}</div>
                    <div class="preset-copy" style="margin-top:0.5rem;">
                        Theme: {preset["theme"]}<br/>Style: {preset["style"]}<br/>Slides: {preset["slides"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Use {name}", key=f"preset_{name}", use_container_width=True):
                st.session_state["selected_preset"] = name
                st.session_state["preset_theme"] = preset["theme"]
                st.session_state["preset_style"] = preset["style"]
                st.session_state["preset_slides"] = preset["slides"]
    st.markdown("</div>", unsafe_allow_html=True)


def render_outline_preview(outline_data: Dict) -> None:
    try:
        narrative = json.loads(outline_data["narrative"])
    except Exception:
        st.warning("Could not parse slide preview from the outline response.")
        return

    slides = narrative.get("slides", [])
    st.markdown('<div class="panel-card"><h4 style="margin-top:0;">Slide Preview</h4>', unsafe_allow_html=True)
    preview_columns = st.columns(2)
    for index, slide in enumerate(slides[:8]):
        with preview_columns[index % 2]:
            bullets = slide.get("bullet_points", [])
            bullet_preview = " | ".join(bullets[:3]) if bullets else "Title / opening slide"
            st.markdown(
                f"""
                <div class="preview-card">
                    <h4>{slide.get("slide_number", index + 1)}. {slide.get("title", "Untitled")}</h4>
                    <p>{bullet_preview}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def render_summary(summary) -> None:
    st.markdown('<div class="panel-card"><h4 style="margin-top:0;">Document Summary</h4>', unsafe_allow_html=True)
    if isinstance(summary, dict):
        overview_cols = st.columns(3)
        overview_cols[0].metric("Main Theme", summary.get("main_theme", "-"))
        overview_cols[1].metric("Topic Count", len(summary.get("key_topics", [])))
        overview_cols[2].metric("Data Points", len(summary.get("data_points", [])))
        if summary.get("key_topics"):
            st.write("Key Topics")
            st.write(", ".join(summary["key_topics"]))
        if summary.get("conclusion"):
            st.write("Conclusion")
            st.write(summary["conclusion"])
    else:
        st.write(summary)
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="newd2p Experience", page_icon="P", layout="wide")
    ensure_state()
    inject_styles()

    styles_meta = get_styles_metadata()
    presentation_styles = styles_meta.get("presentation_styles", {})
    themes = styles_meta.get("themes", ["vibrant", "ocean", "sunset", "forest", "royal"])
    selected_preset = st.session_state.get("selected_preset", "Academic")
    preset_values = THEME_PRESETS.get(selected_preset, THEME_PRESETS["Academic"])

    render_hero()
    render_presets()

    with st.sidebar:
        st.header("Generation Controls")
        style_keys = list(presentation_styles.keys()) or [
            "ted_talk",
            "executive_summary",
            "training",
            "storytelling",
            "pitch_deck",
        ]
        default_style = st.session_state.get("preset_style", preset_values["style"])
        default_theme = st.session_state.get("preset_theme", preset_values["theme"])
        default_slides = st.session_state.get("preset_slides", preset_values["slides"])

        style_index = style_keys.index(default_style) if default_style in style_keys else style_keys.index(DEFAULT_STYLE)
        theme_index = themes.index(default_theme) if default_theme in themes else themes.index(DEFAULT_THEME)

        style = st.selectbox("Presentation style", style_keys, index=style_index)
        theme = st.selectbox("Theme", themes, index=theme_index)
        slide_count = st.slider("Number of slides", min_value=4, max_value=14, value=default_slides or DEFAULT_SLIDE_COUNT)
        include_speaker_notes = st.toggle("Speaker notes", value=True)
        use_ollama = st.toggle("Use Ollama AI", value=True)

        with st.expander("Advanced options"):
            image_mode = st.checkbox("Auto images", value=False)
            diagram_mode = st.checkbox("Auto diagrams", value=False)
            export_formats = st.multiselect("Additional exports", ["pdf", "markdown"], default=[])

    left, right = st.columns([1.35, 0.9])

    with left:
        tabs = st.tabs(["Upload", "Preview", "Generate"])

        with tabs[0]:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.subheader("Upload Document")
            uploaded_file = st.file_uploader(
                "Drag and drop your file here",
                type=["pdf", "docx", "txt"],
                help="Best results come from clean reports, project docs, and study material.",
            )
            if uploaded_file is not None:
                file_details = st.columns(3)
                file_details[0].metric("Filename", uploaded_file.name)
                file_details[1].metric("File Type", uploaded_file.type or "document")
                file_details[2].metric("Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")

                if st.button("Upload and register document", type="primary", use_container_width=True):
                    try:
                        upload_info = upload_document(uploaded_file)
                        st.session_state["uploaded_file_id"] = upload_info["file_id"]
                        st.session_state["uploaded_filename"] = upload_info["filename"]
                        st.session_state["outline_data"] = None
                        st.session_state["generation_result"] = None
                        st.session_state["current_stage"] = 1
                        st.success(f"Uploaded successfully. File ID: {upload_info['file_id']}")
                    except requests.RequestException as exc:
                        st.error(f"Upload failed: {exc}")
            st.markdown("</div>", unsafe_allow_html=True)

        with tabs[1]:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.subheader("Preview Slide Structure")
            file_id = st.session_state.get("uploaded_file_id")
            if not file_id:
                st.info("Upload a document first to preview the outline.")
            else:
                st.caption(f"Current file: {st.session_state.get('uploaded_filename', file_id)}")
                if st.button("Generate outline preview", use_container_width=True):
                    try:
                        st.session_state["current_stage"] = 2
                        # Preview uses the lightweight path for faster feedback.
                        outline_data = generate_outline(file_id, style, slide_count, False)
                        st.session_state["outline_data"] = outline_data
                        st.success("Slide preview generated.")
                    except requests.RequestException as exc:
                        st.error(f"Preview failed: {exc}")
            st.markdown("</div>", unsafe_allow_html=True)

        with tabs[2]:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.subheader("Generate Final Presentation")
            file_id = st.session_state.get("uploaded_file_id")
            if not file_id:
                st.info("Upload a document first.")
            else:
                st.caption(f"Ready to generate from: {st.session_state.get('uploaded_filename', file_id)}")
                if st.button("Generate presentation", type="primary", use_container_width=True):
                    progress = st.progress(0)
                    status_placeholder = st.empty()
                    try:
                        st.session_state["current_stage"] = 2
                        for index, step in enumerate(PIPELINE_STEPS):
                            status_placeholder.info(step)
                            progress.progress((index + 1) / len(PIPELINE_STEPS))
                            if index == 0 and not st.session_state.get("outline_data"):
                                try:
                                    st.session_state["outline_data"] = generate_outline(file_id, style, slide_count, False)
                                except requests.RequestException:
                                    pass
                            if index == 2:
                                st.session_state["current_stage"] = 3
                                result = generate_presentation(
                                    file_id=file_id,
                                    style=style,
                                    theme=theme,
                                    slide_count=slide_count,
                                    use_ollama=use_ollama,
                                    image_mode=image_mode,
                                    diagram_mode=diagram_mode,
                                    include_speaker_notes=include_speaker_notes,
                                    export_formats=export_formats,
                                )
                                st.session_state["generation_result"] = result
                                st.session_state["current_stage"] = 4
                        status_placeholder.success("Presentation ready.")
                        st.success("Presentation generated successfully.")
                    except requests.RequestException as exc:
                        st.error(f"Generation failed: {exc}")

                result = st.session_state.get("generation_result")
                if result:
                    generation_mode = result.get("generation_mode", "simple")
                    ollama_model = result.get("ollama_model")
                    st.markdown('<div class="download-strip">', unsafe_allow_html=True)
                    if generation_mode == "ollama" and ollama_model:
                        st.info(f"Using Ollama model: {ollama_model}")
                    else:
                        st.warning("Generated with local fallback mode.")

                    ppt_bytes = download_file("ppt", file_id)
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.download_button(
                            "Download PPTX",
                            data=ppt_bytes,
                            file_name=f"{file_id}_presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True,
                        )
                    with d2:
                        if "pdf" in export_formats:
                            try:
                                pdf_bytes = download_file("pdf", file_id)
                                st.download_button(
                                    "Download PDF",
                                    data=pdf_bytes,
                                    file_name=f"{file_id}_presentation.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                )
                            except requests.RequestException:
                                st.button("PDF unavailable", disabled=True, use_container_width=True)
                    with d3:
                        if "markdown" in export_formats:
                            try:
                                md_bytes = download_file("markdown", file_id)
                                st.download_button(
                                    "Download Markdown",
                                    data=md_bytes,
                                    file_name=f"{file_id}_presentation.md",
                                    mime="text/markdown",
                                    use_container_width=True,
                                )
                            except requests.RequestException:
                                st.button("Markdown unavailable", disabled=True, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with right:
        render_status_panel(st.session_state.get("current_stage", 0))
        if st.session_state.get("outline_data"):
            render_outline_preview(st.session_state["outline_data"])
        result = st.session_state.get("generation_result")
        if result and result.get("document_summary"):
            render_summary(result["document_summary"])
        else:
            st.markdown(
                """
                <div class="panel-card">
                    <h4 style="margin-top:0;">Experience Notes</h4>
                    <p style="color:#5e6a70;">
                        Use the preview tab before final generation to catch structure issues early.
                        For college project reports, the current prompt flow tries to produce
                        problem statement, objective, architecture, workflow, tech stack, AI pipeline,
                        modules, results, limitations, and future scope.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
