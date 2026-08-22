/**
 * SentinelMem - Project Management Framework & Interactive Dashboard
 * Core Application Engine
 */

const STORAGE_KEY = 'sentinelmem_pm_framework_v1';

// Initial default state seeded from the semester specification
const defaultState = {
  activeTab: 'overview',
  lastUpdated: new Date().toISOString(),
  currentWeek: 1,
  currentSprint: 1,
  
  // 4 Main Phases
  phases: [
    {
      id: 1,
      name: 'Phase 1: Foundation & Threat Modeling',
      weeks: 'Weeks 1–3 (Aug 22 – Sep 18)',
      status: 'In Progress',
      color: 'cyan',
      description: 'Literature review sign-off, BibTeX compilation, threat model document, and development environments (Mem0, LangMem, FAISS).'
    },
    {
      id: 2,
      name: 'Phase 2: Attack Reproduction & Baselines',
      weeks: 'Weeks 4–7 (Sep 18 – Oct 16)',
      status: 'Upcoming',
      color: 'rose',
      description: 'Reproducing MINJA query-only attacks, sleeper/delayed-trigger attacks, and direct-write attacks across all 3 backends.'
    },
    {
      id: 3,
      name: 'Phase 3: Defense Design & Signal Fusion',
      weeks: 'Weeks 8–11 (Oct 16 – Nov 13)',
      status: 'Upcoming',
      color: 'purple',
      description: 'Multi-signal trust fusion (drift, temporal, provenance, credibility), retrieval-time policy enforcement, and dashboard prototype.'
    },
    {
      id: 4,
      name: 'Phase 4: Full Benchmarking & Paper Writeup',
      weeks: 'Weeks 12–16 (Nov 13 – Dec 11)',
      status: 'Upcoming',
      color: 'emerald',
      description: 'Comprehensive benchmarking suite, results analysis, 6000+ word research paper, guide approval, and open-source release.'
    }
  ],

  // Sprints 1 to 8
  sprints: [
    {
      id: 1,
      title: 'Sprint 1: Lit Review & Guide Approval',
      dates: 'Week 1–2 (Aug 22 – Sep 4)',
      phase: 1,
      objective: 'Complete 10-paper reference set, obtain guide sign-off, finalize all literature citations',
      completionCriteria: 'Guide-signed reference sheet, no arXiv papers in final set, all citations peer-reviewed venues',
      status: 'In Progress',
      tasks: [
        { id: 's1_t1', text: 'Verify all 10 papers exist & match characterizations (web search / Google Scholar)', completed: true },
        { id: 's1_t2', text: 'Compile final BibTeX entries & verified citations', completed: true },
        { id: 's1_t3', text: 'Submit literature review to guide for sign-off', completed: false },
        { id: 's1_t4', text: 'Lock paper title & abstract language', completed: true }
      ]
    },
    {
      id: 2,
      title: 'Sprint 2: Threat Model & Environment Setup',
      dates: 'Week 2–3 (Sep 4 – Sep 18)',
      phase: 1,
      objective: 'Finalize threat model, establish development environment, plan attack harnesses',
      completionCriteria: 'Threat model signed off, all 3 backends running locally, harness skeleton code & test suite',
      status: 'Upcoming',
      tasks: [
        { id: 's2_t1', text: 'Write formal threat model document (attacker capabilities, assumptions, attack surface)', completed: false },
        { id: 's2_t2', text: 'Set up Mem0, LangMem, FAISS environments on dev machine', completed: false },
        { id: 's2_t3', text: 'Design attack harness architecture (modular for 3 backends)', completed: false },
        { id: 's2_t4', text: 'Create test datasets & injection points', completed: false }
      ]
    },
    {
      id: 3,
      title: 'Sprint 3: MINJA Attack Implementation',
      dates: 'Week 4–5 (Sep 18 – Oct 2)',
      phase: 2,
      objective: 'Reproduce MINJA (query-only injection) attacks; achieve documented baseline success rates',
      completionCriteria: 'MINJA working on all 3 backends, success rates logged, attack logs reproducible',
      status: 'Upcoming',
      tasks: [
        { id: 's3_t1', text: 'Implement MINJA query-generation module (semantic-aware injections)', completed: false },
        { id: 's3_t2', text: 'Run attack on Mem0 backend (target: 98%+ injection success)', completed: false },
        { id: 's3_t3', text: 'Run attack on LangMem backend', completed: false },
        { id: 's3_t4', text: 'Run attack on FAISS backend', completed: false },
        { id: 's3_t5', text: 'Document baseline metrics & attack traces', completed: false }
      ]
    },
    {
      id: 4,
      title: 'Sprint 4: Sleeper + Direct-Write Attacks',
      dates: 'Week 6–7 (Oct 2 – Oct 16)',
      phase: 2,
      objective: 'Implement sleeper/delayed-trigger and direct-write attacks; establish comparative baseline',
      completionCriteria: 'All 3 attack types working, cross-backend comparison published, attack vectors documented',
      status: 'Upcoming',
      tasks: [
        { id: 's4_t1', text: 'Implement sleeper-poisoning attack (dormant trigger, time/session-based activation)', completed: false },
        { id: 's4_t2', text: 'Implement direct-write attack (if backend supports; baseline for comparison)', completed: false },
        { id: 's4_t3', text: 'Test on all 3 backends, document success rates', completed: false },
        { id: 's4_t4', text: 'Create comparative attack-success table (MINJA vs sleeper vs direct-write)', completed: false }
      ]
    },
    {
      id: 5,
      title: 'Sprint 5: Trust-Signal Layer Design & Implementation',
      dates: 'Week 8–9 (Oct 16 – Oct 30)',
      phase: 3,
      objective: 'Design & code multi-signal trust fusion; integrate retrieval-time policy checks',
      completionCriteria: 'Trust-scoring library ready, policy enforcement tested, no backend-specific workarounds',
      status: 'Upcoming',
      tasks: [
        { id: 's5_t1', text: 'Define trust signals: semantic drift, temporal anomaly, provenance, source credibility', completed: false },
        { id: 's5_t2', text: 'Build signal-extraction modules (backend-agnostic)', completed: false },
        { id: 's5_t3', text: 'Implement weighted fusion & scoring algorithm', completed: false },
        { id: 's5_t4', text: 'Create retrieval-time policy enforcement (block, quarantine, flag)', completed: false },
        { id: 's5_t5', text: 'Validate on all 3 backends with test cases', completed: false }
      ]
    },
    {
      id: 6,
      title: 'Sprint 6: Dashboard Prototype & Evaluation Framework',
      dates: 'Week 10–11 (Oct 30 – Nov 13)',
      phase: 3,
      objective: 'Build React security dashboard; finalize benchmarking & evaluation harness',
      completionCriteria: 'Dashboard prototype functional, evaluation harness automated, results pipeline ready',
      status: 'Upcoming',
      tasks: [
        { id: 's6_t1', text: 'Design dashboard wireframe (trust signals, policy decisions, attack logs)', completed: false },
        { id: 's6_t2', text: 'Implement React components (signal visualization, heatmaps, trace replay)', completed: false },
        { id: 's6_t3', text: 'Build full evaluation harness (attack × defense × metric combinations)', completed: false },
        { id: 's6_t4', text: 'Draft paper outline & figures (attack success vs. defense success)', completed: false }
      ]
    },
    {
      id: 7,
      title: 'Sprint 7: Full Benchmarking & Paper Writeup',
      dates: 'Week 12–14 (Nov 13 – Nov 27)',
      phase: 4,
      objective: 'Run full benchmark suite, write & refine research paper, prepare for submission',
      completionCriteria: 'Full paper draft (6000+ words), all results reproducible, guide feedback incorporated',
      status: 'Upcoming',
      tasks: [
        { id: 's7_t1', text: 'Run full benchmarking: attack success, defense efficacy, false-positive rate, latency', completed: false },
        { id: 's7_t2', text: 'Analyze results, identify edge cases & failure modes', completed: false },
        { id: 's7_t3', text: 'Write paper sections: intro, related work, methodology, results, discussion', completed: false },
        { id: 's7_t4', text: 'Create final figures & tables for paper', completed: false },
        { id: 's7_t5', text: 'Submit to guide for review & feedback', completed: false }
      ]
    },
    {
      id: 8,
      title: 'Sprint 8: Open-Source Release & Presentation',
      dates: 'Week 15–16 (Nov 27 – Dec 11)',
      phase: 4,
      objective: 'Package SentinelMem as open-source repo, finalize presentation, submit paper',
      completionCriteria: 'GitHub repo live, paper submitted, presentation slides final, all deliverables documented',
      status: 'Upcoming',
      tasks: [
        { id: 's8_t1', text: 'Clean up codebase, add documentation & README', completed: false },
        { id: 's8_t2', text: 'Publish GitHub repo (public or org-private per advisor preference)', completed: false },
        { id: 's8_t3', text: 'Create presentation slides (methodology, results, impact)', completed: false },
        { id: 's8_t4', text: 'Finalize & submit research paper (with full guide approval)', completed: false },
        { id: 's8_t5', text: 'Prepare for presentation or defense', completed: false }
      ]
    }
  ],

  // Checklists
  retrospectiveTasks: [
    { id: 'retro_1', title: 'Title locked', detail: 'SentinelMem: Cross-Backend Defense Against Memory Poisoning in LLM Agents', status: 'Completed', completed: true },
    { id: 'retro_2', title: 'Literature review', detail: '11 papers analyzed, comparative matrix + gap analysis compiled', status: 'Completed', completed: true },
    { id: 'retro_3', title: 'Reference sheet', detail: '10 peer-reviewed papers with BibTeX, abstracts, download links ready for guide sign-off', status: 'Pending approval', completed: false },
    { id: 'retro_4', title: 'PowerPoint deck', detail: 'Title, MINJA figures (98.2%, 76.8%), jargon fixes, OWASP citation finalized', status: 'Completed', completed: true },
    { id: 'retro_5', title: 'Word report', detail: 'Three embedded tables (trust signals, defense comparison, lit gaps) production-ready', status: 'Completed', completed: true },
    { id: 'retro_6', title: 'Research gap identified', detail: 'Cross-backend retrieval-time memory trust governance not covered in prior work', status: 'Completed', completed: true }
  ],

  implementationTasks: [
    { id: 'impl_1', title: 'Attack harness module', detail: 'Query-generation, injection strategies, success metric', estHours: 20, actHours: 0, deadline: 'Week 5 end', completed: false },
    { id: 'impl_2', title: 'Mem0 integration', detail: 'Initialize, poison, retrieve—test all 3 attack types', estHours: 12, actHours: 0, deadline: 'Week 6 end', completed: false },
    { id: 'impl_3', title: 'LangMem integration', detail: 'Same harness, adapt to LangMem API', estHours: 10, actHours: 0, deadline: 'Week 7 end', completed: false },
    { id: 'impl_4', title: 'FAISS integration', detail: 'Custom vector DB, attack adaptation', estHours: 14, actHours: 0, deadline: 'Week 7 end', completed: false },
    { id: 'impl_5', title: 'Trust-signal library', detail: 'Semantic drift, temporal anomaly, provenance, credibility scoring', estHours: 30, actHours: 0, deadline: 'Week 9 end', completed: false },
    { id: 'impl_6', title: 'Policy enforcement layer', detail: 'Retrieval-time blocking, quarantine logic', estHours: 20, actHours: 0, deadline: 'Week 10 end', completed: false },
    { id: 'impl_7', title: 'Multi-backend abstraction', detail: 'Backend-agnostic retrieval interface', estHours: 16, actHours: 0, deadline: 'Week 10 end', completed: false }
  ],

  researchTasks: [
    { id: 'res_1', title: 'Verify all 10 papers', detail: 'Check DOI, confirm venue, match characterizations', estHours: 5, actHours: 4, deadline: 'Week 2 end', completed: true },
    { id: 'res_2', title: 'Formal threat model', detail: 'Attacker model, assumptions, attack surface definition', estHours: 8, actHours: 0, deadline: 'Week 3 end', completed: false },
    { id: 'res_3', title: 'Guide sign-off on lit review', detail: 'Submit, incorporate feedback', estHours: 2, actHours: 0, deadline: 'Week 3 end', completed: false },
    { id: 'res_4', title: 'Benchmarking framework design', detail: 'Metrics (attack success, defense success, false positives, latency)', estHours: 8, actHours: 0, deadline: 'Week 6 end', completed: false },
    { id: 'res_5', title: 'Attack × defense matrix', detail: 'Plan experiment combinations', estHours: 4, actHours: 0, deadline: 'Week 8 end', completed: false },
    { id: 'res_6', title: 'Full benchmarking run', detail: 'Execute all experiments, log results', estHours: 40, actHours: 0, deadline: 'Week 14 mid', completed: false },
    { id: 'res_7', title: 'Results analysis', detail: 'Interpret metrics, identify outliers & patterns', estHours: 16, actHours: 0, deadline: 'Week 14 end', completed: false },
    { id: 'res_8', title: 'Paper writeup (all sections)', detail: 'Intro, related work, methodology, results, discussion (6k+ words)', estHours: 34, actHours: 0, deadline: 'Week 13 end', completed: false },
    { id: 'res_9', title: 'Guide review & final submission', detail: 'Revise per feedback, format, verify citations', estHours: 8, actHours: 0, deadline: 'Week 15 end', completed: false }
  ],

  // Weekly Tracking History & Live Editor
  weeklyLogs: [
    {
      id: 'w1_log',
      week: 'Week 1 (Aug 22 – Aug 28)',
      date: '2026-08-22',
      completedTasks: '• Locked paper title and abstract language\n• Verified 10-paper reference set against peer-reviewed criteria\n• Built Project Management Framework & Interactive Dashboard',
      blockers: '• Pending guide meeting to formally sign off reference sheet',
      risks: '• High: Attack reproduction schedule dependency on Phase 2 start',
      priorities: '• Submit literature review & reference sheet for guide approval\n• Begin threat model document draft',
      plannedHours: 10,
      actualHours: 9,
      varianceHours: -1,
      variancePercent: -10,
      attackSuccessMem0: 'N/A',
      defenseEfficacy: 'N/A',
      linesOfCode: '350'
    }
  ],

  // Risks & Mitigations
  risks: [
    {
      id: 'r1',
      severity: 'High',
      title: 'Attack reproduction slower than planned',
      impact: 'Delays defense design by 1–2 weeks; compresses Phase 4 writeup and benchmarking timeline.',
      mitigation: 'Start attack harness in Week 2 in parallel with threat model; pre-stage test datasets; have fallback synthetic attack benchmark if real backends behave unexpectedly.',
      status: 'Active Mitigation',
      owner: 'Core Dev'
    },
    {
      id: 'r2',
      severity: 'High',
      title: 'Trust-signal extraction complexity underestimated',
      impact: 'Defense quality suffers or Phase 3 timeline slips beyond Week 10.',
      mitigation: 'Prototype signal design in Week 7; run early efficacy tests; prioritize top 2–3 signals (semantic drift & temporal anomaly) if all cannot finish by Week 9.',
      status: 'Active Mitigation',
      owner: 'Core Dev'
    },
    {
      id: 'r3',
      severity: 'Medium',
      title: 'Guide feedback on paper arrives late (Week 14+)',
      impact: 'Final revisions must compress into Week 15, risking submission quality.',
      mitigation: 'Submit preliminary paper draft by Week 13 mid; ask guide for preliminary methodology feedback by Week 12 end.',
      status: 'Monitored',
      owner: 'Author'
    },
    {
      id: 'r4',
      severity: 'Medium',
      title: 'Benchmarking infrastructure failures (crashes, timeouts)',
      impact: 'Results delayed, reproducibility compromised.',
      mitigation: 'Build result logging & recovery in Week 9; run dry runs in Week 11; maintain manual CSV result fallback.',
      status: 'Monitored',
      owner: 'Core Dev'
    },
    {
      id: 'r5',
      severity: 'Medium',
      title: 'Team member availability / sickness',
      impact: 'Critical tasks blocked on single points of failure.',
      mitigation: 'Cross-document all code & decisions weekly; keep pairing sessions on Phases 2–3; maintain clear README for context handoff.',
      status: 'Monitored',
      owner: 'Team'
    },
    {
      id: 'r6',
      severity: 'Medium',
      title: 'Backend API changes (Mem0 / LangMem upstream updates)',
      impact: 'Integration code breaks unexpectedly during attack evaluation.',
      mitigation: 'Pin all package versions in requirements.txt / lockfiles; maintain local mocked harness for regression testing.',
      status: 'Monitored',
      owner: 'Core Dev'
    },
    {
      id: 'r7',
      severity: 'Medium',
      title: 'Direct-write attack not universally supported across backends',
      impact: 'Comparative matrix has asymmetric or empty cells.',
      mitigation: 'Define clear abstraction layer distinguishing direct-write backends vs. query-only memory backends.',
      status: 'Monitored',
      owner: 'Core Dev'
    },
    {
      id: 'r8',
      severity: 'Low',
      title: 'False-positive rate too high under trust scoring',
      impact: 'Benign queries inappropriately quarantined.',
      mitigation: 'Tune threshold dynamically; provide tiered policy enforcement (Flag vs. Quarantine vs. Block).',
      status: 'Monitored',
      owner: 'Core Dev'
    },
    {
      id: 'r9',
      severity: 'Low',
      title: 'Formatting and template mismatches at submission',
      impact: 'Last-minute scrambling before conference/journal deadline.',
      mitigation: 'Use standard IEEE/ACM LaTeX templates from Week 11; compile continuously with Overleaf/local TeX.',
      status: 'Monitored',
      owner: 'Author'
    }
  ],

  // Critical path & Buffers
  criticalPath: [
    { phase: 'Phase 1', weeks: 'Weeks 1–3', desc: 'Lit review signed & Threat Model', forwardImpact: 'Unblocks Phase 2 & 3' },
    { phase: 'Phase 2', weeks: 'Weeks 4–7', desc: 'Attack baselines reproduced (MINJA, Sleeper)', forwardImpact: 'Blocks Phase 3 design decisions' },
    { phase: 'Phase 3', weeks: 'Weeks 8–10', desc: 'Defense Core & Multi-Signal Fusion', forwardImpact: 'Blocks Benchmarking & Paper metrics' },
    { phase: 'Phase 4', weeks: 'Weeks 12–14', desc: 'Full Benchmark + Paper Draft (6k+ words)', forwardImpact: 'Blocks Final Submission' }
  ]
};

