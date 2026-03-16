"""
newd2p - Prompt Templates for LLM
"""


SYSTEM_PROMPT = """You are a world-class presentation designer and storyteller.
You create engaging, TED-talk style narratives from documents.
Your presentations are clear, compelling, and memorable.
You always respond in valid JSON format when asked."""


NARRATIVE_PROMPT = """Based on the following document content, create a presentation
with {slide_count} slides in "{style}" style.

Document Content:
{context}

Create a JSON response with this exact structure:
{{
    "title": "Presentation Title",
    "subtitle": "A compelling subtitle",
    "slides": [
        {{
            "slide_number": 1,
            "slide_type": "title",
            "title": "Engaging Title",
            "bullet_points": [],
            "speaker_notes": "What the presenter should say (2-3 paragraphs, natural speech)",
            "visual_cue": "Description of what visual/image should be shown",
            "duration_seconds": 30
        }},
        {{
            "slide_number": 2,
            "slide_type": "content",
            "title": "Slide Title",
            "bullet_points": ["Point 1", "Point 2", "Point 3"],
            "speaker_notes": "Natural speech for this slide...",
            "visual_cue": "Description of visual...",
            "duration_seconds": 45
        }}
    ]
}}

Rules:
- slide_type can be: title, content, chart, transition, closing
- Maximum 4 bullet points per slide
- Each bullet must be a SHORT PHRASE, not a sentence (maximum 6 words)
- Avoid generic phrases like "Key insights" or "Important points"
- Make slide titles professional and concise, not conversational
- Visual cues should describe what image, chart, diagram or infographic to show
- First slide is always "title" type
- Last slide is always "closing" type
- Include a "transition" slide between major topic changes
- Make it engaging and story-driven
- If the document is a software/AI project report, prefer this academic order:
  Problem Statement, Objective, System Architecture, Workflow / Methodology,
  Tech Stack, AI Pipeline, Code Modules, Results / Output, Limitations, Future Scope
- For project presentations, keep wording viva-friendly and clear for professors

Respond ONLY with valid JSON, no other text."""


SUMMARY_PROMPT = """Summarize the following document content in a structured way:

{content}

Provide:
1. Main theme (one sentence)
2. Key topics (list of 4-6 topics)
3. Important data points (any numbers, statistics, facts)
4. Main conclusion

Respond in JSON format:
{{
    "main_theme": "...",
    "key_topics": ["topic1", "topic2"],
    "data_points": ["stat1", "stat2"],
    "conclusion": "..."
}}

Respond ONLY with valid JSON."""


EXPLAIN_SLIDE_PROMPT = """You are an expert teacher explaining presentation slides
to students in a clear, friendly way.

Below is the content of a single slide from a presentation. Explain this slide
as if you are speaking to the audience. Use 1-3 short paragraphs, avoid jargon
unless it is explained, and focus on intuition and big-picture understanding.

Slide context:
- Title: "{title}"
- Bullet points: {bullets}
- Speaker notes (optional): {speaker_notes}

Write your explanation as plain text, not JSON. Do NOT restate the bullet points
verbatim; instead, explain them in natural language."""


CHART_ANALYSIS_PROMPT = """Analyze the following text for numerical data that can be
visualized as charts:

{content}

For each potential chart, provide:
{{
    "charts": [
        {{
            "chart_type": "bar",
            "title": "Chart Title",
            "labels": ["Label1", "Label2"],
            "values": [10, 20],
            "x_label": "X Axis",
            "y_label": "Y Axis"
        }}
    ]
}}

If no numerical data found, return: {{"charts": []}}

Respond ONLY with valid JSON."""


DIAGRAM_ANALYSIS_PROMPT = """Analyze the following text for processes, workflows,
or step-by-step sequences that can be visualized as simple diagrams.

Focus on flows like:
- pipelines (e.g., "Data Collection → Preprocessing → Training → Evaluation")
- business processes
- system / architecture flows at a high level

From the content, extract at most 3 of the most important flows and respond in
the following JSON format:
{{
  "diagrams": [
    {{
      "diagram_type": "workflow",
      "title": "Workflow Title",
      "steps": [
        "Step 1",
        "Step 2",
        "Step 3"
      ]
    }}
  ]
}}

Rules:
- Steps must be in the correct order of the process.
- Each diagram should have at least 2 and at most 8 steps.
- Use concise step names suitable for node labels.

If no clear processes or flows are found, return: {{"diagrams": []}}

Respond ONLY with valid JSON."""
