"use client";

import { CopilotChat } from "@copilotkit/react-core/v2";
import styles from "./page.module.css";

const sections = [
  ["◈", "Agents", "Directory of registered agent identities"],
  ["◇", "Skills", "Portable instructions, assets, references, scripts"],
  ["⌁", "MCP", "Filesystem, Terminal, and Playwright actuators"],
  ["◎", "Trails", "Governed runs, evidence, and outcomes"],
];

export default function Home() {
  return (
    <main className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <span className={styles.mark}>A</span>
          <div><strong>AgentSkills</strong><small>Workspace</small></div>
        </div>
        <nav className={styles.nav}>
          {sections.map(([icon, name, description]) => (
            <button className={styles.navItem} key={name} title={description}>
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
          <section className={styles.welcome}>
            <span className={styles.eyebrow}>COMMAND CENTER</span>
            <h2>Build with your agents, skills, and tools.</h2>
            <p>Use the assistant to inspect the workspace, plan changes, execute approved actions, and audit results.</p>
            <div className={styles.pills}><span>Planner</span><span>Maker</span><span>Checker</span><span>Reflector</span></div>
          </section>
          <section className={styles.chat}>
            <CopilotChat agentId="default" className="h-full" labels={{ welcomeMessageText: "Ask the ProjectName agent to inspect, plan, or build." }} />
          </section>
        </div>
      </section>
    </main>
  );
}
