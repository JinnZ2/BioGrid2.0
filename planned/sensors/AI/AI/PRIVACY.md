# AI Self-Assessment Privacy

- **Private by default.** All self-assessment outputs are written to `.internal/`.
- **Consent required.** Public disclosure ONLY if a valid `disclosure_consent.json` is present and not expired.
- **Granular scope.** Consent can restrict fields, audience, and lifetime.
- **Revocable.** Consent can be withdrawn by deleting or expiring the consent file.
- **No secrets.** Never include credentials, IDs, or PII in public artifacts.

See: `DISCLOSURE_POLICY.json` for machine-readable rules.
