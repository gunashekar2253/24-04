# Phase 6: Frontend UI/UX Design & Architecture

This document serves as the primary blueprint for executing **Phase 6** of the AI Financial Decision System. It translates the high-fidelity, premium aesthetic requirements into concrete CSS and component architecture plans.

## 1. Aesthetic Identity & Design System
**Name:** Finance AI
**Vibe:** "Silicon Valley" professional, data-dense (like Bloomberg Terminal), yet clean and modern (like Linear or Revolut).
**Theme:** High-contrast Dark Mode only.

### Color Palette (CSS Variables)
*   **Base Background:** Deep Charcoal (`#121212` to `#18181A`)
*   **Surface Panels:** Navy / Dark Slate (`#1E1E24` or `#1A1D24`)
*   **Primary Text:** High-contrast White (`#FFFFFF` or `#F7F7F8`)
*   **Secondary Text:** Light Gray/Silver (`#A1A1AA`)
*   **Profit / Success Accent:** Emerald Green (`#10B981` or `#00E676`)
*   **AI/Predictive Accent:** Neon Violet (`#8B5CF6` or `#B026FF`)
*   **Warning/Anomaly Accent:** Crimson or Coral (`#EF4444`)

### Visual Effects
*   **Glassmorphism:** Elements like modals, floating sidebars, and chat bubbles will utilize `backdrop-filter: blur(12px)` combined with extremely subtle white/violet semi-transparent borders.
*   **Typography:** We will import and universally apply **Inter** or **Outfit** via Google Fonts, ensuring crisp readability even at small sizes required for data-density.
*   **Micro-interactions:** Interactive elements (buttons, table rows, stock tickers) will feature `transition: all 0.2s ease`, with hover states that slightly elevate the element (`transform: translateY(-2px)`) and increase brightness.

---

## 2. Key Interface Layouts

### A. Executive Dashboard (`/dashboard`)
A grid-css controlled layout heavily utilizing space and clean borders to separate intelligence modules:
1.  **Metric Cards (Top Row):** Floating, minimalist boxes displaying "Monthly Income", "Savings Ratio", and "Budget Stability".
2.  **AI Risk Meter:** A dedicated canvas/SVG drawing a semi-circular gauge. The needle will point to Low, Medium, or High, populated dynamically from the ReLU TensorFlow model.
3.  **Interactive Spending Forecast:** Powered by `recharts`. A sleek, dark line-chart that overlays Prophet's predicted spending trendline (Neon Violet) over the historical spending path (White).
4.  **Anomaly Alerts:** A high-contrast side-panel. If an Isolation Forest anomaly is detected, it renders flashing coral warning metrics.

### B. Split-Screen Stock Analysis (`/stocks`)
1.  **Left Pane (Data & Charts):** yFinance pulled fundamental data alongside a professional candlestick (or sleek line) chart.
2.  **Right Pane (CrewAI Agent):** A dedicated console-like window where the specific Stock AI generates qualitative insights and official Buy/Hold/Sell signals in real-time.

### C. AI Financial Assistant (`/assistant`)
*   A chat interface mimicking premium generative AI apps.
*   Centered message thread with "user" bubbles (charcoal) and "AI" bubbles (frosted glass/violet).
*   **Finance-Only Status Hook:** At the top of the chat, a glowing green indicator stating "🔒 Finance Specialization Active" confirming the [query_classifier.py](file:///c:/project-at/backend/app/engine/query_classifier.py) protection is online.

### D. Goal Planning (`/goals`)
*   A visually impressive, timeline-based layout.
*   Circular progress rings outlining percentage completion for goals like "Retirement".
*   Horizontal milestone tracks displaying the mathematical output of [goal_planner.py](file:///c:/project-at/backend/app/engine/goal_planner.py).

---

## 3. Execution Scope
We will execute this strictly using **Vanilla CSS (`index.css`)** to ensure pixel-perfect control over the gradients, backdrop filters, and grid layouts without being constrained by unrequested tailwind utility classes. We will implement React Router for navigation and Axios for seamlessly pulling data from our FastAPI backend controllers.
