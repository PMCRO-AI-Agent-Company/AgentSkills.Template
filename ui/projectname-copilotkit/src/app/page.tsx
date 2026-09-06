"use client";

import { useState } from "react";
import { CopilotChat } from "@copilotkit/react-core/v2";
import styles from "./page.module.css";

type SectionId = "agents" | "skills" | "mcp" | "trails";

const sections: [SectionId, string, string, string][] = [
  ["agents", "◈", "Agents", "Directory of registered agent identities"],
  ["skills", "◇", "Skills", "Portable instructions, assets, references, scripts"],
  ["mcp", "⌁", "MCP", "Filesystem, Terminal, and Playwright actuators"],
  ["trails", "◎", "Trails", "Governed runs, evidence, and outcomes"],
];

type PackagingTarget = { target: string; path: string | null; status: string | null };
type AgentSummary = {
  id: string;
  kind: string;
  displayName: string;
  description: string;
  ownerRole: string;
  status: string;
  marketplaceVisible: boolean;
  skillCount: number;
  packaging: PackagingTarget[];
};
type SkillSummary = { id: string; name: string | null; description: string | null };
type McpServerSummary = { name: string; description: string };
type TrailSummary = {
  id: string;
  status: string;
  openedAt: string | null;
  sealedAt: string | null;
  seedIntent: string | null;
};
type QueueItemSummary = { id: string; priority: number | null; intent: string | null };
type GovernanceSummary = {
  trailsSealedCount: number;
  trailsOpenCount: number;
  trailsAbandonedCount: number;
  trailsOtherCount: number;
  recentTrails: TrailSummary[];
  pendingQueue: QueueItemSummary[];
};
type WorkspaceIndex = {
  repoRoot: string;
  agents: AgentSummary[];
  skills: SkillSummary[];
  mcpServers: McpServerSummary[];
  governance: GovernanceSummary;
  examples: string[];
};

