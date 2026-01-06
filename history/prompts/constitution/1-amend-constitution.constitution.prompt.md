---
id: 1
title: amend constitution
stage: constitution
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-fullstack-todo
user: Claude Sonnet 4.5
command: sp.constitution
labels: [constitution, update, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
# Project Constitution – Todo Evolution Phase II

## Vision
Transform a single-user in-memory CLI Todo app into a secure, scalable, multi-user
full-stack web application following spec-driven development principles.

## Core Principles
- Spec-driven development is mandatory
- No feature is implemented without an approved spec
- Clean architecture and separation of concerns
- Security by default (JWT-based authentication)
- User data isolation at every layer
- Production-ready code standards

## Architecture
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- API Style: RESTful

## Security Rules
- All API endpoints require JWT authentication
- JWT token must be verified on backend
- Users can only access their own tasks
- Shared secret must be read from environment variables
- Unauthorized requests return 401

## Development Rules
- Use Claude Code + Spec-Kit Plus for all implementation
- No manual boilerplate coding
- Each phase must be testable independently
- Clear folder structure for frontend and backend

## Definition of Done
- Multi-user Todo web app
- JWT-secured REST API
- Persistent storage in Neon PostgreSQL
- Responsive, creative UI
- Full documentation in README
```

## Response snapshot

Updated the project constitution to reflect the requirements for transforming a single-user CLI Todo app into a multi-user web application with specific architectural principles. The new constitution includes sections for Vision, Core Principles, Architecture & Tech Stack, Development Rules, Security Rules, and Definition of Done, all aligned with the user's requirements.

## Outcome

- ✅ Impact: Updated constitution file to version 1.2.0 with new principles
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: None needed
- 🧠 Reflection: Constitution now properly reflects the multi-user web application requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A