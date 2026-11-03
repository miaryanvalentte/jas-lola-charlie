import json, re, sys
H = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3J5VVo50uL70F327Y6AS8CqWwV6/'
BRX = 'https://brxcdn.com/uk1-app-storage/2e25bbd8-55a8-11f0-9f79-9aae66778e25/media/original/'
SUBJECT = 'A little Christmas magic, just for you ✨'
PREHEADER = 'VIP early access is open, plus a FREE candle with code FREEFLAME.'

def img_row(bg, href, src, alt, comment):
    return (f"<!-- {comment} --><tr><td align='center' style='background:{bg};padding:0;font-size:0;line-height:0;'>"
            f"<a href='{href}' target='_blank' style='display:block;text-decoration:none;'>"
            f"<img src='{src}' width='600' alt='{alt}' style='display:block;width:100%;max-width:600px;height:auto;border:0;'></a></td></tr>")

def cell(w, pct, src, alt, href=None):
    img = f"<img src='{BRX}{src}' width='{w}' alt='{alt}' style='display:block;width:100%;max-width:{w}px;height:auto;border:0;'>"
    if href:
        img = f"<a href='{href}' target='_blank' style='display:block;text-decoration:none;'>{img}</a>"
    return f"<td width='{w}' valign='top' style='width:{pct}%;padding:0;font-size:0;line-height:0;'>{img}</td>"

def row(*cells):
    return "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0' style='width:100%;'><tr>" + ''.join(cells) + "</tr></table>"

UNSUB = '{{ email.unsubscribe }}'
FOOTER = ("<!-- FOOTER: standard sliced footer (same as Thu-Sun tests, links live) --><tr><td align='center' bgcolor='#f1ece4' style='background:#f1ece4;padding:0;font-size:0;line-height:0;'>"
  + row(cell(600, '100.0', '760ecf9e-bdac-11f1-9bec-da72c3ede207', 'Share the love - refer a friend and get 15% off', 'https://valentte.com/refer-a-friend/'))
  + row(cell(600, '100.0', '9be8f870-bdac-11f1-ae3e-3a61f529e63a', 'Seamless, secure checkout. We accept Apple Pay, Google Pay, Visa, Mastercard, PayPal, Amex, Klarna and Clearpay. Fast delivery, 7 day customer care, proudly UK made.', 'https://valentte.com/cart/'))
  + row(cell(270, '45.0', '72909d34-bdac-11f1-9503-6e106daa45cc', 'Call 08000 869 311', 'tel:08000869311'),
        cell(330, '55.0', '5d27c198-bdac-11f1-9016-6a3143bb27f1', 'Email support@valentte.com', 'mailto:support@valentte.com'))
  + row(cell(118, '19.667', '8e2412a6-bdac-11f1-9dc7-e2485d303308', ''),
        cell(120, '20.0', '4ef0a180-bdac-11f1-9bec-da72c3ede207', 'Facebook', 'https://www.facebook.com/ValentteLondon'),
        cell(121, '20.167', '6ec5e3a8-bdac-11f1-b194-e2485d303308', 'TikTok', 'https://www.tiktok.com/@valentte_london'),
        cell(120, '20.0', '86d08fc0-bdac-11f1-8337-6e106daa45cc', 'Instagram', 'https://www.instagram.com/valentte_london'),
        cell(121, '20.167', '9fb55dc2-bdac-11f1-a522-da72c3ede207', ''))
  + row(cell(383, '63.833', '833168a8-bdac-11f1-aac9-e2485d303308', 'Change your contact preferences', UNSUB),
        cell(29, '4.833', '91e44a82-bdac-11f1-ad1e-da72c3ede207', 'here', UNSUB),
        cell(188, '31.333', '95978c2a-bdac-11f1-ad4c-6a3143bb27f1', '', UNSUB))
  + row(cell(600, '100.0', '7dde79d6-bdac-11f1-9dc7-e2485d303308', 'Please note: this email address is not monitored.'))
  + row(cell(332, '55.333', '7a2d97e0-bdac-11f1-ad4c-6a3143bb27f1', 'For any enquiries, please contact'),
        cell(139, '23.167', '8a562fd8-bdac-11f1-9bec-da72c3ede207', 'support@valentte.com', 'mailto:support@valentte.com'),
        cell(129, '21.5', '5946373a-bdac-11f1-bbf4-3a61f529e63a', ''))
  + row(cell(600, '100.0', 'a8900f0a-bdac-11f1-a522-da72c3ede207', 'Valentte Unit 8 &amp; 9 Artis Park, Winsford Industrial Estate, Winsford, Cheshire, CW7 3SE'))
  + row(cell(297, '49.5', '543573d2-bdac-11f1-bbf4-3a61f529e63a', 'Click here to'),
        cell(76, '12.667', '4517097e-bdac-11f1-9bec-da72c3ede207', 'Unsubscribe', UNSUB),
        cell(227, '37.833', '67e0349e-bdac-11f1-82b3-6a3143bb27f1', ''))
  + row(cell(247, '41.167', '60c1b822-bdac-11f1-b585-3a61f529e63a', ''),
        cell(100, '16.667', '6449db5a-bdac-11f1-ad1e-da72c3ede207', 'View In Browser', '{{ email.view }}'),
        cell(253, '42.167', '4b054530-bdac-11f1-9503-6e106daa45cc', ''))
  + "</td></tr>")

