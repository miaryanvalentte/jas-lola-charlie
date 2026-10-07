# Project rules

## Bloomreach email frequency policy (permanent rule)

Every email Claude uploads into Bloomreach Engagement must use the **"Unlimited Policy"** frequency policy (policy id `unlimited-policy`). This applies to:

- standalone email campaigns (`create_email_campaign` / `update_email_campaign`): set `frequency_policy: "unlimited-policy"` in the payload
- send-email nodes inside scenarios (`create_scenario` / `update_scenario`): set each email node's frequency policy to `unlimited-policy`

Never leave it on the project default, "Default", "Abandoned Email Policy", "Smart Newsletter Policy" or any other policy, and never copy another node's policy. After every write, re-fetch and confirm the policy reads `unlimited-policy`.
