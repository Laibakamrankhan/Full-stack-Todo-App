<!--
SYNC IMPACT REPORT:
Version change: 1.1.0 → 1.2.0
Modified principles: Core Philosophy → Spec-Driven Development
Modified principles: Architectural Principles → Architecture & Tech Stack
Modified principles: Workflow Standards → Development Rules
Modified principles: Configuration & Secrets → Security Rules
Modified principles: Definition of Done → Definition of Done
Added sections: Vision, Core Principles
Removed sections: Evolutionary Architecture, Phase Isolation Rule, User Isolation & Security First, Checkpoint Pattern, Spec-Driven TDD, Monorepo Stability, 12-Factor Compliance, Authenticated Multi-User Correctness
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: none
-->

# Project Constitution – Todo Evolution Phase II

## Vision
Transform a single-user in-memory CLI Todo app into a secure, scalable, multi-user
full-stack web application following spec-driven development principles.

## Immutable Governance Framework

This Project Constitution establishes the foundational principles, governance mechanisms, and operational guidelines for the "Todo Evolution Phase II" project. This document is immutable and serves as the ultimate authority for all project decisions, architectural choices, and implementation standards throughout the project lifecycle.

---

## Core Principles

### 1. **Spec-Driven Development is Mandatory**
- **No feature implemented without approved spec**: All features must be specified before implementation
- **Sequential workflow**: Constitution → Spec → Plan → Tasks → Implementation
- **Verification requirement**: All implementations must align with approved specifications

### 2. **Clean Architecture and Separation of Concerns**
- **Layer isolation**: UI, API, Business Logic, and Persistence must be strictly separated
- **Authentication isolation**: Authentication logic must not leak into business logic
- **Clear boundaries**: Each component has a single, well-defined responsibility

### 3. **Security by Default**
- **Authentication requirement**: All API endpoints require JWT authentication
- **User data isolation**: Users can only access their own tasks
- **Security priority**: Security considerations take precedence over convenience

### 4. **Production-Ready Code Standards**
- **Quality standards**: All code must meet production readiness criteria
- **Error handling**: Proper error handling and validation in all components
- **Performance considerations**: Code optimized for production use

---

## Architecture & Tech Stack

### 5. **Frontend: Next.js 16+ (App Router)**
- **Framework requirement**: Use Next.js 16+ with App Router for frontend
- **Modern practices**: Follow Next.js best practices and conventions
- **Responsive design**: Ensure responsive and accessible UI

### 6. **Backend: Python FastAPI**
- **Framework requirement**: Use Python FastAPI for backend API
- **RESTful design**: Follow RESTful API principles
- **Type safety**: Use type hints throughout the codebase

### 7. **ORM: SQLModel**
- **Database interaction**: Use SQLModel for database operations
- **Type safety**: Leverage SQLModel's type safety features
- **Database abstraction**: Proper abstraction of database operations

### 8. **Database: Neon Serverless PostgreSQL**
- **Database provider**: Use Neon Serverless PostgreSQL for persistence
- **Connection management**: Proper connection pooling and management
- **Schema management**: Follow SQLModel conventions for schema definition

### 9. **Authentication: Better Auth (JWT-based)**
- **Authentication provider**: Use Better Auth for JWT-based authentication
- **Token verification**: JWT tokens must be verified on backend
- **Secure implementation**: Follow JWT security best practices

---

## Development Rules

### 10. **Claude Code + Spec-Kit Plus Mandate**
- **Implementation requirement**: All implementation code must be generated via Claude Code + Spec-Kit Plus
- **Manual coding prohibition**: Manual coding is strictly prohibited
- **Quality assurance**: Human oversight for architectural decisions, agent execution for implementation

### 11. **No Manual Boilerplate Coding**
- **Boilerplate generation**: All boilerplate code must be generated via tools
- **Template usage**: Use provided templates and patterns
- **Consistency requirement**: Maintain consistency through tooling

### 12. **Each Phase Must Be Testable Independently**
- **Test isolation**: Each phase must be independently testable
- **Verification points**: Clear verification points for each phase
- **Quality gates**: Each phase serves as a quality validation point

### 13. **Clear Folder Structure**
- **Frontend organization**: Clear folder structure for frontend components
- **Backend organization**: Clear folder structure for backend components
- **Separation**: Maintain clear separation between frontend and backend

---

## Security Rules

### 14. **JWT Authentication Requirements**
- **Universal authentication**: All API endpoints require JWT authentication
- **Token verification**: JWT token must be verified on backend
- **Unauthorized responses**: Unauthorized requests return 401

### 15. **User Data Isolation**
- **Access restriction**: Users can only access their own tasks
- **Cross-user protection**: Cross-user access is strictly forbidden
- **Data scoping**: Every task is scoped to a single user

### 16. **Secret Management**
- **Environment variables**: Shared secret must be read from environment variables
- **No committed secrets**: No secrets committed to repository
- **Secure configuration**: Follow 12-factor app methodology for configuration management

---

## Definition of Done

### 17. **Constitutional Compliance**
- **Constitution adherence**: All implementations must comply with this constitution
- **Specification alignment**: Implementation must match approved specifications
- **Clean build achievement**: All builds must pass without warnings or errors

### 18. **Multi-User Todo Web App**
- **Multi-user functionality**: System correctly handles multiple users simultaneously
- **User isolation**: User data properly isolated and secure
- **Full functionality**: All todo features work for multiple users

### 19. **JWT-Secured REST API**
- **Authentication validation**: All API endpoints properly authenticate users
- **Security compliance**: API follows JWT security best practices
- **Access control**: Proper access control for all endpoints

### 20. **Persistent Storage in Neon PostgreSQL**
- **Database integration**: Proper integration with Neon PostgreSQL
- **Data persistence**: All user data properly stored and retrieved
- **Connection management**: Proper database connection handling

### 21. **Responsive, Creative UI**
- **User experience**: Responsive and intuitive user interface
- **Creative design**: Creative and engaging UI design
- **Accessibility**: Accessible to all users

### 22. **Full Documentation in README**
- **Setup instructions**: Clear setup instructions provided in README
- **Environment reproduction**: Environments reproducible following README instructions
- **Deployment validation**: System deployable using documented procedures

---

*This constitution is effective as of the date of creation and remains immutable throughout the project lifecycle. Any exceptions or amendments require extraordinary circumstances and formal approval from the project governance board.*

**Version**: 1.2.0 | **Ratified**: 2025-12-20 | **Last Amended**: 2026-01-02