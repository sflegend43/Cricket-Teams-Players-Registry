# Implementation Plan — Cricket Team & Player Registry
## Based on Deep Analysis of Sports Car Showroom Reference Project (110 pages)

> [!IMPORTANT]
> This plan is **discussion-only**. No code changes will be made until you explicitly approve it.

---

## Project Overview

We will produce **3 documents** that exactly mirror the structure of the Cars Project reference, substituting cricket domain content:

| Document | Pages | Reference |
|---|---|---|
| **SRS Report** | ~41 pages | Sports Car Showroom SRS (41 pages) |
| **UML Diagrams** | ~35 pages | SE Project Diagrams (35 pages, 44 diagrams) |
| **Testing Document** | ~34 pages | Testing Document (34 pages, 3 levels) |

---

## Actors (3 — Required by Your Course)

Since the Cars Project had 2 actors (Admin + Customer) but your course requires **3 actors**, we add a third that mirrors their "Support Reviewer":

| # | Actor | Cricket Equivalent | Capabilities |
|---|---|---|---|
| 1 | **Admin** | League/Association Manager | Full CRUD: Add/Edit/Delete Teams & Players, manage system |
| 2 | **Team Manager** | Replaces "Support Reviewer" | Can view their assigned team's roster and update player stats |
| 3 | **Fan** | Replaces "Customer" | Register, Login, browse Teams & Players (read-only) |

---

## System Scope (Ultra-Simple — Easy to Document)

**System Name:** Cricket Team & Player Registry System

**What it does (only these features):**
1. **Auth**: Register (Fan only), Login (all 3 actors), Logout
2. **Team Management**: Admin can Add/Edit/Delete Teams; all can View Team List & Team Details
3. **Player Management**: Admin can Add/Edit/Delete Players; Team Manager can Edit player stats; all can View Player List & Player Profile

**What we REMOVE from the existing codebase:**
- ❌ Live Ball-by-Ball Scoring (entire `matches.html`, `matches.js`)
- ❌ Tournaments (`tournaments.html`, `tournaments.js`)
- ❌ Rankings (`rankings.html`, `rankings.js`)
- ❌ AI Stats (`stats.html`, `stats.js`)
- ❌ Records/Hall of Fame (`records.html`, `records.js`)
- ❌ Super Over, Free Hit, all complex cricket rules

**What we KEEP (only these 5 pages):**
- ✅ `login.html` — Login page
- ✅ `signup.html` — Registration page (Fan only)
- ✅ `index.html` — Simple dashboard/home
- ✅ `players.html` — Player list + Add/Edit/Delete
- ✅ `teams.html` — Team list + Add/Edit/Delete

---

## DOCUMENT 1: SRS Report (~41 pages)

Exact structure from Cars Project, cricket content substituted.

