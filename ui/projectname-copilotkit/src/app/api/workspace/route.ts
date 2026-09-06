// Server-side proxy to ProjectName.Api's read-only workspace index
// (AGENTSKILLS-IDE.md increment 1). Mirrors the existing
// app/api/copilotkit/[[...slug]]/route.ts pattern: the browser talks to
// this Next.js route, which talks to the backend using the Aspire
// service-discovery hostname the browser itself cannot resolve.
export async function GET() {
  const backend =
    process.env.WORKSPACE_API_URL ?? "http://projectname-api/api/workspace/index";

  try {
    const response = await fetch(backend, { cache: "no-store" });
    const body = await response.text();
    return new Response(body, {
      status: response.status,
      headers: { "content-type": "application/json" },
    });
  } catch (error) {
    return Response.json(
      { error: `workspace index backend unreachable: ${String(error)}` },
      { status: 502 },
    );
  }
}
