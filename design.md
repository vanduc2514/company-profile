# Design Document — Automated Enterprise Customer Profile App

> **Version:** 1.0  
> **Last Updated:** 2026-08-15  
> **Stack:** HTML5 · Vanilla JS (ES6+) · Tailwind CSS (CDN) · Inter Font · Phosphor Icons

---

## 1. Design Philosophy

The interface is inspired by the intersection of three aesthetic references:

| Reference | Borrowed Quality |
|---|---|
| **Notion** | Clean information hierarchy, generous whitespace, card-based layout |
| **Linear** | Precise typography, keyboard-first feel, sidebar navigation |
| **Bloomberg Terminal** | Data density, status badges, structured field/value grids |

**Core principle:** *Data-dense but visually breathable.* The app handles complex enterprise data without overwhelming the user. Every element has a purpose; nothing is decorative noise.

---

## 2. Color System

### 2.1 Dark Mode (Default)

| Token | Hex | Usage |
|---|---|---|
| `--bg-base` | `#0f172a` | App background (deep navy) |
| `--bg-surface` | `#1e293b` | Cards, sidebar, panels |
| `--bg-elevated` | `#293548` | Input fields, hover states |
| `--bg-border` | `#334155` | Dividers, input borders |
| `--accent-primary` | `#6366f1` | CTA buttons, active states, links |
| `--accent-secondary` | `#818cf8` | Hover accents, progress steps |
| `--accent-glow` | `rgba(99,102,241,0.3)` | Button glow, focus rings |
| `--text-primary` | `#f1f5f9` | Headings, primary labels |
| `--text-secondary` | `#94a3b8` | Supporting text, placeholders |
| `--text-muted` | `#64748b` | Timestamps, metadata |
| `--success` | `#22c55e` | Completed pipeline steps |
| `--warning` | `#f59e0b` | Medium confidence scores |
| `--danger` | `#ef4444` | Delete actions |

### 2.2 Light Mode (Toggle)

| Token | Hex | Usage |
|---|---|---|
| `--bg-base` | `#f8fafc` | App background (off-white) |
| `--bg-surface` | `#ffffff` | Cards, sidebar |
| `--bg-elevated` | `#f1f5f9` | Input fields |
| `--bg-border` | `#e2e8f0` | Dividers |
| `--text-primary` | `#0f172a` | Headings |
| `--text-secondary` | `#475569` | Supporting text |
| `--text-muted` | `#94a3b8` | Timestamps |

Accent colors (`--accent-primary`, `--accent-secondary`) remain identical across themes.

### 2.3 Industry Tag Palette

| Industry | Background | Text |
|---|---|---|
| Technology / SaaS | `#1e3a5f` | `#60a5fa` |
| Finance | `#14532d` | `#4ade80` |
| Manufacturing | `#431407` | `#fb923c` |
| Healthcare | `#4a1d96` | `#c084fc` |
| Retail / E-commerce | `#713f12` | `#fbbf24` |
| Unknown / Other | `#1e293b` | `#94a3b8` |

---

## 3. Typography

