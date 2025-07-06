See https://askdev.ai/github/google-gemini/gemini-cli?trk=public_post_comment-text


It understands (ingests) PDFs and videos by now, but does not know how, so: 

  - **Image/PDF/Audio/Video files:** The tool can read common image types (PNG, JPEG, etc.), PDF, audio, and video files, returning them as base64 encoded data. These files _must_ be explicitly targeted by the `paths` or `include` patterns (e.g., by specifying the exact filename like `video.mp4` or a pattern like `*.mov`).




Here’s how “memory” in Gemini CLI works under the hood, and how you’d see it if it were exposed via an MCP server—or simply in its built-in form.

Model Context Protocol (MCP) in a Nutshell
• MCP is just a JSON-RPC–style protocol for “tool” discovery and execution.
• An MCP server publishes a list of named functions (tools), each with a JSON schema.
• The CLI’s mcp-client connects (via stdio, SSE or HTTP), fetches the tool schemas, and registers them.
• Each discovered tool becomes a DiscoveredMCPTool instance in the CLI’s global tool registry.

Built-in Memory vs. MCP-based Memory
A. Built-in Memory (MemoryTool)
– Lives in packages/core/src/tools/memoryTool.ts.
– Exposes a single save_memory tool. Under the covers it:
• Opens (or creates) a GEMINI.md file (by default in your home dir)
• Appends your “fact” under a “## Gemini Added Memories” section
– At runtime the CLI also calls loadServerHierarchicalMemory (in utils/memoryDiscovery.ts) to:
• Traverse upwards/downwards from your CWD plus the home directory
• Read and concatenate all GEMINI.md files (including imported sub-files)
• Inject that text as context before running your LLM prompt
– To the CLI it’s just another tool:
name: save_memory
description: “Save Memory”
parameters: { fact: string, path?: string }

B. MCP-based Memory (hypothetical or custom)
– You could spin up an MCP server whose sole tool is “get_memory”/“put_memory” backed by a database or vector store.
– In your ~/.gemini/settings.json you’d add under "mcpServers" something like: { "memoryServer": { "url": "http://localhost:8080/mcp", "trust": true } } – On startup the CLI’s discoverMcpTools() (in mcp-client.ts) will:
1. Connect to that URL
2. Fetch the list of tools (e.g. { name: "get_memory", inputSchema: {...} })
3. Wrap each in a DiscoveredMCPTool with serverName="memoryServer"
4. Register them in the same registry that holds MemoryTool and other built-ins
– You’d then see these tools in the CLI’s tool list just like any other MCP tool: get_memory (memoryServer MCP Server) put_memory (memoryServer MCP Server) – When you invoke one, DiscoveredMCPTool.execute() will package your args into an MCP function call, send it over the chosen transport, and unwrap the response.

Key Code Paths
• Discovery:
packages/core/src/tools/mcp-client.ts → discoverMcpTools() → connectAndDiscover() → uses @modelcontextprotocol/sdk to fetch CallableTools → mcpToTool() → ToolRegistry.registerTool().
• Execution wrapper:
packages/core/src/tools/mcp-tool.ts → DiscoveredMCPTool which extends BaseTool and implements execute() by calling mcpTool.callTool(...).
• Built-in Memory:
packages/core/src/tools/memoryTool.ts → MemoryTool.performAddMemoryEntry() writes to GEMINI.md.
• Hierarchical Loading:
packages/core/src/utils/memoryDiscovery.ts → loadServerHierarchicalMemory() finds all memory files and concatenates them.

—
In short: to Gemini CLI, memory—whether it’s the built-in file-based save_memory or a custom MCP memory server—is just another tool with a name, description and JSON schema. The MCP machinery discovers it, wraps it in a DiscoveredMCPTool, and lets you call it as part of your LLM workflow.