NAV = ''.join(f"<a href='{h}' target='_blank' class='nav-link' style='font-family:Inter,Arial,sans-serif;font-size:13px;letter-spacing:1px;color:#16171a;text-decoration:none;margin:0 14px;white-space:nowrap;'>{t}</a>"
              for h, t in [('https://valentte.com/sale/', 'Offers'), ('https://valentte.com/about-home-fragrance/', 'Home Fragrance'), ('https://valentte.com/best-sellers/', 'Best Sellers')])

HEAD = ("<!DOCTYPE html><html xmlns:v='urn:schemas-microsoft-com:vml' xmlns:o='urn:schemas-microsoft-com:office:office' lang='en'><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
  f"<title>{SUBJECT}</title><!--[if !mso]><!--><link href='https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap' rel='stylesheet'><!--<![endif]-->"
  "<style>body, table, td { margin:0; padding:0; }img { border:0; display:block; }body { background:#f2efe9; }@media only screen and (max-width:620px) {.pg-title div { font-size:18px !important; line-height:21px !important; }.pg-btn a { padding:10px 12px !important; white-space:nowrap !important; }.wrap { width:100% !important; }.nav-row { padding:0 8px 18px !important; }.nav-link { font-size:12px !important; letter-spacing:0.5px !important; margin:0 6px !important; }}</style></head>"
  "<body style='margin:0;padding:0;background:#f2efe9;'>"
  f"<div style='display:none;max-height:0;overflow:hidden;'>{PREHEADER}" + "&#847;&zwnj;&nbsp;" * 4 + "</div>"
  "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='background:#f2efe9;'><tr><td align='center' style='padding:24px 0;'>"
  "<table role='presentation' class='wrap' width='600' cellpadding='0' cellspacing='0' style='width:600px;background:#ffffff;'>"
  "<!-- HEADER --><tr><td align='center' style='padding:26px 24px 16px;'><a href='https://valentte.com/' target='_blank' style='display:block;text-decoration:none;'>"
  "<div style='font-family:Cardo,Georgia,serif;font-size:26px;letter-spacing:2px;color:#16171a;'>VALENTTE</div>"
  "<div style='font-family:Inter,Arial,sans-serif;font-size:10px;letter-spacing:3px;color:#595959;margin-top:2px;'>LONDON</div></a></td></tr>"
  f"<tr><td align='center' class='nav-row' style='padding:0 24px 18px;'>{NAV}</td></tr>")

SPACER = "<tr><td height='24' style='height:24px;font-size:0;line-height:0;background:#ffffff;'>&nbsp;</td></tr>"

