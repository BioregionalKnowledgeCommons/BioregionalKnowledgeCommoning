# Transcription and Processing Pipeline

## Purpose
Support the BKC Practices and Patterns effort by enabling consent-aware interview transcription, processing, and ontology mapping.

## Pipeline
1. Intake
- Register interview metadata and consent policy before processing.

2. Transcription
- Produce timestamped transcript with speaker attribution.

3. QA
- Human pass for correction and redaction where required.

4. Extraction
- Extract entities, practices, patterns, claims, and evidence.

5. Mapping
- Create ontology mapping proposals and route to review.

6. Publication
- Publish only consent-permitted outputs (public or restricted tiers as configured).

7. Audit
- Maintain traceability from recording -> transcript -> extraction -> mapping -> publication.

## Required Metadata
- source/interview ID
- participants and roles
- consent tier
- usage constraints
- processing timestamps
- reviewer identity

## Acceptance Criteria (Pilot)
- At least one interview transcript processed end-to-end.
- Consent metadata validated at intake and before publication.
- Mapping approvals recorded with rationale.
- Export pipeline blocks artifacts missing consent metadata.