function WorkspacePanel({
  section,
  data,
  loading,
  error,
}: {
  section: SectionId;
  data: WorkspaceIndex | null;
  loading: boolean;
  error: string | null;
}) {
  if (loading) return <p className={styles.panelStatus}>Loading workspace index...</p>;
  if (error) return <p className={styles.panelStatus}>Could not load workspace index: {error}</p>;
  if (!data) return null;

  if (section === "agents") {
    return (
      <ul className={styles.panelList}>
        {data.agents.map((a) => (
          <li key={a.id} className={styles.panelItem}>
            <div className={styles.panelItemHead}>
              <b>{a.displayName}</b>
              <span className={styles.panelBadge}>{a.status}</span>
            </div>
            <p>{a.description}</p>
            <small>{a.ownerRole} · {a.kind} · {a.skillCount} skill(s)</small>
          </li>
        ))}
        {data.agents.length === 0 && <p className={styles.panelStatus}>No agents found in .pmcro/directory/agents.yaml.</p>}
      </ul>
    );
  }

  if (section === "skills") {
    return (
      <ul className={styles.panelList}>
        {data.skills.map((s) => (
          <li key={s.id} className={styles.panelItem}>
            <b>{s.name ?? s.id}</b>
            <p>{s.description ?? "(no description in SKILL.md frontmatter)"}</p>
          </li>
        ))}
        {data.skills.length === 0 && <p className={styles.panelStatus}>No skills found under .agents/skills.</p>}
      </ul>
    );
  }

  if (section === "mcp") {
    return (
      <ul className={styles.panelList}>
        {data.mcpServers.map((m) => (
          <li key={m.name} className={styles.panelItem}>
            <b>{m.name}</b>
            <p>{m.description}</p>
          </li>
        ))}
        {data.mcpServers.length === 0 && <p className={styles.panelStatus}>No MCP servers found under mcp/.</p>}
      </ul>
    );
  }

  const g = data.governance;
  return (
    <div>
      <div className={styles.pills}>
        <span>{g.trailsSealedCount} sealed</span>
        <span>{g.trailsOpenCount} open</span>
        <span>{g.trailsAbandonedCount} abandoned</span>
        <span>{g.pendingQueue.length} queued</span>
      </div>
      <ul className={styles.panelList}>
        {g.recentTrails.map((t) => (
          <li key={t.id} className={styles.panelItem}>
            <div className={styles.panelItemHead}>
              <b>{t.id.slice(0, 8)}</b>
              <span className={styles.panelBadge}>{t.status}</span>
            </div>
            {t.seedIntent && <p>{t.seedIntent}</p>}
          </li>
        ))}
        {g.recentTrails.length === 0 && <p className={styles.panelStatus}>No trails found under .pmcro/trails.</p>}
      </ul>
      {g.pendingQueue.length > 0 && (
        <>
          <small>PENDING QUEUE</small>
          <ul className={styles.panelList}>
            {g.pendingQueue.map((q) => (
              <li key={q.id} className={styles.panelItem}>
                <b>{q.id}</b>
                {q.intent && <p>{q.intent}</p>}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default function Home() {
  const [activeSection, setActiveSection] = useState<SectionId | null>(null);
  const [index, setIndex] = useState<WorkspaceIndex | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetched lazily from the click handler (not a useEffect) - loading the
  // workspace index is a response to the user opening a panel, not a
  // synchronization concern, so it belongs in the event that triggers it.
  function loadIndexOnce() {
    if (index !== null || loading) return;
    setLoading(true);
    setError(null);
    fetch("/api/workspace")
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return (await res.json()) as WorkspaceIndex;
      })
      .then(setIndex)
      .catch((err) => setError(String(err)))
      .finally(() => setLoading(false));
  }

  function handleSectionClick(id: SectionId) {
    setActiveSection((current) => (current === id ? null : id));
    loadIndexOnce();
  }

  const activeMeta = sections.find(([id]) => id === activeSection);

  return (
    <main className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <span className={styles.mark}>A</span>
          <div><strong>AgentSkills</strong><small>Workspace</small></div>
        </div>
        <nav className={styles.nav}>
          {sections.map(([id, icon, name, description]) => (
            <button
              className={`${styles.navItem} ${activeSection === id ? styles.navItemActive : ""}`}
              key={id}
              title={description}
              onClick={() => handleSectionClick(id)}
            >
              <span>{icon}</span><b>{name}</b>
            </button>
          ))}
        </nav>
        <div className={styles.repoCard}>
          <small>WORKSPACE</small>
          <strong>ProjectName</strong>
          <span>MAF · Aspire · MCP</span>
        </div>
      </aside>

      <section className={styles.content}>
        <header className={styles.header}>
          <div><span className={styles.eyebrow}>AGENT DEVELOPMENT ENVIRONMENT</span><h1>ProjectName Agent Workspace</h1></div>
          <span className={styles.status}><i /> Local runtime</span>
        </header>
        <div className={styles.grid}>
          {activeMeta ? (
            <section className={styles.welcome}>
              <span className={styles.eyebrow}>{activeMeta[2].toUpperCase()}</span>
              <h2 className={styles.panelHeading}>{activeMeta[3]}</h2>
              <WorkspacePanel section={activeMeta[0]} data={index} loading={loading} error={error} />
            </section>
          ) : (
            <section className={styles.welcome}>
              <span className={styles.eyebrow}>COMMAND CENTER</span>
              <h2>Build with your agents, skills, and tools.</h2>
              <p>Use the assistant to inspect the workspace, plan changes, execute approved actions, and audit results.</p>
              <div className={styles.pills}><span>Planner</span><span>Maker</span><span>Checker</span><span>Reflector</span></div>
            </section>
          )}
          <section className={styles.chat}>
            <CopilotChat agentId="default" className="h-full" labels={{ welcomeMessageText: "Ask the ProjectName agent to inspect, plan, or build." }} />
          </section>
        </div>
      </section>
    </main>
  );
}
