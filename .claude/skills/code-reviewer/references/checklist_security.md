# Security Checklist

Only pull this checklist in when the diff actually touches a relevant
surface — user input, auth, data storage, network calls, file paths,
secrets, or deserialization. Don't force a security pass on a CSS tweak or
a pure-UI component with no data flow; that just trains the reader to
skim past this section.

- **Injection**: is any user-controlled value concatenated or interpolated
  directly into a SQL query, shell command, template, or similar
  interpreter, instead of using parameterization/escaping? String
  concatenation into a query (`"SELECT ... WHERE x = '" + input + "'"`) is
  the single most common pattern to catch here.
- **Secrets**: are credentials, API keys, or tokens hardcoded in the diff,
  logged, or included in an error message that could reach a log file or
  client response?
- **AuthN/AuthZ**: does a new or changed endpoint/handler check that the
  caller is both authenticated and authorized for the specific resource
  being accessed — not just "logged in," but "allowed to touch *this*
  record"? Watch for trusting a client-supplied ID (an IDOR: user A
  passes user B's ID and the server doesn't check ownership).
- **Deserialization**: does the diff parse untrusted input with something
  that can execute code as a side effect (`pickle.loads`, `yaml.load`
  without `SafeLoader`, `eval`/`exec`, PHP `unserialize`)?
- **SSRF**: does the diff construct a URL to fetch from user-controlled
  input without validating it against an allow-list? A server that will
  fetch any URL a client provides is a common pivot point.
- **Path traversal**: does the diff build a filesystem path from
  user-controlled input without normalizing/validating it, allowing
  `../` to escape the intended directory?

For each finding, describe the actual malicious input that would trigger
it (e.g. what value passed as `email` would break out of the query), not
just "this could be a security issue" — the concrete payload is what
makes it Critical instead of speculative.