BODY = (
  "<!-- DELIVERY PASS STRIP (dynamic, Mon 9 Nov daily design): pass holders see banner 1, everyone else sees banner 2 -->"
  "{% if (customer.has_delivery_pass | string | lower) in ['true', '1', 'yes'] %}"
  + img_row('#ffffff', 'https://valentte.com/sale/', H + '888d1f89-9748-46e0-888e-e5cfe1b94ee8.jpg',
            'Your delivery’s on the house. Your Unlimited Delivery Pass is live – every VIP order ships free.', 'Delivery banner 1 (pass holders)')
  + "{% else %}"
  + img_row('#ffffff', 'https://valentte.com/delivery-membership/', H + 'd06f438e-4c47-4490-b4d2-d4c4b6bd445a.jpg',
            'Want free delivery all winter? Grab our Unlimited Delivery Pass – free shipping all year.', 'Delivery banner 2 (everyone else)')
  + "{% endif %}"
  + img_row('#F4F0E9', 'https://valentte.com/home-fragrance/candles/', H + '134d6faa-0ec6-48f3-b4a7-d7876decc117.jpg',
            'VIP Gift. Your FREE Scented Candle. A little thank-you for our VIPs – add yours to any order tonight. Use code FREEFLAME. Claim my FREE candle.', 'FREE GIFT: VIP FREEFLAME (Mon)')
  + SPACER
  + img_row('#F4F0E9', 'https://valentte.com/sale/', H + 'c4e2a72b-2cc3-437f-a966-480b9e0ba532.jpg',
            'VIP early access is open. A little Christmas magic, just for you. Shop up to 44% off before anyone else, plus a FREE candle with code FREEFLAME. Your sneak peek starts now. Unwrap my VIP deals.', 'HERO: VIP early access snow globe')
  + img_row('#F4F0E9', 'https://valentte.com/sale/', H + 'f55e6104-b362-414b-a9e9-afcd00c32a97.jpg',
            'Your VIP picks… Best sellers, up to 44% off – before anyone else', 'PICKS HEADING')
  + img_row('#F4F0E9', 'https://valentte.com/organic/best-selling-gift-box-cardamom-nutmeg/', H + '6cc1704f-b7f5-45c2-ae1f-f88afbb33270.jpg',
            'Best-Selling Gift Box Cardamom &amp; Nutmeg. Was £37.99, now £23.99. 37% off. Shop now.', 'PRODUCT 1')
  + img_row('#F4F0E9', 'https://valentte.com/organic/100ml-diffuser-refill-portofino-bay/', H + '85695243-690b-47ef-bbf4-669684ded1ab.jpg',
            'Portofino Bay 100ml Diffuser Refill. Was £17.99, now £9.99. 44% off. Shop now.', 'PRODUCT 2')
  + img_row('#F4F0E9', 'https://valentte.com/organic/customer-favourites-mini-mist-box-of-4/', H + '01501996-493e-470b-8d44-951034028240.jpg',
            'Customer Favourites Mini Mist Box of 4. Was £13.49, now £7.99. 41% off. Shop now.', 'PRODUCT 3')
  + img_row('#F4F0E9', 'https://valentte.com/organic/bergamot-and-lemon-100ml-diffuser-refill/', H + 'fa9bf7e5-e845-4cd2-9eb8-98b593adf670.jpg',
            'Bergamot &amp; Lemon 100ml Diffuser Refill. Was £17.99, now £10.49. 42% off. Shop now.', 'PRODUCT 4')
  + img_row('#ffffff', 'https://valentte.com/christmas/', H + '8feb0ea1-f0e9-45c1-b61a-b47c43307928.gif',
            'Valentte Christmas Shop. Candles, reed diffusers, gift boxes, hand cream, soap, wax melts and more. Shop Christmas Gifts.', 'BOTTOM BANNER: Christmas Shop animated GIF (Shop Christmas Gifts)')
  + SPACER
  + "<tr><td align='center' style='padding:6px 40px 14px;font-family:Inter,Arial,sans-serif;font-size:11px;line-height:16px;color:#555555;'>Disclaimer: Free gifts may vary from time to time depending on availability and stock levels.</td></tr>"
)
html = HEAD + BODY + FOOTER + "</table></td></tr></table></body></html>"

# sanity checks
assert html.count('<a ') == html.count('</a>'), (html.count('<a '), html.count('</a>'))
assert html.count('{{ email.unsubscribe }}') == 4
assert '8feb0ea1-f0e9-45c1-b61a-b47c43307928.gif' in html
for w in [[600], [600], [270, 330], [118, 120, 121, 120, 121], [383, 29, 188], [600], [332, 139, 129], [600], [297, 76, 227], [247, 100, 253]]:
    assert sum(w) == 600, w
open('/tmp/claude-0/-home-user-jas-lola-charlie/87cc9deb-3095-5e13-be9b-5f41cdf89fc6/scratchpad/mon/mon.html', 'w').write(html)
design = {"data": {"file_ids": [], "jinja_html": html, "preheader": PREHEADER,
                   "provider": {"channel_extension_id": "68937dd3466bc23a502c8b27", "type": "channel_extension"},
                   "reply_to": "support@valentte.com", "sender_email": "marketing@marketing.valentte.com",
                   "sender_name": "Valentte", "subject": SUBJECT, "translations": {}}, "type": "raw"}
json.dump(design, open('/tmp/claude-0/-home-user-jas-lola-charlie/87cc9deb-3095-5e13-be9b-5f41cdf89fc6/scratchpad/mon/design.json', 'w'), ensure_ascii=False)
print('ok', len(html), 'anchors', html.count('<a '), 'imgs', html.count('<img '))
