# Phase 1 – System Design & Planning

## Objective
Design an offline system that analyzes organizational security policies,
identifies gaps by benchmarking them against the NIST Cybersecurity Framework (CSF),
and suggests policy improvements.

## Constraints
- Fully offline execution
- Lightweight local LLM
- No external APIs or cloud services

## High-Level Workflow
1. Input organizational policy document
2. Load reference standards (NIST CSF)
3. Preprocess text using NLP techniques
4. Compare policy content with framework requirements
5. Identify missing or weak policy areas
6. Generate revised policy suggestions
7. Produce an improvement roadmap

## Role of NLP
- Text segmentation and section detection
- Keyword and key-phrase extraction
- Semantic similarity comparison
- Gap classification (missing, partial, adequate)

## Outcome of Phase 1
A clear architectural blueprint that guides dataset preparation,
model selection, and implementation in later phases.
