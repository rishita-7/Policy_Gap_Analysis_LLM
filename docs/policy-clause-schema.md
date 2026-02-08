# Policy Clause Schema

Each policy clause represents a single security requirement
derived from the CIS MS-ISAC NIST CSF Policy Template Guide.

## Fields

- clause_id:
  Unique identifier for the clause

- nist_function:
  One of Identify, Protect, Detect, Respond, Recover

- nist_category:
  Corresponding NIST CSF category (e.g., ID.AM, PR.AC)

- title:
  Short description of the requirement

- description:
  Detailed policy expectation from the framework

- keywords:
  Important terms used for NLP matching

- severity:
  Importance level of the clause (High / Medium / Low)

## Purpose
This schema enables structured comparison between
organizational policies and standard security requirements.