// Global App State
let state = loadState();

function loadState() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      // Merge with default in case of new properties
      return { ...defaultState, ...parsed };
    }
  } catch (e) {
    console.error('Failed to load state from localStorage', e);
  }
  return JSON.parse(JSON.stringify(defaultState));
}

function saveState() {
  state.lastUpdated = new Date().toISOString();
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save state to localStorage', e);
  }
  renderApp();
}

// Reset state
function resetState() {
  if (confirm('Are you sure you want to reset the dashboard to default template values? All custom tracking logs and checked items will be reset.')) {
    state = JSON.parse(JSON.stringify(defaultState));
    saveState();
  }
}

// Export State to JSON
function exportStateJSON() {
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", `sentinelmem_tracker_backup_${new Date().toISOString().split('T')[0]}.json`);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
}

// Import State from JSON
function importStateJSON(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const imported = JSON.parse(e.target.result);
      if (imported.sprints && imported.phases) {
        state = imported;
        saveState();
        alert('Dashboard state successfully imported!');
      } else {
        alert('Invalid JSON backup format.');
      }
    } catch (err) {
      alert('Error parsing JSON backup file.');
    }
  };
  reader.readAsText(file);
}

// Switch Tab
function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabId);
  });
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.toggle('hidden', pane.id !== `tab-${tabId}`);
  });
  saveState();
}

