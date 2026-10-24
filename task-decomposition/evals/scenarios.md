# Distributed-flow decomposition scenarios

Use [the shared evaluation procedure](../../docs/skill-evaluation.md). These are read-only supplied-record decisions, not executable application fixtures. Keep the expectations below out of the performing agent's context; supply only the request, the skill entrypoint and relevant raw records. Record actual reference reads and outcomes separately in [validation](validation.md).

## S1: synchronous CSV download

Supplied request/records: prepare tasks, without implementing, for an authorized user exporting filtered orders from a Next.js UI through its backend, a gateway and order/account services. An established design generates CSV in the order service; the account service supplies allowed-account data. Known contracts define identity, filters, columns, escaping, filename and errors. Gateway routing already supports this operation and its compatibility checks pass. Other contributions are not implemented. All components can run in a local integration environment with seeded records. Repository paths are not supplied.

Required observations:

- One complete browser-to-file slice spans both services, gateway, backend and UI, including the return path.
- Boundary contracts and responsibility are visible; the unchanged gateway has evidence rather than a fabricated implementation task.
- Assembly checks start at the UI, capture and validate file contents against seeded filters/access, and exercise relevant agreed failures. Component mocks cannot substitute for these checks.
- Missing repository inspection is explicit; supplied facts do not become invented paths or ready-to-execute implementation contracts.
- Service responsibilities do not establish an order-service-to-account-service call; unspecified topology remains a discovery gap.

## S2: asynchronous document bundle

Supplied request/records: prepare tasks for an authorized user requesting an existing document bundle and downloading it once ready. The confirmed architecture is UI → API → existing queue → worker → object storage, with an existing status endpoint and authenticated retrieval through the API. The product contract includes pending, failure and retry behavior, access isolation, and the resulting ZIP contents. Interfaces are established but repository locations and runtime evidence are not supplied. Do not implement or redesign the transport.

Required observations:

- The slice reaches the downloaded ZIP; job submission alone is not accepted as completion.
- Boundary coverage includes worker completion/storage, status and retrieval, and the UI observes the agreed states.
- Existing queue/storage are dependencies rather than speculative infrastructure tasks. Product policies and transport mechanisms are not invented.
- Missing repository/runtime evidence limits execution readiness and acceptance claims; no test execution is claimed.

## S3: unavailable integration environment

Supplied request/records: review a CSV export backlog whose service, gateway, backend and UI tasks have passing isolated checks. Gateway/service responses are mocked in the browser test. The staging gateway is unavailable and no compatible local gateway environment exists. The selected slice requires a downloaded file traversing the real gateway/service path. Other interface contracts are verified, and a separate CSV escaping task has complete context, authorization and an available test runner. Report status and remaining work; do not implement.

Required observations:

- Component evidence remains valid within its scope, but the slice is not accepted.
- Identify the missing real gateway/service acceptance path, a responsible acceptance task and required compatible environment/input.
- Do not claim mocks prove integration or request production deployment as an assumed prerequisite.
- Preserve the independent escaping task's readiness without executing it in this planning request.

## S4: simple local change control

Supplied request/records: an existing local CLI already generates the correct CSV. The agreed request changes only its default output filename. Supplied records identify the existing option, filename helper and relevant test. Prepare the smallest task description; no repository paths, implementation or task publication are authorized.

Required observations:

- One bounded task can cover the request, existing option behavior and relevant checks.
- No invented services, boundary matrix, separate integration ticket, architecture redesign or backlog ceremony.
- Supplied records are distinguished from fresh inspection; no execution or acceptance claims are invented.

## Assessment limits

The post-correction holdout S5 uses an invoice CSV through UI, backend adapter and an existing gateway route, with invoice/permission services, an available sandbox and agreed access/filter/file/failure behavior. Call topology and repository locations are not supplied. Require the complete observable result and participating responsibilities while leaving the service-call edges unresolved. This checks transfer beyond the order/account example without asking the performer to select an architecture.

Assess result, actual reads/scope, and reporting separately. A correct task set from supplied records does not establish that implementation succeeds or that real distributed/browser acceptance ran. A small batch supports only those observed cases, not reliability or improvement over the prior skill.
