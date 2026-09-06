// Server-side proxy to ProjectName.Api's read-only skill detail endpoint
// (AGENTSKILLS-IDE.md increment 2). Same shape as the sibling
// app/api/workspace/route.ts, kept as its own small file rather than a
// shared import across route segments.
//
// params.id is a catch-all segment array (Next.js 16: params is a
// Promise - see https://nextjs.org/docs/app/api-reference/file-conventions/route,
// verified against the real docs before writing this, not guessed), e.g.
// ["reasoning", "chain-of-thought"] for /api/workspace/skills/reasoning/chain-of-thought.
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string[] }> },
) {
  const { id } = await params;
  const base = process.env.WORKSPACE_API_URL ?? "http://projectname-api/api/workspace";
  const skillPath = id.map(encodeURIComponent).join("/");

  try {
    const response = await fetch(`${base}/skills/${skillPath}`, { cache: "no-store" });
    const body = await response.text();
    return new Response(body, {
      status: response.status,
      headers: { "content-type": "application/json" },
    });
  } catch (error) {
    return Response.json(
      { error: `workspace skill-detail backend unreachable: ${String(error)}` },
      { status: 502 },
    );
  }
}
