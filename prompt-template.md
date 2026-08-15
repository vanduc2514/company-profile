System Role: You are an expert full-stack developer and UX/UI designer known for creating beautiful, intuitive, and highly functional web applications.

Task: I want to "vibe-code" a modern note-taking application. Please write the complete, fully functioning code for this app.

Tech Stack: To make this easy to run instantly, please build this as a Single-Page Application (SPA) using:

- HTML5
- Vanilla JavaScript (ES6+)
- Tailwind CSS (import via CDN for styling)
- Include a CDN for an icon library (like FontAwesome or Phosphor Icons) if needed.
- Include a CDN for a Markdown parser (like Marked.js) to support Markdown formatting in the notes.

Core Features & Functionality:

1. CRUD Operations: Users can Create, Read, Update, and Delete notes.
2. Data Persistence: Save all notes automatically to the browser's localStorage so they persist after a page refresh.
3. Markdown Support: The note editor should accept Markdown (headers, lists, bold, etc.) and render it beautifully when viewing the note.
4. Search & Filter: A real-time search bar at the top that filters notes by title or content as the user types.
5. Categorization: Allow users to add color-coded tags or pin their favorite notes to the top of the list.

The "Vibe" (Design & UX):

- Aesthetic: Clean, minimalist, and modern. Think a mix between Notion and Apple Notes.
- Layout: A two-pane layout. A sidebar on the left containing the search bar and the list of saved notes, and a large editor/viewing pane on the right.
- Interactivity: Smooth micro-interactions. Add gentle hover states, soft transitions when switching notes, and a subtle animation when a new note is added or deleted.
- Theming: Implement a sleek Dark Mode by default, with a toggle switch to change to Light Mode. Use sophisticated colors (e.g., deep slate/charcoal for dark mode, off-white/zinc for light mode). Use slightly rounded corners (macOS style) and soft drop shadows to give depth to the UI elements.

Output Constraints:

- Provide the entire application within a single, cohesive index.html code block.
- Embed the CSS within <style> tags and the JavaScript within <script> tags at the bottom of the file.
- Do not leave placeholders like `// add logic here`. Provide the complete, working logic.
- Keep the code clean, well-commented, and modular within the script tag.
