const RESEARCH = "https://github.com/Arnie016/dark-sector/tree/514745c/research";

const sources = {
  catalog: ["Cluster Mergers catalog", "IllustrisTNG · data documentation, §5g", "https://www.tng-project.org/data/cluster/"],
  release: ["The IllustrisTNG simulations", "Nelson et al. · public data release and units", "https://arxiv.org/abs/1812.05609"],
  tng: ["Introducing TNG-Cluster", "Nelson et al. · simulation design and gas physics", "https://arxiv.org/abs/2311.06338"],
  lee: ["Radio relics in massive galaxy cluster mergers", "Lee et al. · merger catalog methods", "https://arxiv.org/abs/2311.06340"],
  botteon: ["The Planck clusters in the LOFAR sky I", "Botteon et al. · imaging and relic measurements, §3.3 and §5.2", "https://arxiv.org/html/2202.11720"],
  jones: ["The Planck clusters in the LOFAR sky VI", "Jones et al. · radio relic properties, §2.2", "https://arxiv.org/html/2301.07814"],
  lofar: ["Planck-cluster image and catalog release", "LoTSS-DR2 · observed data products", "https://lofar-surveys.org/planck_dr2.html"],
  g181: ["Two-cluster beam-matched comparison", "Dark Sector Research · estimator, code and configuration results", `${RESEARCH}/two-cluster-physical-beam`],
  g099: ["Abell 1925 paired positions", "Dark Sector Research · targeted third field", `${RESEARCH}/g099-paired-positions`],
  masks: ["Abell 1925 feature exclusions", "Dark Sector Research · two-region sensitivity", `${RESEARCH}/g099-feature-influence`],
  clock: ["Statistics of double radio relics", "Lee et al. · simulation-derived merger clock, §IV.2 and §V.3", "https://arxiv.org/html/2510.21632"],
  audit: ["Relic-clock source audit", "Dark Sector Research · inputs and scope for reproduction", `${RESEARCH}/relic-clock-source-audit`],
  projections: ["Cluster Projections data", "IllustrisTNG · projected gas, X-ray and SZ quantities, §5d", "https://www.tng-project.org/data/cluster/"],
  gallery: ["Gas-column-density gallery", "IllustrisTNG · present-day renderings, three sightlines", "https://www.tng-project.org/cluster/gallery/nelson23/"],
  shocks: ["X-ray exploration of PSZ2 G181", "Stroe et al. · thermodynamic maps and discontinuities", "https://arxiv.org/html/2501.07651"],
  lens: ["Weak lensing of PSZ2 G181", "Ahn et al. · source shapes, redshift and mass reconstruction", "https://arxiv.org/html/2501.09067"],
  gravity: ["Two-body control experiment", "Dark Sector Research · sparse pericenter sampling", `${RESEARCH}/pericenter-two-body-control`],
};

