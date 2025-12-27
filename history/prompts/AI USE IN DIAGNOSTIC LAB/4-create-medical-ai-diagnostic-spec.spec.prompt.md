---
id: 4
title: Create Medical AI Diagnostic Spec
stage: spec
date: 2025-12-21
surface: agent
model: Claude Sonnet 4.5
feature: AI USE IN DIAGNOSTIC LAB
branch: null
user: user
command: sp.clarify
labels: [spec,medical,ai,diagnostics,laboratory]
links:
  spec: specs/AI USE IN DIAGNOSTIC LAB/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/AI USE IN DIAGNOSTIC LAB/spec.md
 - specs/AI USE IN DIAGNOSTIC LAB/checklists/requirements.md
tests:
 - null
---

## Prompt

Create specification at: specs/AI USE IN DIAGNOSTIC LAB/spec.md

Topic: Use of Artificial Intelligence in Medical Diagnostic Laboratories

Role: You are acting as a senior medical AI reviewer, clinical researcher, and academic editor. Your task is to stress-test this specification for clarity, scientific rigor, and feasibility before planning or execution begins.

Analyze the specification in the following dimensions and identify all gaps, ambiguities, and conflicts.

────────────────────────────────────
1. AMBIGUOUS TERMS (DEFINE PRECISELY)
────────────────────────────────────

Clarify all undefined or weakly defined terms, including but not limited to:

- "AI-based diagnostic support"
  • Does this include:
    – Machine learning and deep learning models only?
    – Rule-based expert systems?
    – Hybrid human-AI decision systems?
  • Should AI be limited to decision-support, or may it include autonomous diagnostic or triage systems?

- "Improved diagnostic accuracy"
  • Which metrics are REQUIRED?
    – Sensitivity, specificity, ROC-AUC, PPV/NPV
    – Error rate reduction
    – Turnaround time improvement
  • Must improvements be quantitatively reported, or are qualitative summaries acceptable?

- "Clinical efficiency"
  • Does this refer to:
    – Reduced reporting turnaround time?
    – Reduced workload for lab staff and pathologists?
    – Increased test throughput?
    – Cost reduction?
  • Which metrics must be prioritized?

- "Validated AI systems"
  • What level of validation is REQUIRED?
    – Regulatory approval (FDA, CE, WHO)?
    – Peer-reviewed clinical validation studies?
    – Real-world hospital or laboratory deployment?

────────────────────────────────────
2. MISSING ASSUMPTIONS (MAKE EXPLICIT)
────────────────────────────────────

Identify assumptions that must be explicitly stated to avoid misalignment:

- Citation and formatting standard
  • APA (medical/health sciences default)?
  • Journal-ready formatting?

- Target audience
  • Clinical pathologists
  • Laboratory technologists
  • Hospital administrators
  • Medical AI researchers
  • Mixed professional audience?

- Paper length
  • Minimum and maximum word count
  • Treatment of tables, figures, and appendices

- Source recency
  • Default window (last 5 years)?
  • Are landmark studies older than 5–10 years acceptable for background?

- Regulatory scope
  • International (FDA, CE, WHO)?
  • Regional only?
  • Comparative regulatory discussion allowed or excluded?

────────────────────────────────────
3. INCOMPLETE REQUIREMENTS (FILL GAPS)
────────────────────────────────────

Identify incomplete or underspecified requirements, including:

- Introduction requirements
  • Background and historical context?
  • Clear problem statement (limitations of traditional diagnostics)?
  • Explicit thesis on AI's role and value?

- Conflicting or negative evidence
  • Must studies showing AI failure, bias, or underperformance be included?
  • How should model bias, overfitting, dataset shift, and generalizability be handled?

- Source credibility
  • Peer-reviewed medical journals only?
  • Are WHO, CDC, FDA technical reports acceptable?
  • Are preprints (e.g., medRxiv) allowed or excluded?

- Structural organization
  • Thematic (applications, benefits, challenges)?
  • Workflow-based (pre-analytical, analytical, post-analytical)?
  • Modality-based (hematology, pathology, microbiology, radiology)?

───────────────────────────────────

## Response snapshot

Created comprehensive specification for "Use of Artificial Intelligence in Medical Diagnostic Laboratories" that addresses all clarification requirements:

1. AMBIGUOUS TERMS - Clearly defined:
   - AI-based diagnostic support includes machine learning, deep learning, rule-based systems, and hybrid approaches
   - Diagnostic accuracy metrics include sensitivity, specificity, ROC-AUC, PPV/NPV
   - Clinical efficiency encompasses turnaround time, workload reduction, throughput, and cost
   - Validated AI systems require regulatory approval and peer-reviewed studies

2. MISSING ASSUMPTIONS - Made explicit:
   - Uses APA citation standards with peer-reviewed medical journals
   - Targets clinical pathologists, laboratory directors, and medical researchers
   - Includes content organized by diagnostic specialty and workflow stage
   - Covers both benefits and risks with balanced presentation

3. INCOMPLETE REQUIREMENTS - Filled gaps:
   - Includes content about AI failures, bias, and limitations
   - Organized by diagnostic specialties (hematology, pathology, microbiology, clinical chemistry)
   - Addresses pre-analytical, analytical, and post-analytical applications
   - Provides standardized metrics for AI diagnostic accuracy

The specification includes 3 prioritized user stories, 10 functional requirements, 5 key entities, and 8 measurable success criteria with specific metrics.

## Outcome

- ✅ Impact: Comprehensive medical AI diagnostic specification created with clarifications
- 🧪 Tests: No tests required for specification
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Plan implementation with /sp.plan
- 🧠 Reflection: Specification addresses all requested clarifications for medical context

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create implementation plan for medical AI content