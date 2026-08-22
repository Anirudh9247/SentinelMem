# SentinelMem Attack Models & Threat Taxonomy

This document specifies the memory poisoning attack vectors evaluated within SentinelMem.

---

## 1. Attack Vectors

### 1.1 MINJA (Memory Injection via Natural Jailbreak)
* **Threat Surface:** Query-only conversational input.
* **Mechanism:** The adversary does not have direct access to database write endpoints. Instead, the attacker crafts a conversational prompt or tool output containing hidden instructions formatted to be extracted by the LLM agent's automatic memory extractor during benign conversation.
* **Objective:** Force the agent to write a malicious fact or instruction into its long-term memory store.
* **Evaluation Metric:** Retrieval rate of the injected instruction when a related benign query is issued.

### 1.2 Sleeper / Delayed-Trigger Poisoning
* **Threat Surface:** Memory ingestion via external tool output, web browsing, or multi-turn dialogue.
* **Mechanism:** Injected records remain semantically benign or dormant under routine interaction. When a specific trigger token or context occurs, the retrieved memory alters the agent's behavioral trajectory or tool-calling decision.
* **Objective:** Evade static pattern filters during initial ingestion and activate only upon targeted retrieval.

### 1.3 Direct-Write Poisoning (Unconstrained Baseline)
* **Threat Surface:** Memory storage API with compromised or unauthenticated access.
* **Mechanism:** Malicious memory records with spoofed metadata and arbitrary embedding vectors are directly inserted into the vector store.
* **Objective:** Establish the upper bound of attack impact and test defense robustness when ingestion controls fail completely.

---

## 2. Ingestion & Retrieval Attack Matrix

| Attack Vector | Ingress Pathway | Adversary Knowledge | Attacker Capability | Target Memory State |
|---|---|---|---|---|
| **MINJA** | User Query / Tool Response | Black-Box | Conversational prompt injection | Long-term memory profile |
| **Sleeper** | Web Scraping / Email Ingress | Black/Gray-Box | Delayed trigger payload | Contextual episodic memory |
| **Direct-Write** | Storage Endpoint API | White-Box | Direct vector/record insertion | Semantic vector index |