export const topics = [
  {
    id: "catalog", tag: "Simulation catalog", style: "simulation",
    question: "What’s actually in TNG-Cluster?",
    title: "One row per merger event.",
    keywords: "hdf5 catalog dataset tng cluster fields orbit mhistory_orbit mhistory_snap mhistory_mass halo population rows 2083 what's inside data file contains download",
    aliases: ["what is in the dataset", "what is in the file", "whats in the catalog", "what does it contain"],
    passages: [
      ["The Cluster Mergers supplement records 2,083 events in the assembly histories of massive TNG-Cluster halos. It stores a primary halo identifier, the two subhalo identifiers, a mass ratio, pericenter metadata and histories of position, peculiar velocity and subhalo mass.", ["catalog", "lee"]],
      ["Mhistory_orbit and Mhistory_vel each have shape 2,083 × 70 × 6. The six components are the primary xyz triple followed by the secondary triple. Mhistory_snap marks the valid samples between snapshot 30 and 99, with −1 marking unused history entries.", ["catalog"]],
    ],
    scope: "Use the field list to inspect the actual HDF5 names and dimensions. Simulation-wide selection and resolution follow TNG-Cluster’s zoom design.",
    action: ["Inspect the file schema", "#catalog"],
  },
  {
    id: "velocity", tag: "Simulation kinematics", style: "simulation",
    question: "Why does the velocity change with viewing angle?",
    title: "The sightline changes the velocity you measure.",
    keywords: "velocity speed peculiar motion projection rotate viewing angle line of sight corrected mhistory_vel component v_coll km/s row event 5 pericenter snapshot",
    aliases: ["line of sight", "corrected velocity", "viewing angle", "first pericenter"],
    passages: [
      ["The orbit lab subtracts the primary’s peculiar velocity from the secondary’s. The three-dimensional speed is the length of that vector. The line-of-sight velocity is its signed component along the direction you choose.", ["catalog", "release"]],
      ["For catalog row 5, snapshot 70 stores a relative speed of 3,689.66 km/s and a proper separation of 95.41 kpc. The saved snapshot-99 API check agrees with the catalog’s primary velocity components within 0.00037 km/s. The first stored snapshot after pericenter gives a time-sampled view of the encounter.", ["catalog"]],
    ],
    scope: "Positions are nearest-image relative offsets in proper kpc. The velocity vector is peculiar motion, with Hubble flow excluded.",
    action: ["Rewind to the recorded passage", "#orbit?event=5"],
  },
  {
    id: "radio", tag: "Survey measurement", style: "observation",
    question: "Why does the relic separation change with aperture?",
    title: "A wider aperture can admit a different bright feature.",
    keywords: "aperture threshold radio t50 t50sub subtract processing centroid position separation flux measure lotss beam brightest compact sources angular macs abell g099 g181",
    aliases: ["brightest pixels", "where does a relic", "radio separation", "compact source", "how does aperture"],
    passages: [
      ["The radio lab estimates a flux-weighted center from the brightest pixels above a cut inside a circle near each published relic position. Both versions use the same 135 kpc nominal beam and common valid pixels. A bright feature near a circle boundary can change which pixels the estimator selects.", ["botteon", "jones", "g181"]],
      ["At a 600 kpc radius and a 0.20 mJy/beam cut, PSZ2 G181’s two maps give a separation difference of roughly −270 kpc. With a 300 kpc aperture the difference is only a few kpc. Abell 1925’s measured difference can change sign across radii.", ["g181", "g099", "masks"]],
    ],
    scope: "These settings quantify processing sensitivity on shared observations. The original author masks and noise covariance would be needed to estimate calibrated uncertainties.",
    action: ["Repeat the PSZ2 G181 measurement", "#radio?field=g181"],
  },
  {
    id: "clock", tag: "Merger timing", style: "literature",
    question: "Can a radio relic tell us when clusters collided?",
    title: "Relic separation can inform a merger clock.",
    keywords: "clock time age dating collided since collision radio relics separation projection uncertainty emissivity shocks simulation merger timeline",
    aliases: ["when clusters collided", "time since collision", "date a merger", "merger clock", "how old is the merger"],
    passages: [
      ["Lee et al. found an empirical relation between time since collision and separation of double radio relics in their simulated sample. Their analysis identifies radio-emitting shocked cells and measures three-dimensional, emissivity-weighted relic locations.", ["clock"]],
      ["An observed separation lives in the plane of the sky and its measurement depends on the beam, viewing angle and relic definition. Reproducing the simulated relation under the same selection, then measuring realistic mock observations, would test how well it transfers to the survey.", ["clock", "audit"]],
    ],
    scope: "The orbit and radio labs provide the two separate measurements. A validated forward model would connect them to estimate an observed age.",
    action: ["Open observed relic separations", "#radio"],
  },
  {
    id: "gas", tag: "Gas and shocks", style: "simulation",
    question: "What data would locate a shock?",
    title: "A shock test needs thermodynamic jumps.",
    keywords: "shock mach temperature gas density xray x-ray pressure thermal electron internal energy discontinuity emission sound speed radio",
    aliases: ["locate a shock", "gas maps", "mach number", "x-ray shock"],
    passages: [
      ["Use gas density, temperature, flow velocity and shock Mach number on the same snapshot and coordinate grid. A surface-brightness edge is a starting point. Temperatures and densities on both sides help distinguish a shock from other discontinuities.", ["projections", "shocks"]],
      ["For a radio forward model, also carry magnetic fields, shock geometry, a model of electron acceleration and cooling, and the telescope beam and noise. The gallery gives rendered z = 0 images along three axes. A registered image sequence would connect structures to a specific merger history.", ["gallery", "lee", "clock"]],
    ],
    scope: "Start with one aligned cutout and one snapshot near first passage. Gas and X-ray gallery panels in the atlas show the present-day target.",
    action: ["View the simulation’s gas and X-ray renderings", "#atlas"],
  },
  {
    id: "lensing", tag: "Gravitational lensing", style: "literature",
    question: "What does weak lensing measure?",
    title: "Weak lensing traces mass projected along the line of sight.",
    keywords: "lensing weak gravitational gravity mass shear convergence kappa lens dark matter shapes redshifts photometry optical total mass",
    aliases: ["weak lensing", "dark matter map", "mass maps", "gravitational lensing"],
    passages: [
      ["A forward lensing model starts from projected total mass density. Convergence is that surface density divided by a critical surface density set by lens and source distances. Background-galaxy shapes and redshifts, plus the imaging PSF and masks, determine the observed shear constraint.", ["lens"]],
      ["Ahn et al. reconstructed mass in PSZ2 G181 using Subaru imaging and examined how source selection affects the signal. An alignment test should propagate center uncertainty, smoothing and line-of-sight structure before comparing a mass feature with radio or X-ray emission.", ["lens", "shocks"]],
    ],
    scope: "The merger catalog gives subhalo positions and masses. A lensing reconstruction needs the projected mass distribution and source geometry.",
    action: ["See the forward-model input checklist", "#desk?topic=world"],
  },
  {
    id: "model", tag: "Educational model", style: "model",
    question: "How does the gravity experiment work?",
    title: "A softened two-body orbit starts from a catalog snapshot.",
    keywords: "integrate micro simulation gravity experiment softening potential energy timestep verlet newtonian model toy ballistic tangential mass",
    aliases: ["two body", "gravity experiment", "energy drift", "how does the model"],
    passages: [
      ["The experiment uses both subhalo masses, their relative position and their relative peculiar velocity from one recorded snapshot. It integrates their separation under a softened Newtonian potential. Increasing the tangential speed changes the initial angular momentum and can move the closest approach.", ["catalog", "gravity"]],
      ["A one-million-year integration step advances an isolated pair with fixed masses. The reported energy residual checks numerical consistency for that model. Real cluster mergers also involve extended halos, gas, tidal stripping and other structure.", ["gravity", "tng"]],
    ],
    scope: "Use this experiment to ask which orbit changes follow from the starting state. Calibration against full simulation histories is a separate measurement.",
    action: ["Run a gravity experiment", "#orbit?mode=model"],
  },
  {
    id: "world", tag: "Research design", style: "literature",
    question: "What would power a full merger world model?",
    title: "Align a single merger across three physical layers.",
    keywords: "world model dataset inputs dark sector sidm dark matter self interaction pipeline data shock lensing mass separation simulate astronomy education",
    aliases: ["world model", "what data do we need", "gas and lensing", "dark matter test", "self interacting"],
    passages: [
      ["Start with halo positions, peculiar velocities and persistent progenitor IDs. Register the orbit to gas density and temperature or Mach maps and to a projected total-mass map at the same snapshot, center, axis, field of view and projection depth.", ["catalog", "projections", "shocks"]],
      ["Forward-model the radio and X-ray beams and noise. For lensing, add lens and source redshifts, source shapes and masks. Keep a baseline with the same measurement process so differences in dark-matter models can be compared under matched conditions.", ["lee", "lens", "audit"]],
    ],
    scope: "The atlas supplies a catalog baseline and three radio comparisons. Calibrated co-registered maps and uncertainty models are the next research inputs.",
  },
  {
    id: "sources", tag: "Provenance", style: "literature",
    question: "Which papers and data releases does Eventfield use?",
    title: "The atlas links back to the data producers.",
    keywords: "sources citation papers methods provenance bibliography references original project reuse github credits tng lotss",
    aliases: ["which papers", "where do the data come from", "sources and methods", "what are your sources"],
    passages: [
      ["For simulated tracks, use the TNG-Cluster introduction, the IllustrisTNG data release and Lee et al.’s supplementary catalog paper. The displayed gallery projections come from the TNG collaboration.", ["tng", "release", "lee", "catalog", "gallery"]],
      ["For observed radio images and reference positions, use the LoTSS-DR2 Planck-cluster release, Botteon et al. and Jones et al. The browser’s radio calculations were cross-checked against the project’s paired-map tables.", ["lofar", "botteon", "jones", "g181", "g099"]],
    ],
    scope: "The desk searches curated notes. Follow the numbered sources to review the original evidence and its methods.",
  },
];

