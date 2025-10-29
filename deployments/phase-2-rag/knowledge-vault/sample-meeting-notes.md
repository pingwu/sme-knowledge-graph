# Weekly Engineering Standup - January 10, 2024

---
date: 2024-01-10
tags: [meeting, standup, engineering]
people: [john-smith, sarah-johnson, mike-chen, lisa-wang]
meeting-type: weekly-standup
---

## Attendees

- John Smith (Engineering Lead)
- Sarah Johnson (Product Manager)
- Mike Chen (DevOps)
- Lisa Wang (Frontend Engineer)

## Agenda

1. Database selection decision
2. Q2 launch timeline review
3. Team capacity planning
4. Blockers and risks

---

## 1. Database Selection Decision

**John**: We need to finalize database choice this week. Customer (Acme Corp) requires on-premise deployment.

**Key Points**:
- PostgreSQL emerging as top choice
- Team has existing expertise (John, Mike have 5+ years)
- Meets SOC2 compliance requirements
- Customer's on-premise requirement eliminates cloud-only options (Aurora, Cosmos DB)

**Sarah**: From product perspective, need full-text search for user dashboard. Can PostgreSQL handle this?

**John**: Yes, PostgreSQL has excellent full-text search with GiN indexes. We can also add Elasticsearch later if needed.

**Decision**: Move forward with PostgreSQL. John to write technical architecture doc by Friday.

---

## 2. Q2 Launch Timeline Review

**Sarah**: Target launch is April 15 (13 weeks from now).

**Milestones**:
- Week 4 (Feb 7): Database migration complete
- Week 8 (Mar 7): Feature freeze
- Week 10 (Mar 21): Beta testing begins
- Week 13 (Apr 15): General availability

**Mike**: Database migration is critical path. 6-week estimate assumes:
- No schema changes after Feb 1
- Test data ready by Jan 20
- Migration scripts reviewed and tested

**Risk**: If schema changes after Feb 1, we slip timeline by 2-3 weeks.

**Sarah**: Understood. I'll lock requirements by Jan 25.

---

## 3. Team Capacity Planning

**John**: Current team: 4 engineers (2 backend, 1 frontend, 1 DevOps)

**Needs**:
- Backend: Need +1 senior engineer for database work
- Frontend: Lisa can handle alone for MVP, but need +1 by March for scale features

**Sarah**: Recruiting pipeline:
- Backend senior role: 3 candidates in final round
- Frontend mid-level: Job posted, 15 applications

**Decision**: Prioritize backend hire. Target offer by Jan 31.

---

## 4. Blockers and Risks

### Blocker 1: Test Data Availability
**Mike**: QA environment needs realistic test data for migration testing.
**Action**: Sarah to coordinate with Acme Corp for sanitized production dump (due: Jan 18)

### Blocker 2: Docker Desktop Licensing
**Lisa**: New Docker Desktop licensing affects local dev environments.
**Mike**: Investigating Podman or Colima as alternatives. Will have recommendation by Friday.

### Risk 1: PostgreSQL Training Gap
**John**: 2 engineers (Lisa, new hire) need PostgreSQL training.
**Action**: Schedule internal training sessions (Weeks 2-3, 1 hour each)

---

## Action Items

| Owner | Action                               | Due Date | Status      |
| ----- | ------------------------------------ | -------- | ----------- |
| John  | PostgreSQL architecture doc          | Jan 15   | In Progress |
| Sarah | Lock product requirements            | Jan 25   | Not Started |
| Sarah | Get sanitized test data from Acme    | Jan 18   | In Progress |
| Mike  | Docker Desktop alternatives research | Jan 15   | In Progress |
| John  | Schedule PostgreSQL training         | Jan 17   | Not Started |

---

## Next Meeting

**Date**: January 17, 2024 (Weekly standup)
**Focus**: Review architecture doc, confirm test data timeline

---

## Related Documents

- Database Decision: `sample-decision.md`
- Q2 Launch Plan: (TBD)
- Team Capacity Model: (TBD)
