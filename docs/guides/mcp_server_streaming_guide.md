Track the tracker: 

try:
https://github.com/EchoingVesper/mcp-task-orchestrator


Tool: sequentialthinking
▼
To get live progress or status updates from an MCP server—without having to ask Gemini (the CLI) repeatedly—you need to tap the MCP transport’s streaming events directly. Here’s the step-by-step:

Use a Streamable Transport
• MCP supports three transports: stdio (batch), SSE (Server-Sent Events), and HTTP streaming.
• For live progress, SSE or HTTP streaming is ideal. In your ~/.gemini/settings.json you’d configure your MCP server with "url" (for HTTP/SSE) rather than a "command".

Example SSE config:

json
Copy
{
  "mcpServers": {
    "myTracker": {
      "url": "http://localhost:8080/events",
      "transport": "sse",
      "trust": true
    }
  }
}
Emit Progress from Your MCP Server
• Your server’s tool implementation must emit partial responses or custom “progress” parts as it works.
• With the MCP SDK (Node.js example), you’d do something like:

js
Copy
// inside your LongRunningTool handler
async function handler({ jobId }) {
  // send start event
  await server.sendProgress(jobId, { percent: 0, status: 'starting' });
  for (let i = 1; i <= 10; i++) {
    // do work…
    await server.sendProgress(jobId, { percent: i*10, status: `step ${i}` });
  }
  return { content: [{ type:'text', text:'Done' }] };
}
• The MCP SDK’s server transports for SSE or HTTP streaming let you push these “progress” parts as they happen.

Consume the Stream in Your Client Code
• Under the hood, the CLI’s SSE or streamable-HTTP transport will attach an event listener to the HTTP/SSE stream.
• If you’re writing your own client—rather than the pre-built CLI—you can parse these events yourself. For example, in JavaScript using EventSource:

js
Copy
const es = new EventSource('http://localhost:8080/events');
es.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.type === 'progress') {
    console.log(`Progress: ${msg.payload.percent}% – ${msg.payload.status}`);
  } else if (msg.type === 'tool_result') {
    console.log('Final result:', msg.payload);
    es.close();
  }
};
• In the CLI, you’d see interleaved parts in the LLM response. But if you hook into the transport layer, you can render a progress bar or dashboard instead.

Hook into the CLI’s Transport (Advanced)
• Gemini CLI’s MCPClientTransport implementations live in @modelcontextprotocol/sdk/client/{stdio,sse,streamableHttp}.js.
• You can extend or wrap these transports to register your own callbacks on partial “parts” of the result.
• For instance, subclass SSEClientTransport in your own tool, override onData(part) to emit('progress', part) whenever part.metadata.progress exists.

Summary
– Configure your server for SSE or HTTP streaming.
– Emit progress events in your MCP tool code.
– On the client side (CLI or custom), subscribe to the stream and render progress updates as they arrive—no manual “show me progress” calls required.

Copy
