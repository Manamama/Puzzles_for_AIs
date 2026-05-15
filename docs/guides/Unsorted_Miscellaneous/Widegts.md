On claude.ai, when you ask Claude to visualize something, it calls a tool called show_widget that renders HTML inline in the conversation. The HTML streams live - you see cards, charts, and sliders appear as tokens arrive.



Good question — let me search for what's current, as this may have evolved.The GitHub repo is the gold mine here. Someone reverse-engineered all 28 of Claude's internal tools — let me fetch it.Excellent — this is the most authoritative source available. Someone reverse-engineered all 28 of Claude.ai's internal tools across browser, desktop, and mobile. Here's the full hierarchy based on that:

---

**Parent nodes — the complete picture:**

**Interaction widgets**
`ask_user_input_v0` (what you saw), `message_compose_v1` (email/message drafter with variants)

**Visualizer** *(the new inline visual system)*
`diagram`, `mockup`, `interactive`, `chart`, `art`

**Inline charts** *(separate from Visualizer)*
`chart_display_v0` — older, distinct from the Visualizer chart module

**Search & data**
web search, image search, places search, maps display, sports data, Google Drive, weather, recipes

**Context tools**
`user_time_v0`, `user_location_v0`

**Memory**
`memory_user_edits`, `conversation_search`, `recent_chats`

**Calendar & device** *(mobile only)*
6 calendar tools + alarms + timers

**Computer use** *(desktop/browser)*
bash, file creation, artifacts, the skill system

**Meta-tool**
`tool_search` — used to discover and load other tools dynamically

---
 

Or: 


Input collection: ask_user_input_v0
Visualizer: read_me + show_widget (with the 5 modules)
Search & data: web_search, web_fetch, image_search, places_search, fetch_sports_data, weather_fetch
Maps: places_map_display_v0
Interaction/output: message_compose_v1, recipe_display_v0
Computer use: bash_tool, create_file, str_replace, view, present_files
MCP registry: search_mcp_registry, suggest_connectors
Artifacts: via create_file + present_files pipeline
So roughly 8 parent nodes — slightly different from the GitHub list, and notably missing the mobile-only calendar/alarm tools and the memory tools, which aren't loaded in this context.



Note: 
read_me is an internal setup step I call before generating any visual. It loads design guidelines — CSS variables, color ramps, typography rules, layout constraints — for whichever module I'm about to use (diagram, chart, etc.). It's essentially "read the style manual before drawing."

read_me (load design rules for module X) → show_widget (render the actual visual)

bash_tool → shell → python3 (or any other binary)




diagram — for explaining structure and relationships. Flowcharts, system architecture, process flows, org charts, concept maps. Useful when you want to understand how things connect — "show me the OAuth login flow", "diagram the layers of TCP/IP".
mockup — for UI previews without building anything. Forms, dashboards, app screens, card layouts. Useful when you want to visualize an interface before committing to code — "what would this settings page look like", "mock up a user profile card".
interactive — the most versatile and what TechRadar tested. The feature lets you create small tools with controls — sliders, toggles, selectors — that update the visual in real time. GitHub The coffee calculator, volcano cross-section, outfit generator from the article are all this module. Useful when you want a tiny working tool inside the conversation.
chart — for data visualization. Bar charts, line graphs, pie charts via Chart.js. Useful when you have numbers and want to see the pattern — "chart these sales figures", "plot this against time".
art — generative and illustrative SVG. Abstract visuals, algorithmic patterns, decorative graphics. Less "useful" in the productivity sense, more for visual thinking or aesthetics.




See https://github.com/Michaelliv/pi-generative-ui 
https://www.techradar.com/ai-platforms-assistants/claude/i-tried-claudes-new-interactive-visuals-feature-and-its-one-of-the-most-fun-ai-tricks-ive-seen

https://github.com/N1-AI/claude-hidden-toolkit



But then, also:


That widget is a separate system entirely — it's not one of the five Visualizer modules (`diagram`, `mockup`, `interactive`, `chart`, `art`).

It's called **`ask_user_input`** — a dedicated tool for collecting structured input from the user before responding. It has three question types: `single_select`, `multi_select` (what you saw), and `rank_priorities` (drag-and-drop ranking).

So the full map of "panels" in this conversation was actually:

| Widget | Tool | Purpose |
|---|---|---|
| Multiple choice checkboxes | `ask_user_input` | Clarify user's intent *before* answering |
| Inline visuals (diagrams, charts etc.) | `visualize:show_widget` | Enhance the *answer* with graphics |
| Recipes, weather, maps, sports, email composer | various dedicated tools | Domain-specific structured output |

The `ask_user_input` tool is conceptually the closest to the AskMe MCP you linked earlier — both are about *human-in-the-loop* input collection. The difference is that `ask_user_input` is native to claude.ai, while AskMe MCP is an external server you install yourself, primarily for Claude Code.


