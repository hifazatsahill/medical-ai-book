<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.0.0
Modified principles: [PRINCIPLE_1_NAME] → Quality Standards, [PRINCIPLE_2_NAME] → Book Topic, [PRINCIPLE_3_NAME] → Base Requirements, [PRINCIPLE_4_NAME] → Bonus Features, [PRINCIPLE_5_NAME] → Technical Constraints, [PRINCIPLE_6_NAME] → Deliverables
Added sections: Ethical Guidelines
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
- README.md ⚠ pending
Follow-up TODOs: None
-->

# AI in Medical Laboratory Diagnostics: Revolutionizing Precision and Efficiency Constitution

## Core Principles

### Quality Standards
All content must be accurate, original, evidence-based, and verifiable. Medical and technical claims must reference primary peer-reviewed sources (e.g., PubMed, The Lancet, Nature Medicine, CLSI guidelines, FDA documents). Code examples must be practical, safe, modular, well-documented, testable, and deployable using free-tier services. Zero tolerance for plagiarism or unsubstantiated claims.

### Book Topic
A comprehensive guide exploring the transformative role of Artificial Intelligence in medical laboratory diagnostics. Covers fundamentals of lab medicine, AI/ML techniques (classical ML, deep learning, CNNs for pathology images, NLP for reports), real-world applications (hematological analysis, microbiology, clinical chemistry, digital pathology, predictive diagnostics), ethical considerations, regulatory aspects, implementation challenges, and future trends.

### Base Requirements (100 points)
Create a fully interactive digital book using AI/spec-driven methods. Build and embed a Retrieval-Augmented Generation (RAG) chatbot using OpenAI Agents/ChatKit SDKs, FastAPI backend, Neon Serverless Postgres database, Qdrant Cloud Free Tier vector store. The chatbot must answer questions based on the full book content and user-selected text only (context-aware mode).

### Bonus Features (up to 200 extra points)
+50 points: Create and use reusable intelligence via Claude Code Subagents and Agent Skills throughout the book project (e.g., for content generation, literature summarization, code example automation, and task orchestration). +50 points: Implement user authentication (Signup/Signin) using https://www.better-auth.com/. During signup, collect user background (software/hardware experience, medical/lab profession) to enable content personalization. +50 points: Allow logged-in users to personalize chapter content by pressing a button at the start of each chapter (content adapts based on stored user background, e.g., simplified for students, advanced/clinical focus for pathologists or lab technicians). +50 points: Allow logged-in users to translate chapter content to Urdu by pressing a button at the start of each chapter.

### Technical Constraints
Use only free-tier services where specified. Ensure security best practices (environment variables, secure auth, input sanitization). RAG responses must achieve >90% relevance and factual accuracy in testing (especially critical for medical content). Cross-browser compatibility and responsive design required.

### Deliverables
Fully published interactive book titled AI in Medical Laboratory Diagnostics: Revolutionizing Precision and Efficiency with embedded functional RAG chatbot. Complete, clean, and well-organized source code repository. Clear documentation of architecture, deployment steps, and bonus feature implementations.

## Ethical Guidelines
Promote inclusive, bias-free, and patient-safe content. Clearly state that the book is educational and not a substitute for professional medical advice or regulatory approval. Protect user privacy (secure storage and ethical use of background data for personalization).

## Governance
This constitution defines the foundational quality standards for developing an interactive digital book using AI/spec-driven methods with an integrated RAG chatbot. It ensures all downstream specifications, plans, and tasks align to deliver a high-scoring project (base 100 points + up to 200 bonus points). The workflow emphasizes spec-driven development, rigorous verification, reusable intelligence, personalization, and accessibility. This constitution must be referenced in every downstream artifact. All specifications, plans, and tasks inherit these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-21 | **Last Amended**: 2025-12-21