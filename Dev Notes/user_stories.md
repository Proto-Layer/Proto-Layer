## Client → Validator Workflow

This scenario describes how a client interacts with validators when making a utility request. The process should be the same regardless of the specific utility being requested.

Sending the Request
The client sends a utility request to the validator network.

How does the client know where to send it?

A preloaded list of known validators comes with the codebase. Each entry includes the necessary communication details, allowing the client to initiate contact. In this example, we focus on IP connections, but any low-latency channel could work.

This file might include: alias/ID, communication type, routing details, latency, and reliability.

For efficiency, we might store currently active validators in memory (e.g., a dictionary) instead of repeatedly reading the TOML file from disk.

Validator Acknowledgment
The validator responds, confirming receipt of the request and adding it to the job file for a specific block. They also return a list of validators participating in the payout cycle.

Possible issues:

Connection failure with some or all targeted validators.

Retry up to four times.

As a fallback, attempt connection over every available channel or address (“scream cast”), sending a plaintext message if the recipient is unknown (high-risk).

Consider a six-second timeout; if the job file for the current block is not filled within that time, move the request to the next block’s job file.

Block alignment: All validators must agree on which block will include the job before the request is sent. Maintaining two job files—one for the current block, one for the next—ensures late requests automatically roll forward.

Propagation
The client may send the request to additional validators if they haven’t received it yet.

This may be unnecessary if propagation is handled automatically. Three validator confirmations might be sufficient.

Finding Partners
Validators compile a list of partners able to provide the requested utility.

Include perception scores so the client can decide based on risk tolerance.

For centralized partners, include their preferred connection method to reduce wait time.

Clients should not store this partner info permanently, since partners might change IPs or use load balancing.

Sending Partner List
Validators return the list of willing partners to the client.

Prefer incremental delivery to start utility sooner.

Limit the number of listed partners to a reasonable threshold (set by the client).

Closing Communication
Normally, validator–client communication ends here, resuming only after the utility is complete. For this example, the flow continues.

Completion Reporting
The client sends validators a signed receipt from both client and partner for each completed transaction. Validators confirm completion and report the block number.

Potential problems:

The client might fail to send the receipt; if the partner submits it, the job completes. If neither does, it’s canceled at the next payout cycle (four hours), and only the transaction fee is paid.

A validator could ignore the completion message, but with a pool, more than two-thirds would need to collude for this to persist.

Partner → Validator Workflow

This scenario focuses on how partners interact with validators when offering to fulfill utility requests, excluding centralized partners for simplicity.

Announcing Availability
The partner sends a “ready to provide utility” message to the validator pool (e.g., for storage, computation, or access), using the same validator list as clients.

Risks:

Validator fails to respond.

Partner falsely claims they can provide a service—validators could issue challenges, possibly handled by passive validators to avoid overloading active ones.

Decide whether validators should proactively notify partners of matching jobs, or whether partners should search job files themselves. The proactive approach reduces partner polling load.

Partners may send periodic “still active” pings if waiting too long; we’ll need to define an interval.

Job Notifications
Validators notify partners when relevant jobs appear.

Risks:

Censorship by validators, possibly for reasons unrelated to perception score. Mitigation options:

Partner resends request or queries the job file.

If jobs exist and partner meets requirements, reduce offending validators’ perception scores.

Switching public keys circumvents bans, since validators cannot block all accounts.

Optionally escalate to the chain owner or make the issue public.

Partner fails a resource check—validators notify them.

Low perception score disqualifies participation—validators inform the partner.

Responding to Jobs
Partners respond to jobs of interest.

Risks:

Validators ignore responses due to delays, distance, or censorship. Long response times reduce likelihood of allocation.

Connection Details
Validators send partners the client’s contact details so they can initiate communication (or vice versa for centralized partners).

Incorrect information could come from either side, making diagnosis difficult and creating an attack vector.

Payout Pool Registration
Once connected, the partner informs validators the utility has started so it can be added to the payout pool. Validators confirm registration.

Capacity Management
Partners can send an “at capacity” message to indicate they cannot take on more work.

This provides real-time network load data and can guide creation of new domains.

A cooldown prevents excessive notifications.

Shutdown Notification
Partners send a “sign-off” message before going offline (e.g., power loss). This won’t prevent perception score drops but avoids receiving new requests.

Utility Completion
Upon completion, the partner sends validators a signed receipt from both sides, who return the completion block number.

Risks:

Client refuses to sign—partners can enter arbitration mode by sending the last signed message from the client to claim partial payout.

Validators fail to register the end of the job—could be malicious or due to overload; retries may be needed.

Validator ↔ Validator Workflow

This section outlines validator-to-validator communication, consensus methods, and role distinctions.

Active Validators – Directly handle all user requests, manage job and payout files, and maintain the blockchain. Limited to the number set by the chain owner (recommendation: ≤10 per domain).
Passive Validators – Standby nodes that can take over if an active validator fails or handle offloaded tasks. No limit; a way to rebuild perception scores.
Known Validators – Appointed by chain owners, possibly owned by them. No more than 44% of the active pool.
Unknown Validators – Randomly selected participants rotated every payout period (four hours), making up the remaining 56% of the active pool.

Network Discovery – New validators contact known validators to join the pool. Known validators wait for unknowns to connect.

Risk: insufficient unknown validators early on—may temporarily reclassify some known validators as unknown.

If no response, use scream cast to locate nodes.

Time Consensus – All validators agree on “block time” instead of block count.

During startup, measure latency between validators, discard outliers, and average times.

Time sync can be triggered if all agree, but cannot shift beyond a payout period.

Capacity Testing – Measure how many simultaneous connections a validator can handle, possibly using passive validators to simulate job traffic.

Job Files – Maintain two job files (current and next block). Update incrementally with partner data and hash checks. Resolve mismatches via binary search on file segments or full file transfers, depending on efficiency.

Payout Files – Similar to job files but include completion data. Could replace separate job files entirely to save space.

Convergence – When the network is overloaded or during a hash algorithm change, merge the chain into a new genesis block while keeping transactions going (or suspending them, if needed).

Network Status – Validators share status updates to detect overloads, possibly alongside job/payout file syncing.

Chain Link – At block end, send hashes to connected chains (max two). If a co-chain misses a hash, resume linking on the next block.

Domain Link – Connects domains (e.g., Earth and Mars instances) to reduce latency and allow token transfers between them.

Network Link – Connects independent but cooperative UndChain-like networks.

Risk: incompatible governance could cause splits, reducing interoperability.
