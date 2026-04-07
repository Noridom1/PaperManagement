# Graph Report - Test-time Scaling  (2026-04-07)

## Corpus Check
- Corpus is ~291 words - fits in a single context window. You may not need a graph.

## Summary
- 33 nodes · 41 edges · 6 communities detected
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Reward Model as External Verifier` - 5 edges
2. `TTGen: Incorporating Test-time Scaling to Diffusion Models` - 3 edges
3. `Test-Time Scaling of Diffusion Models via Noise Trajectory Search` - 3 edges
4. `VReST: Enhancing Reasoning in Vision-Language Models` - 2 edges
5. `Scaling Inference Time Compute for Diffusion Models` - 2 edges
6. `R1-One Vision: Advancing Generalized Multimodal Reasoning` - 2 edges
7. `Scaling LLM Test Time Compute` - 2 edges
8. `Efficient Test-time Scaling for Small Vision-Language Models` - 2 edges
9. `Inference-Time Scaling for Diffusion Models Beyond Scaling Denoising Steps` - 2 edges
10. `Let's Verify Step by Step: Verification Methods` - 2 edges

## Surprising Connections (you probably didn't know these)
- `ImageReward: Learning Human Preferences` --implements--> `Reward Model as External Verifier`  [EXTRACTED]
  Test-time Scaling/NeurIPS 2023 Poster - ImageReward.pdf → Test-time Scaling/Test-time Scaling ideas.txt
- `Best-of-Step Verification: Multiple Noise Paths` --conceptually_related_to--> `Test-Time Scaling of Diffusion Models via Noise Trajectory Search`  [INFERRED]
  Test-time Scaling/Test-time Scaling ideas.txt → Test-time Scaling/NeurIPS 2025 Poster - Test-Time Scaling of Diffusion Models via Noise Trajectory Search.pdf
- `ImageReward: Learning and Evaluating Human Preferences for Text-to-Image` --implements--> `Reward Model as External Verifier`  [EXTRACTED]
  Test-time Scaling/NeurIPS-2023-imagereward-learning-and-evaluating-human-preferences-for-text-to-image-generation-Paper-Conference.pdf → Test-time Scaling/Test-time Scaling ideas.txt
- `Reward Models: Survey and Taxonomy` --conceptually_related_to--> `Reward Model as External Verifier`  [EXTRACTED]
  Test-time Scaling/RewardModels-Survey.pdf → Test-time Scaling/Test-time Scaling ideas.txt
- `Finetune/Distill/Adapt for Intermediate Denoising Steps` --rationale_for--> `TTGen: Incorporating Test-time Scaling to Diffusion Models`  [EXTRACTED]
  Test-time Scaling/Test-time Scaling ideas.txt → Test-time Scaling/CVPR 2025 Workshop - TTGen Incorporating Test-time Scaling to Diffusion Models.pdf

## Hyperedges (group relationships)
- **Diffusion Model Test-Time Scaling Methods** — cvpr2025_diffusion_paper, ttgen_paper, diffusion_beyond_paper, noise_trajectory_paper, tts_var_paper [EXTRACTED 0.90]
- **Vision-Language Model Test-Time Scaling** — vrest_paper, efficient_tts_vlm_paper, visual_planning_paper, r1_onevision_paper [EXTRACTED 0.85]
- **Verification and Reward Models** — visionreward_paper, imagereward_neurips2023, imagereward_conf, verify_step_by_step_paper, reward_models_survey [EXTRACTED 0.90]
- **Reasoning and Recurrent Approaches** — recurrent_depth_paper, r1_onevision_paper, visual_planning_paper [INFERRED 0.80]
- **Survey and Overview Papers** — tts_llm_survey, reward_models_survey [EXTRACTED 0.95]

## Communities

### Community 0 - "Multimodal Reasoning"
Cohesion: 0.22
Nodes (10): R1-One Vision: Advancing Generalized Multimodal Reasoning, Reasoning and Recurrent Depth, Scaling up Test-Time Compute with Latent Reasoning: Recurrent Depth, S1: Simple Test-time Scaling, Test-Time Scaling, Test-time Scaling Research Ideas, TTSnap: Snapshot Test-Time Approach, VisionReward: Image Reward Model (+2 more)

### Community 1 - "Reward Verification Loop"
Cohesion: 0.25
Nodes (8): Image Generation / Text-to-Image, ImageReward: Learning and Evaluating Human Preferences for Text-to-Image, ImageReward: Learning Human Preferences, External Verifier Requires Additional Compute, Reward Model as External Verifier, Reward Models: Survey and Taxonomy, Verification enables evaluation at inference time, Let's Verify Step by Step: Verification Methods

### Community 2 - "Diffusion Test-Time Scaling"
Cohesion: 0.29
Nodes (7): Best-of-Step Verification: Multiple Noise Paths, Scaling Inference Time Compute for Diffusion Models, Inference-Time Scaling for Diffusion Models Beyond Scaling Denoising Steps, Diffusion Models, Finetune/Distill/Adapt for Intermediate Denoising Steps, Test-Time Scaling of Diffusion Models via Noise Trajectory Search, TTGen: Incorporating Test-time Scaling to Diffusion Models

### Community 3 - "VLM Test-Time Scaling"
Cohesion: 0.67
Nodes (3): Efficient Test-time Scaling for Small Vision-Language Models, Vision-Language Models, VReST: Enhancing Reasoning in Vision-Language Models

### Community 4 - "LLM Test-Time Scaling"
Cohesion: 0.67
Nodes (3): Scaling LLM Test Time Compute, Large Language Models, Test-Time Scaling on LLMs: Survey

### Community 5 - "VAR Adaptation Scaling"
Cohesion: 1.0
Nodes (2): TTS-VAR: Test-Time Scaling with VAR Models, VAR-based Generative Model Adaptation

## Knowledge Gaps
- **10 isolated node(s):** `VisionReward: Image Reward Model`, `VisRef: Visual Refocusing`, `S1: Simple Test-time Scaling`, `Visual Planning: Let's Think Only with Images`, `TTSnap: Snapshot Test-Time Approach` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `VAR Adaptation Scaling`** (2 nodes): `TTS-VAR: Test-Time Scaling with VAR Models`, `VAR-based Generative Model Adaptation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TTGen: Incorporating Test-time Scaling to Diffusion Models` connect `Diffusion Test-Time Scaling` to `Multimodal Reasoning`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `Test-Time Scaling of Diffusion Models via Noise Trajectory Search` connect `Diffusion Test-Time Scaling` to `Multimodal Reasoning`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Test-Time Scaling` (e.g. with `R1-One Vision: Advancing Generalized Multimodal Reasoning` and `Visual Planning: Let's Think Only with Images`) actually correct?**
  _`Test-Time Scaling` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `VisionReward: Image Reward Model`, `VisRef: Visual Refocusing`, `S1: Simple Test-time Scaling` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._