# Presenter Scrip: Disaster Context Graph RAG

**Audience**: Research Group / Professor
**Speaker**: User (Team Lead)
**Time**: ~5-7 Minutes

---

### Slide 1: Project Status Overview
"Hi everyone. As you know, we're building the **Disaster Context Graph RAG** system.
I'm happy to report that we are **On Track**.

Over the last week, we've completed the initial setup phase.
- **First**, we've finalized the architecture—specifically the two-layer graph design we discussed.
- **Second**, we've audited the data. We have confirmed access to over 35 datasets at the Hex-resolution level, so we aren't blocked on data availability.
- **And finally**, the infrastructure is ready. We have a dedicated repository and environment set up, so the team can start coding immediately."

*(Transition: "Let me remind you briefly of the core problem we’re solving...")*

---

### Slide 2: The Architecture (The "Why")
*(Point to the Diagram)*

"The core problem we face is that Standard RAG fails on Ambiguity and Math.
If a user asks for 'High Flood Risk', a standard vector search might return a random document about floods, but it won't know to look specifically for the `inundation_depth` column or how to aggregate it.

Our solution is this **Context Graph**—think of it as the 'Brain' that sits before the 'Muscle'.
1.  **Map**: First, the graph translates the vague concept 'High Flood Risk' into the precise feature `flood_inundation_depth`.
2.  **Constrain**: It then enforces the correct math—telling us this feature `REQUIRES` an 'Area-Weighted Average', not just a simple count.
3.  **Execute**: It hands this precise specification to the SQL Agent.

This ensures we don't just get an answer, we get a *statistically correct* answer."

---

### Slide 3: Team Roles & Responsibilities
"We have a strong team of four, splitting duties between Research and Engineering.

- **I (User)** will act as the Lead, handling the overall System Architecture and the relationships between components.
- **Ankit**, as our Research Scientist, is tackling the hardest ML problem: the **Feature Resolver**. He's building the logic that lets the AI 'learn' those connections between vague text and database columns.
- **Sahil** is owning the **Schema Graph**. He's building the 'Dictionary'—defining the nodes for features and concepts in Neo4j.
- **Christian** is focused on the **Evidence Graph**. He has the heavy lifting of ingesting those 35 million rows of Parquet data so the system can actually query it."

---

### Slide 4: MVP Plan (Next 2 Weeks)
"Our goal for the next two weeks is simple: **One Query, End-to-End.**

We are purposely restricting scope to ensure we get a working skeleton quickly.
- We aren't trying to load all 35 datasets yet. We are focusing strictly on **Hospitals (CritLife)** and **Shelters (HIFLD)**.
- We aren't building the complex AI resolver yet. We'll use simple keyword matching.

**Success** looks like this: We type 'Where are the shelters?', and the system successfully navigates the graph to find the `hifld_shelter` column and returns the data. Once we prove that, we scale."

---

### Slide 5: Discussion & Technical Decisions
"Finally, a few technical decisions we've made that I want to flag for discussion:

1.  **Neo4j**: We've decided to move to Neo4j for the graph database. It gives us better persistence and visualization than a simple Python network. We'll need to make sure we can run this on the lab servers via Docker.
2.  **Resolution**: The datasets are all indexed by H3 Hexagons. For the MVP, we are sticking strictly to Hex-level analysis. We can discuss later if we need to support County-level aggregation for the final paper.

**Questions?**"
