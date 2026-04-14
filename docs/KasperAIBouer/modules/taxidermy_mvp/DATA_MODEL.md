# TAXIDERMY_MVP — DATA MODEL (STARTER)

## Candidate entities
- Client
- Order / Job
- Trophy Item
- Item Component
- Attachment / Photo
- Quote
- Deposit Status
- Approval Record
- Final Payment Status
- Shipment / Handover Record

## Critical design principle
Identity and traceability come first.

## Key questions
- Is each trophy a job, or is a job an order containing multiple trophies?
- How are horns, skins, teeth, skulls and photos linked?
- What is the minimum unique code model?
- What data must be visible to the client?
- What approvals must be retained as audit history?

## Risks
- wrong item linkage
- missing photo association
- status progression without approval/payment requirements
- weak client-data separation


## v0.2 reminder
Traceability must remain stronger than cosmetic UI concerns.