### Cover Page
- University: UET Lahore
- Project: Cricket Team & Player Registry System
- Submitted by: (your names + roll numbers)
- Submitted to: (your professor's name)
- Department of Computer Science

### Part A — Main Report (Pages 5–10)
| Section | Cricket Content |
|---|---|
| **Abstract** | Web-based cricket registry. 3 roles (Admin, Team Manager, Fan). Admin manages teams/players. Team Managers update stats. Fans browse. Flask + SQLite backend. |
| **Introduction** | Problem with manual cricket record-keeping. Need for centralized digital registry. |
| **Vision** | "To digitalize cricket team and player management by creating an efficient, user-friendly web platform..." |
| **Problem Statement** | "How can we overcome challenges of manual cricket record management to create a more efficient, secure, and user-friendly digital registry?" |
| **Objectives** | 1. User-Friendly Interface, 2. Automated Player Registry, 3. Role-Based Access Control, 4. Team Roster Management, 5. Secure Login System, 6. Database Integration, 7. Admin Control Panel |
| **Scope** | 3 actors, 5 screens, add/edit/delete teams and players |
| **Tools & Technology** | Python/Flask, SQLite, HTML/CSS/JS, VS Code, Astah UML, Figma |
| **System Design** | Users Table + Players Table + Team Table |
| **Related Work** | Compare 3 existing systems: ESPN Cricinfo, CricHeroes, ICC Website |
| **Team Members & Tasks** | Table: Name \| Reg No. \| Tasks (split Use Cases, Wireframes, Requirements) |
| **Timeline** | 4 weeks: Week 1 Scope, Week 2 Requirements, Week 3 Design, Week 4 Wireframes |
| **Data Gathering** | Data manually entered via admin panel |

### Part B — Requirements (Pages 11–16)

#### 1.1 Functional Requirements

**Table 1: Admin FRs (index: FR-01-XX)**
| Index | Requirement |
|---|---|
| FR-01-01 | The system shall allow an admin to login by providing email, password, and role type |
| FR-01-02 | The system shall verify admin credentials and allow access to the admin panel upon successful authentication |
| FR-01-03 | The system shall allow the admin to view all teams and players in the registry |
| FR-01-04 | The system shall enable the admin to add a new team with details (name, country, coach) |
| FR-01-05 | The system shall allow the admin to edit any team's details |
| FR-01-06 | The system shall allow the admin to delete any team from the registry |
| FR-01-07 | The system shall enable the admin to add a new player with details (name, role, DOB, team) |
| FR-01-08 | The system shall allow the admin to edit any player's details |
| FR-01-09 | The system shall allow the admin to delete any player from the registry |
| FR-01-10 | The system shall allow the admin to logout successfully |

**Table 2: Team Manager FRs (index: FR-02-XX)**
| Index | Requirement |
|---|---|
| FR-02-01 | The system shall allow a team manager to login with valid credentials |
| FR-02-02 | The system shall allow the team manager to view the roster of their assigned team |
| FR-02-03 | The system shall allow the team manager to update player statistics for their team |
| FR-02-04 | The system shall allow the team manager to logout successfully |

**Table 3: Fan FRs (index: FR-03-XX)**
| Index | Requirement |
|---|---|
| FR-03-01 | The system shall allow fans to register an account by entering name, email, and password |
| FR-03-02 | The system shall authenticate fan credentials and grant access upon successful login |
| FR-03-03 | The system shall display a list of all cricket teams with basic details |
| FR-03-04 | The system shall display detailed information about a selected team including roster |
| FR-03-05 | The system shall display a list of all registered players with name, role, and team |
| FR-03-06 | The system shall display detailed profile of a selected player |
| FR-03-07 | The system shall allow the fan to logout securely |

#### 1.2 Non-Functional Requirements (7 items, bold title + paragraph)
1. **User Registration** — Fans can create accounts via registration form
2. **User Authentication** — All roles authenticate via login before accessing role-specific features
3. **Browse Team Listings** — All users can view team directory with basic details
4. **View Team Details** — Users can click on a team to see full roster
5. **Browse Player Listings** — All users can view player registry
6. **View Player Profile** — Users can click on a player to see full profile
7. **Logout Functionality** — All users can securely log out at any time

#### 1.3 Business Requirements (6 bullets)
- Centralized Player Information Management
- Team Display for Users
- Admin Control Panel
- Data Security and Accuracy
- Responsive and User-Friendly Interface
- Maintainability and Scalability

#### 1.4 Business Rules (6 numbered)
1. Only registered users can access the player and team directory
2. The admin is the only authorized user who can add, update, or delete team and player information
3. A valid email and password are required for login authentication
4. All players added must include mandatory details (name, DOB, role, nationality, team)
5. Team Managers can only update players of their assigned team
6. Any player deleted by admin should automatically be removed from the team roster view

#### 1.5 User Requirements, 1.6 External Interface, 1.7 Physical Requirements, 1.8 Development Constraints
(Same format as Cars Project, cricket content)

### Part C — Design Specifications (Pages 17–40)

#### 2.1 Wireframes (12 screens)
Each screen: Figma grayscale screenshot + table (Sr NO. \| Element \| As Fan \| As Admin \| As Team Manager)

| # | Screen |
|---|---|
| 1 | Home / Landing Page |
| 2 | Login Page |
| 3 | Register Page |
| 4 | Team List Page |
| 5 | Team Details Page |
| 6 | Player List Page |
| 7 | Player Profile Page |
| 8 | Admin Dashboard |
| 9 | Add Player Form |
| 10 | Edit Player Form |
| 11 | Add Team Form |
| 12 | Team Manager Dashboard |

#### 2.2 Use Cases (9 use case tables)
Same field structure as Cars Project: Name, Participating Actor, Goals, Triggers, Pre-conditions, Post-conditions, Basic Flow (Actor\|System two-column table), Alternative Flow, Exceptions, Qualities.

| # | Use Case | Actor |
|---|---|---|
| 1 | Admin Login | Admin |
| 2 | Add Player | Admin |
| 3 | Edit Player | Admin |
| 4 | Delete Player | Admin |
| 5 | System Login (combined) | Admin, Team Manager, Fan |
| 6 | Register Account | Fan |
| 7 | View Player List | Fan, Admin, Team Manager |
| 8 | View Player Profile | Fan, Admin, Team Manager |
| 9 | Update Player Stats | Team Manager |

#### 2.3 User Stories
**Admin (6 stories):**
- As an Admin, I want to **log in** so that I can access the admin panel to manage teams and players.
- As an Admin, I want to **add a new player** so that I can update the registry with newly registered players.
- As an Admin, I want to **update player details** so that I can keep player information accurate.
- As an Admin, I want to **view the list of players** so that I can monitor all registered players.
- As an Admin, I want to **delete a player** so that I can remove players who are no longer active.
- As an Admin, I want to **log out** from the system so that my admin account remains secure.

**Team Manager (4 stories):**
- As a Team Manager, I want to **log in** so that I can access my team's roster.
- As a Team Manager, I want to **view my team's roster** so that I can see all assigned players.
- As a Team Manager, I want to **update player stats** so that I can keep performance records current.
- As a Team Manager, I want to **log out** so that my account remains secure.

**Fan (6 stories):**
- As a Fan, I want to **register an account** so that I can access the cricket registry.
- As a Fan, I want to **log in** so that I can securely browse teams and players.
- As a Fan, I want to **view the list of teams** so that I can explore all registered teams.
- As a Fan, I want to **view detailed team information** so that I can see the full roster.
- As a Fan, I want to **view player profiles** so that I can learn about individual players.
- As a Fan, I want to **log out** so that I can securely end my session.

#### 2.4 Storyboards (3 flow diagrams — one per actor, made in Figma)

---

## DOCUMENT 2: UML Diagrams (~35 pages, 44 diagrams)

**Tool: Astah UML** (same tool as Cars Project — free to download)

All 10 diagram types, same count as Cars Project:

| Diagram Type | Count | Cricket Use Cases |
|---|---|---|
| Use Case Diagram | 1 | 3 actors, ~12 use cases |
| Class Diagram | 1 | Person→Admin/TeamManager/Fan + Player + Team |
| Component Diagram | 1 | 5 components with lollipop interfaces |
| Object Diagram | 1 | 6 instances with real cricket values |
| Deployment Diagram | 1 | Browser → Flask Server → SQLite DB |
| Sequence Diagrams | 7–9 | Login, Register, Add Player, Edit Player, Delete Player, View List, Update Stats |
| Collaboration Diagrams | 7–9 | Same use cases, simpler form |
| Activity Diagrams | ~9 | One per use case, no swim lanes |
| State Machine Diagrams | ~9 | One per use case, entry/do/exit notation |
| Package Diagram | 1 | person→admin/manager/fan + player + team packages |

### Class Diagram Structure
```
Person (parent)
  #name: string
  #email: string
  #id: int
  #password: string
  #role: string
  +login(): void
  +register(): void
  +displayDashboard(): void

Admin extends Person
  +addPlayer(p): void
  +editPlayer(p): void
  +deletePlayer(int id): void
  +addTeam(t): void
  +deleteTeam(int id): void

TeamManager extends Person
  +viewRoster(): List<Player>
  +updatePlayerStats(p): void

Fan extends Person
  +viewPlayerList(): List<Player>
  +viewTeamList(): List<Team>

Player
  +id: int
  +name: string
  +DOB: string
  +nationality: string
  +role: string
  +battingStyle: string
  +bowlingStyle: string
  +teamName: string
  +addPlayer(): void
  +getPlayers(): List<Player>
  +updatePlayer(): void
  +deletePlayer(): void

Team
  +teamName: string
  +country: string
  +headCoach: string
  +ranking: int
  +createTeam(): void
  +getTeams(): List<Team>
  +deleteTeam(): void
```

### Deployment Diagram
- Node 1: **Client Device** → artifacts: Chrome, Edge
- Node 2: **Flask Web Server** → artifact: Python/Flask App
- Node 3: **Database Server** → artifacts: SQLite DB file

---

## DOCUMENT 3: Testing Document (~34 pages)

**3 Testing Levels** (exact same structure as Cars Project):

### Level 1: Unit Testing
Pages/screens to test (one section per screen, with screenshot + Rules list + test case tables):

| Screen | Fields to Test |
|---|---|
| Home Page | Navigation buttons, Logo |
| Login Page | Email V1.0/V1.1, Password V1.0, Login Button |
| Register Page | Name V1.0, Email V1.0/V1.1, Password V1.0, Register Button |
| Admin Dashboard | Logout Button V1.0/V1.1 |
| Add Player | Player Name V1.0/V1.1, DOB V1.0, Role V1.0, Nationality V1.0, Team V1.0, Save Button |
| Edit Player | Same fields + Update Button V1.0/V1.1 |
| Delete Player | Delete Button |
| View Player Profile | Profile Button |
| Add Team | Team Name V1.0/V1.1, Country V1.0, Coach V1.0, Save Button |
| Team Manager Dashboard | Logout Button V1.0/V1.1 |
| Update Player Stats | Stats field V1.0/V1.1, Update Button |

**Column Format (4 columns):**
`Test Data | Expected Results | Actual Results | Pass/Fail`

**V1.0 → V1.1 pattern:** Show some deliberate Fails in V1.0, then fix and retest in V1.1

### Level 2: Integration Testing
**Column Format (5 columns):**
`Test Case ID | Test Case Description | Expected Results | Actual Results | Pass/Fail`

IDs: INT_1, INT_2, ...

Groups:
1. User Register V1.0
2. User Login V1.0
3. Player Management V1.0
4. Team Management V1.0
5. View Players/Teams V1.0
6. Update Player Stats V1.0
7. Session Management V1.0

### Level 3: System Testing
**3 system test cards (one per actor):**
- CTPR_001: Test Admin Functionality (login, add player, edit player, delete player, add team, logout)
- CTPR_002: Test Fan Functionality (register, login, view teams, view players, logout)
- CTPR_003: Test Team Manager Functionality (login, view roster, update player stats, logout)

**Card structure (exact same fields as Cars Project):**
- Test Case ID + Description
- Created by + Reviewed by + Version
- QA Tester's Log: NULL
- Tester's name + Date Tested + Pass/Fail
- Prerequisites table
- Test Data table
- Test Scenario box
- Steps table (Step# | Step Details | Expected Result | Actual Result | Pass/Fail)
- Post Condition box

---

## Open Questions (Discuss Before Executing)

> [!IMPORTANT]
> **Actor 3 name:** Do you prefer "Team Manager" or something else like "Scout" or "Coach"? This needs to match what's written on the register page dropdown.

> [!IMPORTANT]
> **Team Members:** How many people are in your group and what are their names/roll numbers? I need this for the cover page and the Team Members & Tasks table.

> [!WARNING]
> **Wireframes tool:** The Cars Project used **Figma** for wireframes. Do you have Figma access? If not, we can use simple screenshots of the actual running app instead (which is even better — real screenshots are more impressive than mockups).

> [!WARNING]
> **UML Tool:** The Cars Project used **Astah UML**. This is free software. I recommend downloading it so your diagrams match the reference project's exact style. However, I can also generate text descriptions of every diagram so you can draw them manually or in any other UML tool.

---

## Implementation Steps (After Your Approval)

1. **Code changes** (30 minutes): Strip the codebase down to 5 pages, add Team Manager role
2. **Run the app** + take screenshots of all 12 screens → use as Wireframes
3. **Generate all text content** for the SRS Report (every section, every table, every use case, every user story)
4. **Generate all UML diagram descriptions** in Astah format for all 44 diagrams
5. **Generate all Test Cases** for all 3 testing levels