**Font Family:** [Inter](https://fonts.google.com/specimen/Inter) — imported via Google Fonts CDN.

```
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
```

| Role | Weight | Size | Color Token |
|---|---|---|---|
| App Title / Logo | 700 Bold | 18px | `--text-primary` |
| Section Heading | 600 Semibold | 14px | `--text-primary` |
| Field Label | 500 Medium | 12px | `--text-secondary` (uppercase, letter-spacing: 0.08em) |
| Field Value | 400 Regular | 14px | `--text-primary` |
| Sidebar Item Title | 500 Medium | 13px | `--text-primary` |
| Timestamp / Meta | 400 Regular | 11px | `--text-muted` |
| CTA Button | 600 Semibold | 14px | `#ffffff` |
| Badge Text | 600 Semibold | 11px | varies by tag |

---

## 4. Layout Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TOPBAR  (Logo · App Title · Theme Toggle)                  │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│   SIDEBAR    │          MAIN PANEL                         │
│   (280px)    │          (flex-grow)                        │
│              │                                              │
│  [Search]    │  ┌─ VIEW A: Input Form ──────────────────┐  │
│              │  │  Source textareas (Google, LinkedIn,   │  │
│  ─────────   │  │  Website, Registration)                │  │
│  Saved       │  │  [Generate Profile ▶] CTA button       │  │
│  Profiles    │  └────────────────────────────────────────┘  │
│  List        │                                              │
│              │  ┌─ VIEW B: AI Pipeline ──────────────────┐  │
│  • Profile 1 │  │  Step 1: Collecting sources ✓          │  │
│  • Profile 2 │  │  Step 2: Analyzing data ···            │  │
│  • Profile 3 │  │  Step 3: Structuring output            │  │
│              │  │  Step 4: Done                          │  │
│  [+ New]     │  └────────────────────────────────────────┘  │
│              │                                              │
│              │  ┌─ VIEW C: Profile Output ───────────────┐  │
│              │  │  Company Name + AI Badge               │  │
│              │  │  Industry Tag · Scale Tag              │  │
│              │  │  Field Grid (6 fields)                 │  │
│              │  │  [Copy JSON] [Save] [Edit]             │  │
│              │  └────────────────────────────────────────┘  │
└──────────────┴──────────────────────────────────────────────┘
```

The **Main Panel** is a state machine with three views:
- `view: 'form'` — Input form (default/empty state)
- `view: 'processing'` — AI pipeline animation
- `view: 'profile'` — Profile output card

---

## 5. Component Specifications

### 5.1 Topbar

- **Height:** 56px
- **Content:** Left-aligned logo icon + "ProfileAI" wordmark. Right-aligned theme toggle (sun/moon icon with smooth rotation transition).
- **Border:** 1px bottom border using `--bg-border`.
- **Sticky:** `position: sticky; top: 0; z-index: 50`.

---

### 5.2 Sidebar

- **Width:** 280px, fixed. Collapsible on mobile (hamburger toggle).
- **Top section:** Search input with magnifying glass icon. Placeholder: "Search profiles…"
- **Profile list item:**
  ```
  ┌────────────────────────────────┐
  │ ● Company Name           [×]  │
  │   Technology · Aug 15, 2026   │
  └────────────────────────────────┘
  ```
  - Left accent border (`3px solid --accent-primary`) when active.
  - Hover: `--bg-elevated` background with smooth `transition: background 150ms`.
  - Delete `[×]` appears only on hover (opacity transition).

- **Bottom:** `[+ New Profile]` button — ghost style, full width.

---

### 5.3 Input Form (View A)

Four source cards stacked vertically, each containing:
- **Icon + Source label** (e.g., `🔍 Google Search Snippet`)
- **Textarea** — 4 rows, `--bg-elevated` background, `--bg-border` border, `border-radius: 8px`
- Subtle left-side color accent per source:
  - Google → blue `#4285f4`
  - LinkedIn → `#0077b5`
  - Website → `#6366f1`
  - Registration → `#22c55e`

**Generate Profile CTA:**
- Full-width button, `border-radius: 10px`, `padding: 14px`.
- Background: `linear-gradient(135deg, #6366f1, #818cf8)`.
- Pulsing glow animation: `box-shadow: 0 0 0 0 rgba(99,102,241,0.4)` → `0 0 0 12px transparent` on `@keyframes pulse`.
- Disabled + spinner state while processing.

---

### 5.4 AI Pipeline Indicator (View B)

Four sequential steps displayed as a vertical stepper:

```
  ◉ Collecting sources            ✓  (completed — green)
  ◉ Analyzing data                ···  (active — spinning dot)
  ○ Structuring output               (pending — muted)
  ○ Finalizing profile               (pending — muted)
```

- Each step reveals with a fade-in + slight upward slide (`translateY(8px) → 0`).
- Active step has an animated ellipsis or spinner icon.
- Completed step: icon switches to `✓` checkmark with `--success` color.
- Overall timing: ~800ms per step.

---

### 5.5 Profile Output Card (View C)

**Card header:**
- Company name in `20px / 700 bold`.
- Right-aligned **AI Confidence Badge**: pill shape, gradient background `linear-gradient(90deg, #6366f1, #22c55e)`, showing e.g. `92% Confidence`.

**Industry + Scale tags:** Inline tag chips below the header.

**Field grid:** 2-column CSS grid layout.

```
┌──────────────┬──────────────────────────────────────┐
│ INDUSTRY     │  Technology / SaaS                   │
├──────────────┼──────────────────────────────────────┤
│ SCALE        │  Large Enterprise                    │
├──────────────┼──────────────────────────────────────┤
│ PRODUCTS     │  AI Solutions, Data Analytics        │
├──────────────┼──────────────────────────────────────┤
│ MARKETS      │  Global                              │
├──────────────┼──────────────────────────────────────┤
│ REGISTRATION │  Verified ✓                          │
├──────────────┼──────────────────────────────────────┤
│ LINKEDIN     │  "Leading provider of..."            │
└──────────────┴──────────────────────────────────────┘
```

**Action bar (bottom of card):**
- `[Copy as JSON]` — ghost button with copy icon; shows "Copied!" tooltip for 2s on click.
- `[Edit Inputs]` — returns to View A with the same source data.
- `[Delete Profile]` — red text button; shows inline confirmation "Are you sure? [Confirm] [Cancel]".

**Card entrance animation:** `opacity: 0 → 1` + `translateY(16px) → 0` over `400ms ease-out`.

---

### 5.6 Search Bar

- Full-width inside sidebar, `border-radius: 8px`.
- Icon: magnifying glass, `--text-muted` color, left-padded inside input.
- Filters profile list in real-time on `input` event.
- Empty state: "No profiles found" with a subtle ghost icon.

---

## 6. State Machine

```
         ┌──────────────┐
    ───▶  │   EMPTY      │  (no profiles, form shown, sidebar empty)
         └──────┬───────┘
                │ User fills form + clicks "Generate"
                ▼
         ┌──────────────┐
         │  PROCESSING  │  (pipeline animation playing)
         └──────┬───────┘
                │ Pipeline completes (~3.2s)
                ▼
         ┌──────────────┐
         │   PROFILE    │  (profile card shown, saved to DB)
         └──────┬───────┘
                │ User clicks "New Profile" or sidebar item
                ▼
         ┌──────────────┐
         │    FORM      │  (form cleared or pre-filled for editing)
         └──────────────┘
```

---

## 7. Keyword → Field Mapping (Mock AI Logic)

The AI simulation parses user inputs deterministically:

| Detected Keyword(s) | Mapped Field | Output Value |
|---|---|---|
| `saas`, `cloud`, `software`, `ai`, `tech` | Industry | Technology / SaaS |
| `bank`, `finance`, `invest`, `capital` | Industry | Finance |
| `manufactur`, `factory`, `produc` | Industry | Manufacturing |
| `health`, `pharma`, `clinic`, `medical` | Industry | Healthcare |
| `startup`, `seed`, `series a/b` | Scale | Startup |
| `sme`, `small`, `medium` | Scale | SME |
| `enterprise`, `corporation`, `global`, `headquarter` | Scale | Large Enterprise |
| `global`, `worldwide`, `international` | Market | Global |
| `domestic`, `local`, `vietnam`, `viet nam` | Market | Domestic |
| `verified`, `registered`, `certificate` | Registration | Verified ✓ |

A **Confidence Score** is calculated as: `60 + (number of matched keywords × 4)`, capped at 98%.

---

## 8. Micro-interaction Summary

| Element | Interaction | Duration | Easing |
|---|---|---|---|
| Sidebar profile item | Hover background + left border | 150ms | ease |
| Profile item delete `[×]` | Fade in on parent hover | 200ms | ease |
| Theme toggle icon | 180° rotation | 300ms | ease-in-out |
| CTA button | Pulse glow loop | 2000ms | ease-in-out, infinite |
| Pipeline step | Fade-in + slide up | 300ms | ease-out |
| Pipeline step icon | Spinner → checkmark swap | 200ms | ease |
| Profile card entrance | Fade-in + slide up | 400ms | ease-out |
| Copy button feedback | "Copied!" text swap + fade | 2000ms | ease |
| Delete confirm | Inline expand | 200ms | ease |

---

## 9. Responsive Behavior

| Breakpoint | Behavior |
|---|---|
| `> 1024px` | Full two-pane layout (sidebar fixed, main panel fluid) |
| `768px – 1024px` | Sidebar collapses to icon-only rail (280px → 56px) |
| `< 768px` | Sidebar hidden by default, accessible via hamburger menu overlay |

---

## 10. Accessibility

- All interactive elements have `aria-label` attributes.
- Focus rings use `outline: 2px solid --accent-primary` with `outline-offset: 2px`.
- Color contrast: all text/background pairs meet WCAG AA (4.5:1 minimum).
- Keyboard navigation: sidebar items and form fields are fully tab-accessible.
- Delete confirmation prevents accidental data loss.
