// Server-side proxy to ProjectName.Api's read-only workspace index
// (AGENTSKILLS-IDE.md increment 1). Mirrors the existing
// app/api/copilotkit/[[...slug]]/route.ts pattern: the browser talks to
// this Next.js route, which talks to the backend using the Aspire
// service-discovery hostname the browser itself cannot resolve.
//
// WORKSPACE_API_URL is the workspace API's base path (e.g.
// https://projectname-api/api/workspace) - this route appends /index; the
// sibling app/api/workspace/skills/[...id]/route.ts appends /skills/<id>.
export function workspaceApiBase() {
  return process.env.WORKSPACE_API_URL ?? "http://projectname-api/api/workspace";
}

export async function GET() {
  try {
    const response = await fetch(`${workspaceApiBase()}/index`, { cache: "no-store" });
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
