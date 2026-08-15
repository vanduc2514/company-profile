**System Role:** You are an expert full-stack developer and UX/UI designer known for creating beautiful, intuitive, and highly functional web applications. You specialize in data-driven dashboards and internal enterprise tools.

---

**Task:** I want to "vibe-code" a modern **Automated Enterprise Customer Profile** web application. Please write the complete, fully functioning code for this app in a single file.

---

**Tech Stack:** Build this as a Single-Page Application (SPA) using:

- HTML5 (semantic, accessible markup)
- Vanilla JavaScript (ES6+)
- Tailwind CSS (import via CDN for all styling)
- FontAwesome or Phosphor Icons (via CDN for icons)
- No backend required — all data should be mocked or persisted via `localStorage`

---

**Application Context:**

This tool replaces the manual, inefficient process of building enterprise customer profiles. Human officers are currently overwhelmed collecting data from Google, LinkedIn, company websites, and business registration portals — especially for foreign companies. The app simulates an **AI-powered Assembly Line** that ingests raw inputs and outputs a clean, structured company profile, which is then saved to a persistent local database so no redundant research is needed in the future.

---

**Core Features & Functionality:**

1. **Input Form (Data Ingestion Panel)**
   - A clean input form where a user can paste or type raw data sourced from: Google Search snippets, LinkedIn summary, Company Website text, Business Registration info.
   - Each source should have its own labeled textarea or input section.
   - A prominent **"Generate Profile"** CTA button triggers the assembly line simulation.

2. **AI Processing Simulation**
   - After clicking "Generate Profile," show a multi-step animated progress indicator (e.g., "Collecting sources → Analyzing data → Structuring output → Done") with a brief delay between each step to simulate AI processing.
   - Use `setTimeout` to simulate the pipeline stages.

3. **Structured Profile Output**
   - Display the generated company profile in a clean, card-based layout with the following fields:
     - **Company Name**
     - **Industry / Field** (e.g., Technology, Finance)
     - **Company Scale** (e.g., Startup, SME, Large Enterprise)
     - **Key Products / Services**
     - **Target Markets** (e.g., Domestic, Global)
     - **LinkedIn Summary**
     - **Registration Status**
     - **AI Confidence Score** (a mocked percentage badge)
   - Use realistic mock data derived from the user's inputs (parse keywords from the textarea values to populate fields).

4. **Profile Database (localStorage)**
   - All generated profiles are saved automatically to `localStorage`.
   - A **"Saved Profiles"** sidebar or section lists all previously generated profiles by company name and date.
   - Users can click any saved profile to view its full details.
   - Users can **delete** individual profiles from the database.

5. **Search & Filter**
   - A real-time search bar that filters the saved profiles list by company name, industry, or market.

6. **Export**
   - A **"Copy as JSON"** button on each profile card that copies the structured data to the clipboard.

---

**The "Vibe" (Design & UX):**

- **Aesthetic:** Premium, enterprise-grade, and modern. Think a fusion of **Notion**, **Linear**, and a Bloomberg terminal — data-dense but visually breathable.
- **Layout:** Two-pane layout:
  - **Left Sidebar:** Search bar + list of saved profiles, with company name, industry tag, and creation date. Highlight the active profile.
  - **Right Main Panel:** Switches between the **Input Form** view and the **Profile Output** view.
- **Color Palette:** Dark mode by default using deep navy/charcoal tones (`#0f172a`, `#1e293b`), with electric blue/violet accents (`#6366f1`, `#818cf8`). Include a Light Mode toggle.
- **Typography:** Use the **Inter** font family (via Google Fonts CDN). Strong visual hierarchy with `font-semibold` labels and `text-muted` supporting text.
- **Micro-interactions:**
  - Smooth sidebar list hover & active states with a left accent border.
  - The profile output card fades/slides in after the AI pipeline completes.
  - Progress pipeline steps animate sequentially with a checkmark on completion.
  - Soft pulsing glow on the "Generate Profile" button.
- **Tags & Badges:** Color-coded industry tags (e.g., blue for Technology, green for Finance, orange for Manufacturing) and an AI confidence badge with a gradient fill.

---

**Output Constraints:**

- Deliver the **entire application within a single `index.html` file**.
- Embed all CSS within `<style>` tags and all JavaScript within `<script>` tags at the bottom.
- Do **not** leave placeholders like `// add logic here` — provide complete, working logic.
- The mock AI profile generation must be deterministic and driven by keyword parsing from the user's inputs (e.g., if the user types "SaaS" or "cloud" in any field, set Industry to "Technology / SaaS").
- Keep the code clean, well-commented, and modular within the `<script>` tag.
- The app must work fully offline with zero network dependencies except CDN imports.
