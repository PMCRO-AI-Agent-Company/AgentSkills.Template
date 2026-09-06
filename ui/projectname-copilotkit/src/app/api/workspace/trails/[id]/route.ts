// Server-side proxy to ProjectName.Api's read-only trail detail endpoint
// (AGENTSKILLS-IDE.md increment 4, partial). Same shape as the sibling
// app/api/workspace/skills/[...id]/route.ts, but a plain single-segment
// dynamic route since trail ids are one UUID, never a path.
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const base = process.env.WORKSPACE_API_URL ?? "http://projectname-api/api/workspace";

  try {
    const response = await fetch(`${base}/trails/${encodeURIComponent(id)}`, { cache: "no-store" });
    const body = await response.text();
    return new Response(body, {
      status: response.status,
      headers: { "content-type": "application/json" },
    });
  } catch (error) {
    return Response.json(
      { error: `workspace trail-detail backend unreachable: ${String(error)}` },
      { status: 502 },
    );
  }
}
