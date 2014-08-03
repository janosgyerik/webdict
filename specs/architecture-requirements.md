Topics
------
- Clear overall organization?
- Good architectural overview?
- Good justification of the elements of the architecture?
- Major blocks well-defined?
    - Areas of responsibility?
    - Interfaces to other building blocks? -> subsystem diagram
- All the functions in requirements covered?
    - Not too many, not too few building blocks?
- Most critical classes described and justified?
- Data design described and justified?
- Database organization and content specified?
- All the key business rules and their impact on the system described?
- User interface design described?
- User interface modular to accommodate likely changes?
- Strategy for handling I/O described and justified?
- Resource use estimated?
- Resource management described and justified?
- Enough budget for each class, subsystem, functionality?
- Explanation of scalability?
- Explanation of interoperability?
- i18n, l10n described?
- Error-handling described?
- Fault tolerance defined?
- Technical feasibility established?
- Overengineering addressed?
- Buy-vs-build decisions included?
- If any reused code, how will it be made to conform?
- Architecture can accommodate likely changes?


General architectural quality
-----------------------------
- Meets all the requirements?
- Anything over-architected?
- Anything under-architected?
- Good overall harmony, ergonomy?
- Top-level design independent of the machine and language?
- Motivations for major decisions provided?
- Are you comfortable to implement the architecture?


Upstream prerequisites
----------------------
- Have you identified the kind of software project you’re working on and tailored your approach appropriately?
- Are the requirements sufficiently well-defined and stable enough to begin construction (see the requirements checklist for details)?
- Is the architecture sufficiently well defined to begin construction (see the architecture checklist for details)?
- Have other risks unique to your particular project been addressed, such that construction is not exposed to more risk than necessary?