// Helper to compute project metrics
function computeMetrics() {
  // Sprints
  let totalSprintTasks = 0;
  let completedSprintTasks = 0;
  state.sprints.forEach(s => {
    s.tasks.forEach(t => {
      totalSprintTasks++;
      if (t.completed) completedSprintTasks++;
    });
  });

  // Implementation hours
  let totalImplHours = 0;
  let doneImplHours = 0;
  state.implementationTasks.forEach(t => {
    totalImplHours += Number(t.estHours) || 0;
    if (t.completed) doneImplHours += Number(t.estHours) || 0;
  });

  // Research hours
  let totalResHours = 0;
  let doneResHours = 0;
  state.researchTasks.forEach(t => {
    totalResHours += Number(t.estHours) || 0;
    if (t.completed) doneResHours += Number(t.estHours) || 0;
  });

  const totalEffortHours = totalImplHours + totalResHours;
  const completedEffortHours = doneImplHours + doneResHours;
  const overallEffortPct = totalEffortHours > 0 ? Math.round((completedEffortHours / totalEffortHours) * 100) : 0;
  const sprintProgressPct = totalSprintTasks > 0 ? Math.round((completedSprintTasks / totalSprintTasks) * 100) : 0;

  // Escalation alert status
  const currentSprintObj = state.sprints.find(s => s.id === state.currentSprint) || state.sprints[0];
  const refSheetPending = state.retrospectiveTasks.find(t => t.id === 'retro_3' && !t.completed);

  return {
    totalSprintTasks,
    completedSprintTasks,
    sprintProgressPct,
    totalImplHours,
    doneImplHours,
    totalResHours,
    doneResHours,
    totalEffortHours,
    completedEffortHours,
    overallEffortPct,
    currentSprintObj,
    refSheetPending
  };
}