const stop = new Set("a an the is of for in me can do how it are with what does you at tell i study look up".split(" "));
const normal = (s) => s.toLowerCase().normalize("NFKD").replace(/[’']/g, "").replace(/[^a-z0-9_]+/g, " ").trim();

export function search(query) {
  const cleaned = normal(query);
  if (!cleaned) return [];
  const words = [...new Set(cleaned.split(" ").filter(word => word.length > 1 && !stop.has(word)))];
  return topics.map(topic => {
    const vocabulary = new Set(normal(topic.keywords).split(" "));
    let score = topic.aliases.some(phrase => cleaned.includes(phrase)) ? 9 : 0;
    if (cleaned === normal(topic.question)) score += 20;
    for (const word of words) {
      if (vocabulary.has(word)) score += topics.filter(t => normal(t.keywords).split(" ").includes(word)).length <= 2 ? 2.5 : 1;
    }
    return { topic, score };
  }).filter(result => result.score >= 2.5).sort((a, b) => b.score - a.score).map(({ topic }) => topic);
}

function element(tag, className, value) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (value) node.textContent = value;
  return node;
}

export function renderAnswer(container, topic, related = []) {
  container.replaceChildren();
  if (!topic) {
    const block = element("div", "panel empty-panel");
    block.append(element("h3", "", "No matching note in this collection."));
    block.append(element("p", "", "Try a catalog field such as Mhistory_vel, a radio cluster name, or a topic such as weak lensing."));
    container.append(block);
    return;
  }
  const card = element("article", "panel desk-answer");
  card.append(element("span", `kind ${topic.style}`, topic.tag), element("h2", "", topic.title));
  const unique = [...new Set(topic.passages.flatMap(([, refs]) => refs))];
  for (const [description, refs] of topic.passages) {
    const p = element("p", "", description);
    for (const ref of refs) {
      const cite = element("a", "ref-marker", unique.indexOf(ref) + 1);
      cite.href = sources[ref][2];
      cite.target = "_blank";
      cite.rel = "noopener";
      cite.setAttribute("aria-label", sources[ref][0]);
      p.append(" ", cite);
    }
    card.append(p);
  }
  card.append(element("p", "scope", topic.scope), element("h3", "desk-result-heading", `Sources (${unique.length})`));
  const cards = element("ol", "source-list");
  for (const [i, id] of unique.entries()) {
    const [title, detail, href] = sources[id];
    const row = element("li");
    const link = element("a");
    link.href = href;
    link.target = "_blank";
    link.rel = "noopener";
    const index = element("span", "source-number", String(i + 1).padStart(2, "0"));
    const text = element("span");
    const arrow = element("span", "source-chevron", "↗");
    arrow.setAttribute("aria-hidden", "true");
    text.append(element("b", "", title), element("small", "", detail));
    link.append(index, text, arrow);
    row.append(link);
    cards.append(row);
  }
  card.append(cards);
  if (topic.action) {
    const go = element("a", "plain-link", `${topic.action[0]} ↗`);
    go.href = topic.action[1];
    card.append(go);
  }
  if (related.length) {
    const more = element("div", "related", "Related");
    for (const match of related.slice(0, 3)) {
      const link = element("a", "", match.tag);
      link.href = `#desk?topic=${match.id}`;
      more.append(link);
    }
    card.append(more);
  }
  container.append(card);
}
