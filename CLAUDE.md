# Project rules

## Bloomreach emails

- **Always set "Transfer identity to URL links" to "Enabled (only first click)"** on every email put into Bloomreach — campaigns, scenario/flow email nodes, and raw-HTML emails alike. In the API this is `transfer_identity: true` and `transfer_user_identity: "first_click"`.
  - Never leave it "Disabled": clickers land anonymous, get new-visitor pop-ups and lose basket/attribution (this happened on the Evening Email 28/10/26).
  - Never use "Enabled (all clicks)": forwarded or shared emails can tie someone else's browsing to the customer.
  - Hand-built / raw-HTML emails don't inherit this from the BEE template — check it explicitly before scheduling.