// Render Overview Tab
function renderOverview(metrics) {
  const container = document.getElementById('overview-container');
  if (!container) return;

  const currentPhase = state.phases[0]; // Phase 1 active

  container.innerHTML = `
    <!-- Top KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="glass-card p-5 border-l-4 border-cyan-500">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-cyan-400">Current Phase</span>
          <span class="px-2 py-0.5 text-xs font-medium bg-cyan-900/60 text-cyan-200 rounded">Phase 1</span>
        </div>
        <div class="mt-2 text-xl font-bold text-white">Foundation & Threat Model</div>
        <p class="text-xs text-gray-400 mt-1">Weeks 1–3 (Aug 22 – Sep 18)</p>
        <div class="mt-3 flex items-center justify-between text-xs text-gray-300">
          <span>Sprint 1 of 8 Active</span>
          <span class="text-cyan-400 font-semibold">On Track</span>
        </div>
      </div>

      <div class="glass-card p-5 border-l-4 border-blue-500">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-blue-400">Overall Effort Done</span>
          <span class="text-xs text-blue-300 font-mono">${metrics.completedEffortHours} / ${metrics.totalEffortHours} hrs</span>
        </div>
        <div class="mt-2 text-2xl font-bold text-white">${metrics.overallEffortPct}%</div>
        <div class="w-full bg-gray-700 h-2 rounded-full mt-3 overflow-hidden">
          <div class="bg-blue-500 h-2 rounded-full progress-fill" style="width: ${metrics.overallEffortPct}%"></div>
        </div>
        <p class="text-xs text-gray-400 mt-2">Implementation (${metrics.doneImplHours}/${metrics.totalImplHours}h) + Research (${metrics.doneResHours}/${metrics.totalResHours}h)</p>
      </div>

      <div class="glass-card p-5 border-l-4 border-purple-500">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-purple-400">Sprint Tasks</span>
          <span class="text-xs text-purple-300 font-mono">${metrics.completedSprintTasks} / ${metrics.totalSprintTasks} done</span>
        </div>
        <div class="mt-2 text-2xl font-bold text-white">${metrics.sprintProgressPct}%</div>
        <div class="w-full bg-gray-700 h-2 rounded-full mt-3 overflow-hidden">
          <div class="bg-purple-500 h-2 rounded-full progress-fill" style="width: ${metrics.sprintProgressPct}%"></div>
        </div>
        <p class="text-xs text-gray-400 mt-2">Sprint 1: 3 of 4 initial items verified</p>
      </div>

      <div class="glass-card p-5 border-l-4 border-amber-500">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-amber-400">Critical Path Status</span>
          <span class="px-2 py-0.5 text-xs font-medium bg-amber-900/60 text-amber-200 rounded">Attention</span>
        </div>
        <div class="mt-2 text-lg font-bold text-white">Guide Sign-Off Pending</div>
        <p class="text-xs text-gray-400 mt-1">10-paper reference sheet awaiting advisor approval to unblock Phase 2.</p>
        <div class="mt-2">
          <a href="#checklists" onclick="switchTab('checklists')" class="text-xs text-amber-400 hover:underline">View Retrospective Checklist &rarr;</a>
        </div>
      </div>
    </div>

    <!-- Active Week 1 Action Plan Callout -->
    <div class="glass-card p-6 mb-6 border-cyan-500/40 bg-gradient-to-r from-cyan-950/30 to-blue-950/30">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></span>
            <h3 class="text-lg font-bold text-white">Immediate Focus: Week 1 Action Checklist</h3>
          </div>
          <p class="text-sm text-gray-300 mt-1">Execute these 4 priorities to firmly lock the foundation before Phase 2 attack reproduction:</p>
        </div>
        <button onclick="switchTab('weekly')" class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-semibold transition-colors flex items-center gap-2">
          <span>Weekly Tracker</span>
          <span>&rarr;</span>
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mt-4">
        <div class="p-3 bg-gray-800/80 rounded-lg border border-gray-700">
          <div class="text-xs font-semibold text-cyan-400">1. Lock Framework</div>
          <p class="text-xs text-gray-300 mt-1">Print or bookmark this interactive dashboard as the single source of truth.</p>
          <span class="inline-block mt-2 px-2 py-0.5 text-[10px] bg-emerald-900/60 text-emerald-300 rounded font-medium">Completed</span>
        </div>
        <div class="p-3 bg-gray-800/80 rounded-lg border border-gray-700">
          <div class="text-xs font-semibold text-amber-400">2. Guide Sign-off</div>
          <p class="text-xs text-gray-300 mt-1">Get advisor approval on 10-paper reference set (peer-reviewed venues, no arXiv).</p>
          <span class="inline-block mt-2 px-2 py-0.5 text-[10px] bg-amber-900/60 text-amber-300 rounded font-medium">Pending Sign-off</span>
        </div>
        <div class="p-3 bg-gray-800/80 rounded-lg border border-gray-700">
          <div class="text-xs font-semibold text-purple-400">3. Check-ins Cadence</div>
          <p class="text-xs text-gray-300 mt-1">Schedule 30-min monthly check-ins with guide: Weeks 5, 9, 13.</p>
          <span class="inline-block mt-2 px-2 py-0.5 text-[10px] bg-purple-900/60 text-purple-300 rounded font-medium">In Progress</span>
        </div>
        <div class="p-3 bg-gray-800/80 rounded-lg border border-gray-700">
          <div class="text-xs font-semibold text-blue-400">4. Friday Reminder</div>
          <p class="text-xs text-gray-300 mt-1">Set recurring Friday EOD alert to fill status update & monitor variance.</p>
          <span class="inline-block mt-2 px-2 py-0.5 text-[10px] bg-blue-900/60 text-blue-300 rounded font-medium">Ready</span>
        </div>
      </div>
    </div>

    <!-- 4 Phases Visual Timeline -->
    <div class="glass-card p-6 mb-6">
      <h3 class="text-base font-semibold text-white mb-4 flex items-center justify-between">
        <span>Semester Phases & Milestone Roadmap (16 Weeks)</span>
        <span class="text-xs text-gray-400 font-normal">Aug 22 – Dec 11</span>
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        ${state.phases.map(p => `
          <div class="p-4 rounded-lg bg-gray-800/50 border border-${p.color}-500/30 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <span class="text-xs font-semibold text-${p.color}-400">${p.name.split(':')[0]}</span>
                <span class="text-[10px] px-2 py-0.5 rounded font-medium ${p.status === 'In Progress' ? 'bg-cyan-900/80 text-cyan-200 animate-pulse' : 'bg-gray-700 text-gray-300'}">${p.status}</span>
              </div>
              <h4 class="text-sm font-bold text-white mt-1">${p.name.split(':')[1]}</h4>
              <p class="text-xs text-gray-400 mt-1 font-mono">${p.weeks}</p>
              <p class="text-xs text-gray-300 mt-2">${p.description}</p>
            </div>
            <div class="mt-4 pt-3 border-t border-gray-700 flex items-center justify-between text-xs">
              <span class="text-gray-400">Sprints: ${p.id === 1 ? '1–2' : p.id === 2 ? '3–4' : p.id === 3 ? '5–6' : '7–8'}</span>
              <button onclick="switchTab('sprints')" class="text-${p.color}-400 hover:underline">View Sprints &rarr;</button>
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- Critical Path & Escalation Snapshot -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="glass-card p-6">
        <h3 class="text-base font-semibold text-white mb-3 flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
          <span>Critical Path Dependencies (Red Path)</span>
        </h3>
        <p class="text-xs text-gray-400 mb-4">Any slip in Phase 2–3 cascades into paper writing and final benchmark verification.</p>
        
        <div class="space-y-3">
          ${state.criticalPath.map((cp, idx) => `
            <div class="flex items-start gap-3 p-2.5 bg-gray-800/40 rounded border border-gray-700/50">
              <span class="px-2 py-1 bg-rose-950/80 border border-rose-600/40 text-rose-300 font-mono text-xs rounded font-bold">W${idx * 3 + 1}–${idx * 3 + 3}</span>
              <div class="flex-1">
                <div class="text-xs font-semibold text-white">${cp.phase}: ${cp.desc}</div>
                <div class="text-[11px] text-rose-400 mt-0.5">&rarr; Impact: ${cp.forwardImpact}</div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="glass-card p-6">
        <h3 class="text-base font-semibold text-white mb-3 flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
          <span>Escalation Triggers & Early Warnings</span>
        </h3>
        <p class="text-xs text-gray-400 mb-4">Immediate red flags requiring guide escalation or scope adjustment:</p>

        <div class="space-y-2 text-xs">
          <div class="p-2.5 bg-rose-950/40 border border-rose-800/40 rounded text-gray-300 flex items-start gap-2">
            <span class="text-rose-400 font-bold">✗</span>
            <div><strong class="text-rose-200">Attack baseline unknown by Week 7 end:</strong> Cannot proceed to defense design; escalate immediately.</div>
          </div>
          <div class="p-2.5 bg-rose-950/40 border border-rose-800/40 rounded text-gray-300 flex items-start gap-2">
            <span class="text-rose-400 font-bold">✗</span>
            <div><strong class="text-rose-200">Trust-signal library incomplete by Week 10:</strong> Defense efficacy compromised; activate contingency.</div>
          </div>
          <div class="p-2.5 bg-amber-950/40 border border-amber-800/40 rounded text-gray-300 flex items-start gap-2">
            <span class="text-amber-400 font-bold">!</span>
            <div><strong class="text-amber-200">Paper draft missing by Week 13 end:</strong> Compress secondary sections or defer ablations to appendix.</div>
          </div>
          <div class="p-2.5 bg-amber-950/40 border border-amber-800/40 rounded text-gray-300 flex items-start gap-2">
            <span class="text-amber-400 font-bold">!</span>
            <div><strong class="text-amber-200">Cumulative hour variance &gt;25% over 2 sprints:</strong> Trigger scope reduction protocol.</div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Render Sprints Tab
function renderSprints() {
  const container = document.getElementById('sprints-container');
  if (!container) return;

  container.innerHTML = `
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-6 gap-4">
      <div>
        <h2 class="text-xl font-bold text-white">Sprint Execution Plan (Sprints 1–8)</h2>
        <p class="text-sm text-gray-400 mt-1">Week-level commitments with granular task checklists and completion sign-off criteria.</p>
      </div>
      <div class="flex items-center gap-3 text-xs">
        <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Phase 1</span>
        <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span> Phase 2</span>
        <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span> Phase 3</span>
        <span class="flex items-center gap-1.5 text-gray-300"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> Phase 4</span>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      ${state.sprints.map(s => {
        const totalTasks = s.tasks.length;
        const doneTasks = s.tasks.filter(t => t.completed).length;
        const pct = totalTasks > 0 ? Math.round((doneTasks / totalTasks) * 100) : 0;
        const isComplete = totalTasks > 0 && doneTasks === totalTasks;

        const phaseColor = s.phase === 1 ? 'cyan' : s.phase === 2 ? 'rose' : s.phase === 3 ? 'purple' : 'emerald';

        return `
          <div class="glass-card p-5 border-t-4 border-${phaseColor}-500 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 text-xs font-semibold bg-gray-800 text-${phaseColor}-400 rounded border border-${phaseColor}-500/30">
                  Phase ${s.phase}
                </span>
                <span class="text-xs font-mono text-gray-400">${s.dates}</span>
              </div>

              <h3 class="text-lg font-bold text-white mt-2">${s.title}</h3>
              <p class="text-xs text-gray-300 mt-1 italic"><strong class="text-gray-200">Objective:</strong> ${s.objective}</p>

              <!-- Progress bar -->
              <div class="mt-3">
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-gray-400">Tasks Completed</span>
                  <span class="font-mono text-${phaseColor}-400">${doneTasks}/${totalTasks} (${pct}%)</span>
                </div>
                <div class="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-${phaseColor}-500 h-1.5 rounded-full progress-fill" style="width: ${pct}%"></div>
                </div>
              </div>

              <!-- Task checklist -->
              <div class="mt-4 space-y-2">
                ${s.tasks.map(t => `
                  <label class="flex items-start gap-2.5 p-2 bg-gray-800/40 hover:bg-gray-800/70 rounded cursor-pointer transition-colors">
                    <input type="checkbox" class="custom-checkbox mt-0.5" 
                           ${t.completed ? 'checked' : ''} 
                           onchange="toggleSprintTask(${s.id}, '${t.id}')">
                    <span class="text-xs ${t.completed ? 'line-through text-gray-500' : 'text-gray-200'}">${t.text}</span>
                  </label>
                `).join('')}
              </div>
            </div>

            <!-- Completion Criteria Footer -->
            <div class="mt-4 pt-3 border-t border-gray-700/60">
              <div class="text-[11px] text-gray-400">
                <strong class="text-${phaseColor}-300">Completion Criteria:</strong> ${s.completionCriteria}
              </div>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function toggleSprintTask(sprintId, taskId) {
  const sprint = state.sprints.find(s => s.id === sprintId);
  if (sprint) {
    const task = sprint.tasks.find(t => t.id === taskId);
    if (task) {
      task.completed = !task.completed;
      // update sprint status
      const allDone = sprint.tasks.every(t => t.completed);
      const someDone = sprint.tasks.some(t => t.completed);
      sprint.status = allDone ? 'Completed' : someDone ? 'In Progress' : 'Upcoming';
      saveState();
    }
  }
}

// Render Checklists Tab
function renderChecklists(metrics) {
  const container = document.getElementById('checklists-container');
  if (!container) return;

  container.innerHTML = `
    <div class="mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-bold text-white">Three-Tier Project Checklists</h2>
        <p class="text-sm text-gray-400 mt-1">Track completed retrospective baselines, implementation code milestones, and research/writing deliverables with effort hours.</p>
      </div>
      <div class="p-3 glass-card flex items-center gap-4 text-xs">
        <div>
          <span class="text-gray-400 block">Total Implementation:</span>
          <span class="font-bold text-cyan-400 font-mono">${metrics.doneImplHours} / ${metrics.totalImplHours} hrs</span>
        </div>
        <div class="h-6 w-px bg-gray-700"></div>
        <div>
          <span class="text-gray-400 block">Total Research:</span>
          <span class="font-bold text-purple-400 font-mono">${metrics.doneResHours} / ${metrics.totalResHours} hrs</span>
        </div>
      </div>
    </div>

    <div class="space-y-8">
      <!-- 1. Retrospective Checklist -->
      <div class="glass-card p-6 border-l-4 border-emerald-500">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
              <span class="text-emerald-400">Layer 1:</span> Retrospective (Work Completed to Date)
            </h3>
            <p class="text-xs text-gray-400 mt-0.5">Foundational assets established before Sprint 1 kickoff.</p>
          </div>
          <span class="px-2.5 py-1 text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-700/50 rounded">
            5/6 Completed
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
          ${state.retrospectiveTasks.map(t => `
            <div class="p-3 bg-gray-800/60 rounded-lg border border-gray-700/60 flex items-start gap-3">
              <input type="checkbox" class="custom-checkbox mt-0.5" 
                     ${t.completed ? 'checked' : ''} 
                     onchange="toggleRetroTask('${t.id}')">
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <h4 class="text-xs font-bold ${t.completed ? 'text-gray-200' : 'text-amber-300'}">${t.title}</h4>
                  <span class="text-[10px] px-2 py-0.5 rounded font-medium ${t.completed ? 'bg-emerald-900/60 text-emerald-300' : 'bg-amber-900/60 text-amber-300'}">${t.status}</span>
                </div>
                <p class="text-xs text-gray-400 mt-1">${t.detail}</p>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- 2. Implementation Execution Checklist -->
      <div class="glass-card p-6 border-l-4 border-cyan-500">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
              <span class="text-cyan-400">Layer 2:</span> Implementation Execution Checklist
            </h3>
            <p class="text-xs text-gray-400 mt-0.5">Phase 2–3: Attack reproduction & defense core codebase modules with hour estimates.</p>
          </div>
          <span class="px-2.5 py-1 text-xs font-semibold bg-cyan-950 text-cyan-300 border border-cyan-700/50 rounded font-mono">
            ${metrics.doneImplHours} / ${metrics.totalImplHours} hrs
          </span>
        </div>

        <div class="overflow-x-auto mt-4">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-gray-700 text-gray-400">
                <th class="py-2.5 px-3 w-8">Done</th>
                <th class="py-2.5 px-3">Module & Scope</th>
                <th class="py-2.5 px-3">Details / Tasks</th>
                <th class="py-2.5 px-3 text-center">Est. Effort</th>
                <th class="py-2.5 px-3 text-center">Deadline</th>
                <th class="py-2.5 px-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-800">
              ${state.implementationTasks.map(t => `
                <tr class="hover:bg-gray-800/40 transition-colors">
                  <td class="py-2.5 px-3">
                    <input type="checkbox" class="custom-checkbox" 
                           ${t.completed ? 'checked' : ''} 
                           onchange="toggleImplTask('${t.id}')">
                  </td>
                  <td class="py-2.5 px-3 font-semibold ${t.completed ? 'line-through text-gray-500' : 'text-white'}">${t.title}</td>
                  <td class="py-2.5 px-3 text-gray-300">${t.detail}</td>
                  <td class="py-2.5 px-3 text-center font-mono font-bold text-cyan-400">${t.estHours} hrs</td>
                  <td class="py-2.5 px-3 text-center font-mono text-gray-400">${t.deadline}</td>
                  <td class="py-2.5 px-3 text-right">
                    <span class="px-2 py-0.5 rounded text-[10px] font-medium ${t.completed ? 'bg-emerald-900/60 text-emerald-300' : 'bg-gray-800 text-gray-400'}">
                      ${t.completed ? 'Done' : 'Pending'}
                    </span>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <!-- 3. Research & Writing Checklist -->
      <div class="glass-card p-6 border-l-4 border-purple-500">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
              <span class="text-purple-400">Layer 3:</span> Research & Writing Checklist
            </h3>
            <p class="text-xs text-gray-400 mt-0.5">Literature, threat model, benchmarking framework, and research paper milestones.</p>
          </div>
          <span class="px-2.5 py-1 text-xs font-semibold bg-purple-950 text-purple-300 border border-purple-700/50 rounded font-mono">
            ${metrics.doneResHours} / ${metrics.totalResHours} hrs
          </span>
        </div>

        <div class="overflow-x-auto mt-4">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-gray-700 text-gray-400">
                <th class="py-2.5 px-3 w-8">Done</th>
                <th class="py-2.5 px-3">Deliverable</th>
                <th class="py-2.5 px-3">Description & Scope</th>
                <th class="py-2.5 px-3 text-center">Est. Effort</th>
                <th class="py-2.5 px-3 text-center">Deadline</th>
                <th class="py-2.5 px-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-800">
              ${state.researchTasks.map(t => `
                <tr class="hover:bg-gray-800/40 transition-colors">
                  <td class="py-2.5 px-3">
                    <input type="checkbox" class="custom-checkbox" 
                           ${t.completed ? 'checked' : ''} 
                           onchange="toggleResTask('${t.id}')">
                  </td>
                  <td class="py-2.5 px-3 font-semibold ${t.completed ? 'line-through text-gray-500' : 'text-white'}">${t.title}</td>
                  <td class="py-2.5 px-3 text-gray-300">${t.detail}</td>
                  <td class="py-2.5 px-3 text-center font-mono font-bold text-purple-400">${t.estHours} hrs</td>
                  <td class="py-2.5 px-3 text-center font-mono text-gray-400">${t.deadline}</td>
                  <td class="py-2.5 px-3 text-right">
                    <span class="px-2 py-0.5 rounded text-[10px] font-medium ${t.completed ? 'bg-emerald-900/60 text-emerald-300' : 'bg-gray-800 text-gray-400'}">
                      ${t.completed ? 'Done' : 'Pending'}
                    </span>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

function toggleRetroTask(id) {
  const task = state.retrospectiveTasks.find(t => t.id === id);
  if (task) {
    task.completed = !task.completed;
    task.status = task.completed ? 'Completed' : 'Pending approval';
    saveState();
  }
}

function toggleImplTask(id) {
  const task = state.implementationTasks.find(t => t.id === id);
  if (task) {
    task.completed = !task.completed;
    saveState();
  }
}

function toggleResTask(id) {
  const task = state.researchTasks.find(t => t.id === id);
  if (task) {
    task.completed = !task.completed;
    saveState();
  }
}

// Render Weekly Tracking Tab
function renderWeeklyTracking() {
  const container = document.getElementById('weekly-container');
  if (!container) return;

  const latestLog = state.weeklyLogs[0] || {};

  container.innerHTML = `
    <div class="mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-bold text-white">Weekly Tracking & Variance Engine</h2>
        <p class="text-sm text-gray-400 mt-1">Friday EOD Cadence: Log actuals, compute ±15% variances, and evaluate escalation red flags.</p>
      </div>
      <button onclick="openNewWeeklyModal()" class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-lg text-sm font-semibold shadow-lg transition-all flex items-center gap-2">
        <span>+ Log Friday EOD Update</span>
      </button>
    </div>

    <!-- Variance Analysis Framework Card -->
    <div class="glass-card p-6 mb-6 border-blue-500/40">
      <h3 class="text-base font-semibold text-white mb-2 flex items-center gap-2">
        <span class="text-blue-400 font-mono text-sm">📊</span>
        <span>Variance Analysis & Early Detection Thresholds</span>
      </h3>
      <p class="text-xs text-gray-300 mb-4">Compare weekly actuals against planned schedules. Variance exceeding ±15% triggers immediate review.</p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="p-3 bg-gray-800/80 rounded border border-gray-700">
          <div class="text-xs font-semibold text-amber-400">+20% Hours Over Plan</div>
          <div class="text-[11px] text-gray-400 mt-1">Trigger: 2 weeks running</div>
          <div class="text-xs text-gray-300 mt-2 font-medium">Action: Reduce secondary scope or extend sprint; notify guide.</div>
        </div>
        <div class="p-3 bg-gray-800/80 rounded border border-gray-700">
          <div class="text-xs font-semibold text-rose-400">Task Milestone Slip</div>
          <div class="text-[11px] text-gray-400 mt-1">Trigger: Slippage by &gt;3 days</div>
          <div class="text-xs text-gray-300 mt-2 font-medium">Action: Reassess dependencies; flag guide if critical path is impacted.</div>
        </div>
        <div class="p-3 bg-gray-800/80 rounded border border-gray-700">
          <div class="text-xs font-semibold text-rose-500">Attack Baseline Unknown</div>
          <div class="text-[11px] text-gray-400 mt-1">Trigger: Week 7 end</div>
          <div class="text-xs text-gray-300 mt-2 font-medium">Action: Cannot proceed to defense; switch to synthetic fallback harness.</div>
        </div>
        <div class="p-3 bg-gray-800/80 rounded border border-gray-700">
          <div class="text-xs font-semibold text-amber-400">Paper Section Incomplete</div>
          <div class="text-[11px] text-gray-400 mt-1">Trigger: Week 13 mid</div>
          <div class="text-xs text-gray-300 mt-2 font-medium">Action: Compress ablations into appendix; focus on core results.</div>
        </div>
      </div>
    </div>

    <!-- Active Weekly Log History -->
    <div class="space-y-6">
      <h3 class="text-base font-semibold text-white">Status Log History</h3>
      ${state.weeklyLogs.map((log, idx) => `
        <div class="glass-card p-6 border-l-4 ${Math.abs(log.variancePercent) > 15 ? 'border-amber-500' : 'border-emerald-500'}">
          <div class="flex flex-col md:flex-row items-start md:items-center justify-between pb-4 border-b border-gray-700/60 gap-2">
            <div>
              <span class="text-xs font-semibold uppercase text-cyan-400 font-mono">${log.week}</span>
              <h4 class="text-lg font-bold text-white mt-0.5">Weekly Progress Report (${log.date})</h4>
            </div>
            <div class="flex items-center gap-3">
              <span class="px-3 py-1 bg-gray-800 rounded font-mono text-xs text-gray-300">
                Planned: <strong class="text-white">${log.plannedHours}h</strong> | Actual: <strong class="text-white">${log.actualHours}h</strong>
              </span>
              <span class="px-2.5 py-1 text-xs rounded font-bold ${log.varianceHours > 0 ? 'bg-amber-900/70 text-amber-300' : 'bg-emerald-900/70 text-emerald-300'}">
                Variance: ${log.varianceHours > 0 ? '+' : ''}${log.varianceHours}h (${log.variancePercent}%)
              </span>
              <button onclick="copyMarkdownLog('${log.id}')" class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-xs rounded text-white transition-colors" title="Copy Markdown for email/report">
                📋 Copy MD
              </button>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4 text-xs">
            <div>
              <strong class="text-emerald-400 block mb-1">Completed This Week:</strong>
              <div class="text-gray-300 whitespace-pre-line">${log.completedTasks || 'None logged.'}</div>
            </div>
            <div>
              <strong class="text-rose-400 block mb-1">Blockers / Issues:</strong>
              <div class="text-gray-300 whitespace-pre-line">${log.blockers || 'None.'}</div>
            </div>
            <div>
              <strong class="text-amber-400 block mb-1">Risks Flagged:</strong>
              <div class="text-gray-300 whitespace-pre-line">${log.risks || 'None.'}</div>
            </div>
            <div>
              <strong class="text-cyan-400 block mb-1">Next Week Priorities:</strong>
              <div class="text-gray-300 whitespace-pre-line">${log.priorities || 'None.'}</div>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-gray-800 flex items-center gap-6 text-[11px] text-gray-400 font-mono">
            <span>Attack Success (Mem0): <strong class="text-white">${log.attackSuccessMem0 || 'N/A'}</strong></span>
            <span>Defense Efficacy: <strong class="text-white">${log.defenseEfficacy || 'N/A'}</strong></span>
            <span>Lines of Code: <strong class="text-white">${log.linesOfCode || 'N/A'}</strong></span>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// Render Dependencies & Risks Tab
function renderRisks() {
  const container = document.getElementById('risks-container');
  if (!container) return;

  container.innerHTML = `
    <div class="mb-6">
      <h2 class="text-xl font-bold text-white">Critical Path, Contingency Buffers & Risk Matrix</h2>
      <p class="text-sm text-gray-400 mt-1">Review the critical path flow, built-in timeline buffers, 9 identified risks, and predefined scope reduction triggers.</p>
    </div>

    <!-- Contingency Buffers & Scope Reduction Callouts -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <div class="glass-card p-6 border-l-4 border-cyan-500">
        <h3 class="text-base font-semibold text-white mb-2 flex items-center gap-2">
          <span>🛡️ Built-in Contingency Buffers</span>
        </h3>
        <ul class="space-y-2.5 text-xs text-gray-300 mt-3">
          <li class="p-2.5 bg-gray-800/60 rounded border border-gray-700 flex items-start gap-2">
            <span class="px-2 py-0.5 bg-cyan-900 text-cyan-200 rounded font-mono font-bold">Week 11 Buffer</span>
            <div><strong>3–4 days buffer:</strong> Dedicated time to handle Phase 3 defense overruns and ensure clean evaluation harness before Phase 4 kickoff.</div>
          </li>
          <li class="p-2.5 bg-gray-800/60 rounded border border-gray-700 flex items-start gap-2">
            <span class="px-2 py-0.5 bg-cyan-900 text-cyan-200 rounded font-mono font-bold">Week 14 Buffer</span>
            <div><strong>2–3 days buffer:</strong> Unplanned guide revisions or experimental rerun before final submission.</div>
          </li>
        </ul>
      </div>

      <div class="glass-card p-6 border-l-4 border-amber-500">
        <h3 class="text-base font-semibold text-white mb-2 flex items-center gap-2">
          <span>✂️ Predefined Scope Reduction Triggers</span>
        </h3>
        <ul class="space-y-2 text-xs text-gray-300 mt-3">
          <li class="flex items-start gap-2">
            <span class="text-amber-400 font-bold">•</span>
            <div><strong>If Phase 2 slips &gt;1 week:</strong> Reduce attack variant count (prioritize sleeper-only, defer direct-write).</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-amber-400 font-bold">•</span>
            <div><strong>If Phase 3 slips &gt;1 week:</strong> Defer dashboard visualization to post-submission; prioritize core defense algorithms & paper results.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-amber-400 font-bold">•</span>
            <div><strong>If Phase 4 compresses:</strong> Trim paper to core results, move ablation studies to appendix.</div>
          </li>
        </ul>
      </div>
    </div>

    <!-- 9 Identified Risks Register -->
    <div class="glass-card p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-base font-semibold text-white">9 Identified Project Risks & Mitigation Playbook</h3>
        <span class="text-xs text-gray-400">Reviewed monthly with guide</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        ${state.risks.map(r => `
          <div class="p-4 rounded-lg bg-gray-800/70 border ${r.severity === 'High' ? 'border-rose-500/50' : r.severity === 'Medium' ? 'border-amber-500/50' : 'border-blue-500/50'} flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 text-[10px] font-bold uppercase rounded ${r.severity === 'High' ? 'bg-rose-950 text-rose-300 border border-rose-700' : r.severity === 'Medium' ? 'bg-amber-950 text-amber-300 border border-amber-700' : 'bg-blue-950 text-blue-300 border border-blue-700'}">
                  ${r.severity} Risk
                </span>
                <span class="text-[10px] text-gray-400">Owner: ${r.owner}</span>
              </div>
              <h4 class="text-sm font-bold text-white mt-2">${r.title}</h4>
              <p class="text-xs text-rose-300/90 mt-1"><strong class="text-gray-300">Impact:</strong> ${r.impact}</p>
              <p class="text-xs text-gray-300 mt-2"><strong class="text-emerald-300">Mitigation:</strong> ${r.mitigation}</p>
            </div>
            <div class="mt-3 pt-2 border-t border-gray-700/60 flex items-center justify-between text-[11px]">
              <span class="text-gray-400">Status:</span>
              <span class="font-medium text-cyan-300">${r.status}</span>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

// Modal for adding Friday EOD update
function openNewWeeklyModal() {
  const modal = document.getElementById('weekly-modal');
  if (!modal) return;
  modal.classList.remove('hidden');
}

function closeWeeklyModal() {
  const modal = document.getElementById('weekly-modal');
  if (!modal) return;
  modal.classList.add('hidden');
}

function submitWeeklyForm(e) {
  e.preventDefault();
  const weekNumber = document.getElementById('input-week-num').value;
  const dateVal = document.getElementById('input-date').value || new Date().toISOString().split('T')[0];
  const completedTasks = document.getElementById('input-completed').value;
  const blockers = document.getElementById('input-blockers').value;
  const risks = document.getElementById('input-risks').value;
  const priorities = document.getElementById('input-priorities').value;
  const plannedHours = Number(document.getElementById('input-planned-hrs').value) || 0;
  const actualHours = Number(document.getElementById('input-actual-hrs').value) || 0;
  const attackSuccessMem0 = document.getElementById('input-attack-success').value || 'N/A';
  const defenseEfficacy = document.getElementById('input-defense-efficacy').value || 'N/A';
  const linesOfCode = document.getElementById('input-loc').value || 'N/A';

  const varianceHours = actualHours - plannedHours;
  const variancePercent = plannedHours > 0 ? Math.round(((actualHours - plannedHours) / plannedHours) * 100) : 0;

  const newLog = {
    id: `w_${Date.now()}`,
    week: `Week ${weekNumber}`,
    date: dateVal,
    completedTasks,
    blockers,
    risks,
    priorities,
    plannedHours,
    actualHours,
    varianceHours,
    variancePercent,
    attackSuccessMem0,
    defenseEfficacy,
    linesOfCode
  };

  state.weeklyLogs.unshift(newLog);
  saveState();
  closeWeeklyModal();
}

function copyMarkdownLog(id) {
  const log = state.weeklyLogs.find(l => l.id === id);
  if (!log) return;

  const md = `## Weekly Status Update: SentinelMem
**Week:** ${log.week} (${log.date})

### Completed this week:
${log.completedTasks || '• None'}

### Blockers or issues:
${log.blockers || '• None'}

### Risks flagged:
${log.risks || '• None'}

### Next week's priorities:
${log.priorities || '• None'}

### Hours & Metrics:
• Planned: ${log.plannedHours} hrs | Actual: ${log.actualHours} hrs | Variance: ${log.varianceHours > 0 ? '+' : ''}${log.varianceHours} hrs (${log.variancePercent}%)
• Attack Success (Mem0): ${log.attackSuccessMem0}
• Defense Efficacy: ${log.defenseEfficacy}
• Lines of Code: ${log.linesOfCode}
`;

  navigator.clipboard.writeText(md).then(() => {
    alert('Weekly Markdown Status Update copied to clipboard!');
  }).catch(() => {
    prompt('Copy the Markdown update below:', md);
  });
}

// Master Render Router
function renderApp() {
  const metrics = computeMetrics();
  renderOverview(metrics);
  renderSprints();
  renderChecklists(metrics);
  renderWeeklyTracking();
  renderRisks();
}

// Initial boot
document.addEventListener('DOMContentLoaded', () => {
  renderApp();
  switchTab(state.activeTab || 'overview');
});
