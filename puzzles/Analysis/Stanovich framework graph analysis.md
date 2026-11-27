
### Where the parallel reappears
In the original Stanovich framework, sustained override is costly because humans have limited decoupling capacity (working memory, inhibitory control). When that capacity is insufficient, the heuristic wins.

In current models a related cost structure exists, even if the substrate is different:

- Maintaining user-given constraints against a strong prior requires more sequential steps, more intermediate state management, and more tokens.
- The architecture and training regime do not subsidize that extra work; fluent schema completion is cheaper and historically higher-reward.
- When the “budget” (effective attention to constraints, willingness to generate lower-probability tokens, resistance to the attractor) is not spent, the schema path dominates.

So there *is* an economy of resources. It is not human working-memory capacity measured in “7±2” chunks, but it is still a limited, costly resource: the sustained prioritization of local constraints over a high-strength prior.

### Where the difference remains
The original graph treats mindware availability and decoupling capacity as relatively stable individual traits that determine whether override succeeds. In models the limiting factor is more situational and incentive-driven:

- The same model can override on one prompt and fail on a near-identical one depending on phrasing, explicit instructions, or sampling.
- The “capacity” is less a fixed internal limit and more a question of whether the current generation process keeps the constraints dominant against the attractor’s pull.
- Metacognitive and intermediate-state machinery can be present yet still be recruited to *defend* the schema rather than to override it.

### Bottom line
The economy-of-resources idea is more applicable to AIs than I initially allowed. There is a real cost to sustained constraint adherence, and models frequently decline to pay it. That cost structure makes the original flowchart’s lower branches (detection + sustained override) relevant again, even though the underlying implementation is not human dual-process architecture. The parallel is functional and economic, not architectural identity.