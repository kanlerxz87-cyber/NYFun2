/* ==========================================================================
   NYC Trip Planning — dataset
   EVERY value below was read from the official/primary source cited in
   `sources` (or in the row's own link) on 2026-11-25.
   A value that could not be confirmed is left as "" and carries a flag id.
   Never write a guessed number into this file.
   ========================================================================== */

window.RESEARCH_DATE = '2026-11-25';

/* ---------- 1. MICHELIN COVERAGE (official counts + official list links) --- */
window.MICHELIN_COVERAGE = [
  { tier: '3 Stars',            count: 5,   meaning: 'Exceptional cuisine',
    url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin', enumerated: 'all 5 named below' },
  { tier: '2 Stars',            count: 14,  meaning: 'Excellent cooking',
    url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/2-stars-michelin', enumerated: '3 of 14 named below' },
  { tier: '1 Star',             count: 50,  meaning: 'High quality cooking',
    url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin',  enumerated: '3 of 50 named below' },
  { tier: 'Bib Gourmand',       count: 76,  meaning: 'Good quality, good value cooking',
    url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/bib-gourmand',     enumerated: 'none named yet' },
  { tier: 'Selected (no star)', count: 224, meaning: 'Good cooking — guide-listed only',
    url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants',                  enumerated: '2 sampled (Oriana, Mūje)' }
];

/* ---------- 2. HOTELS ------------------------------------------------------
   Prices are live Booking.com rates for Mon 15 Feb -> Mon 22 Feb 2027
   (7 nights, 2 adults, 1 room, USD), read on 2026-11-25.
   "pre-tax" = Booking's quoted total, which already includes the property's
   resort/facility fee. "est. all-in" = pre-tax + the tax lines Booking lists.
   ------------------------------------------------------------------------- */
window.HOTELS = [
  {
    id: 'H1',
    name: 'Hyatt Place New York / Chelsea',
    district: 'Chelsea (Flatiron border)',
    address: '140 West 24th Street, New York, NY 10011',
    zip: '10011',
    room: 'King Room, 180 sq ft',
    bed: '1 king bed (meets “queen or bigger”)',
    bath: 'Attached (private) bathroom',
    nightly: 159,
    total7: 1113,
    tax_line: '14.75% tax + $4 city tax / night',
    est_allin: 1305,
    terms: 'Buffet breakfast included · free cancellation before 13 Feb 2027 · no prepayment',
    src_price: 'https://www.booking.com/hotel/us/hyatt-place-new-york-chelsea.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1',
    src_official: 'https://www.hyatt.com/hyatt-place/en-US/lgazc-hyatt-place-new-york-chelsea/hotel-info',
    note: 'Cheapest of the four priced hotels and the only one with breakfast in the rate.'
  },
  {
    id: 'H2',
    name: 'Arlo NoMad',
    district: 'NoMad / Flatiron',
    address: { v: '', flag: 'F-04' },
    zip: { v: '', flag: 'F-04' },
    room: 'Queen Room, 150 sq ft',
    bed: '1 queen bed',
    bath: 'Room has private facilities — bathroom type not stated on the rate line',
    nightly: 173,
    total7: 1214,
    tax_line: '$136 room + $37 resort fee / night; 14.75% tax + $4 city tax + $1 tourism fee / night',
    est_allin: 1428,
    terms: 'Includes $37/night resort fee · “Black Friday Deal” 39% off (valid on stays 19 Nov 2026–31 Dec 2027) · free cancellation · no prepayment',
    src_price: 'https://www.booking.com/hotel/us/arlo-nomad.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1',
    src_official: 'https://arlohotels.com/nomad/rooms/',
    note: 'Queen and King room types both offered (official room list). Booking describes it as ~1,056 ft from the Empire State Building and ~1,056 ft from the 6 train at 33rd St & Park Ave.'
  },
  {
    id: 'H3',
    name: '11 Howard (Design Hotels)',
    district: 'SoHo',
    address: '11 Howard Street, New York, NY 10013',
    zip: '10013',
    room: 'Queen Room',
    bed: '1 queen bed',
    bath: 'Private bathroom (5-star hotel; room type listed as Queen Room)',
    nightly: 218,
    total7: 1522,
    tax_line: '$182 room + $35 resort fee / night; 14.74% tax + $4 city tax / night',
    est_allin: 1774,
    terms: 'Non-refundable $1,522 · flexible rate $1,948 (free cancellation before 14 Feb 2027) · breakfast on the flexible rate',
    src_price: 'https://www.booking.com/hotel/us/11-howard.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1',
    src_official: 'https://www.11howard.com/',
    note: 'Only hotel of the four that shares a ZIP code with a verified MICHELIN-starred kitchen (Atera, 10013). Guest score 7.6/10; rooms repeatedly described as small.'
  },
  {
    id: 'H4',
    name: 'The Beekman, a Thompson Hotel (Hyatt)',
    district: 'Financial District',
    address: '123 Nassau Street, New York, NY 10038',
    zip: '10038',
    room: 'King Room, 300 sq ft',
    bed: '1 king bed (also sells Queen Rooms)',
    bath: 'Private bathroom with shower, bathrobes, slippers',
    nightly: 641,
    total7: 4488,
    tax_line: '$584 room + $57 resort fee / night; 14.75% city tax + $6 destination tax + $2 tax + $2 tourism fee / night',
    est_allin: 5220,
    terms: 'Non-refundable $4,488 · flexible rate $4,942 (free cancellation before 14 Feb 2027) · continental breakfast $38 pp/night',
    src_price: 'https://www.booking.com/hotel/us/the-beekman-a-thompson-hotel.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1',
    src_official: 'https://www.hyatt.com/thompson-hotels/en-US/nycth-the-beekman-a-thompson-hotel/overview',
    note: '4–5× the price of the other three for the same 7 nights. Included as the "splurge" reference point, not as a recommendation.'
  }
];

/* ---------- 3. MICHELIN PROXIMITY PER HOTEL -------------------------------
   Only same-ZIP-code matches are asserted, because ZIP is printed on both
   the hotel and the restaurant record. Travel times are NOT asserted —
   see flag F-01. Each row links a pre-built Google Maps transit query.
   ------------------------------------------------------------------------- */
window.HOTEL_CLUSTERS = [
  {
    id: 'H1', name: 'Hyatt Place NY / Chelsea', zip: '10011',
    same_zip_starred: 0,
    venues: 'No verified MICHELIN venue in 10011',
    transit_note: 'One subway ride to the NoMad/Flatiron and Theatre District clusters',
    dirs: 'https://www.google.com/maps/dir/?api=1&origin=140+West+24th+Street+New+York&destination=155+West+51st+Street+New+York&travelmode=transit'
  },
  {
    id: 'H2', name: 'Arlo NoMad', zip: '',
    same_zip_starred: '',
    venues: 'ZIP code not yet captured — see F-04',
    transit_note: 'Walking-distance to the NoMad/Flatiron cluster per Booking’s own location notes',
    dirs: 'https://www.google.com/maps/dir/?api=1&origin=Arlo+NoMad+New+York&destination=11+Madison+Ave+New+York&travelmode=transit'
  },
  {
    id: 'H3', name: '11 Howard (SoHo)', zip: '10013',
    same_zip_starred: 1,
    venues: 'Atera ★★ (77 Worth St, 10013)',
    transit_note: 'Same ZIP as Atera; MICHELIN’s Le Coucou ★ record links to this hotel',
    dirs: 'https://www.google.com/maps/dir/?api=1&origin=11+Howard+Street+New+York&destination=77+Worth+Street+New+York&travelmode=transit'
  },
  {
    id: 'H4', name: 'The Beekman (FiDi)', zip: '10038',
    same_zip_starred: 0,
    venues: 'No verified MICHELIN venue in 10038',
    transit_note: 'Downtown base; Atera (10013) is the nearest verified starred kitchen',
    dirs: 'https://www.google.com/maps/dir/?api=1&origin=123+Nassau+Street+New+York&destination=77+Worth+Street+New+York&travelmode=transit'
  }
];

/* ---------- 4. MICHELIN RESTAURANTS --------------------------------------
   stars: 3 / 2 / 1, or 0 for "guide-listed, no star".
   Hours/addresses are copied verbatim from the MICHELIN Guide record;
   social links are only filled when an official/booking-partner page
   printed the handle.
   ------------------------------------------------------------------------ */
window.RESTAURANTS = [
  {
    id: 'R1', name: 'Le Bernardin', stars: 3, cuisine: 'Seafood, French',
    price_band: '$$$$ (MICHELIN)', zip: '10019',
    address: '155 W 51st St, New York, NY 10019',
    hours: { v: 'Mon–Wed: 12:00–2:30 PM and 5:00–10:30 PM. Thu–Sun: not captured', flag: 'F-03' },
    exceptions: 'Business casual dress code (jackets recommended, not required); shorts/t-shirts/sneakers not permitted. Reservations required for the dining room; lounge is walk-in. 48-hour cancellation window, $150 per person fee.',
    cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/le-bernardin',
    official: 'https://www.le-bernardin.com/',
    resy: 'https://resy.com/cities/new-york-ny/venues/le-bernardin',
    instagram: 'https://instagram.com/lebernardinny',
    facebook: 'https://facebook.com/LeBernardin',
    youtube: '', tiktok: '',
    phone: '+1 212-554-1515'
  },
  {
    id: 'R2', name: 'Eleven Madison Park', stars: 3, cuisine: 'Contemporary, vegan option',
    price_band: '$$$$ (MICHELIN)', zip: '10010',
    address: '11 Madison Ave, New York, NY 10010',
    hours: 'Mon–Thu: 5:30–10:00 PM · Fri–Sun: 12:00–1:00 PM and 5:30–11:00 PM',
    exceptions: 'No dress code (stated by MICHELIN). Tasting menu with a vegan path.',
    cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/eleven-madison-park',
    official: 'https://www.elevenmadisonpark.com/',
    resy: 'https://resy.com/cities/new-york-ny/venues/eleven-madison-park',
    instagram: 'https://instagram.com/elevenmadisonpark',
    facebook: 'https://facebook.com/jalexandersrestaurantscollection',
    youtube: '', tiktok: '',
    phone: '+1 212-889-0905'
  },
  {
    id: 'R3', name: 'Per Se', stars: 3, cuisine: 'Contemporary, French',
    price_band: '$$$$ (MICHELIN)', zip: '10019',
    address: '10 Columbus Circle, New York, NY 10019',
    hours: 'Daily 4:30–9:00 PM',
    exceptions: 'Tasting-menu format; reservations via Tock (the booking link MICHELIN publishes).',
    cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/per-se',
    official: 'https://www.thomaskeller.com/perseny',
    resy: '',
    instagram: '', facebook: '', youtube: '', tiktok: '',
    phone: '+1 212-823-9335'
  },
  {
    id: 'R4', name: 'Atera', stars: 2, cuisine: 'Contemporary (counter tasting menu)',
    price_band: '$$$$ (MICHELIN)', zip: '10013',
    address: '77 Worth St, New York, NY 10013',
    hours: 'Mon 7:00–10:00 PM · Tue–Fri 5:00–10:00 PM · Sat 1:30–10:00 PM · Sun 5:00–10:00 PM',
    exceptions: 'Counter seating only (U-shaped counter). Reservations via Tock.',
    cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/atera',
    official: 'https://ateranyc.com/',
    resy: '',
    instagram: '', facebook: '', youtube: '', tiktok: '',
    phone: '+1 212-226-1444'
  },
  {
    id: 'R5', name: 'Sushi Sho', stars: 3, cuisine: 'Japanese / sushi',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: '',
    cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/sushi-sho-1213976',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  },
  {
    id: 'R6', name: 'Jungsik', stars: 3, cuisine: 'Korean',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: '', cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/jungsik-new-york',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  },
  {
    id: 'R7', name: 'Saga', stars: 2, cuisine: 'Contemporary',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: '', cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/saga',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  },
  {
    id: 'R8', name: 'Joo Ok', stars: 2, cuisine: 'Korean',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: '', cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/joo-ok-1214822',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  },
  {
    id: 'R9', name: 'Le Coucou', stars: 1, cuisine: 'French',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: 'MICHELIN links it as the restaurant inside the MICHELIN-selected hotel 11 Howard.',
    cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/le-coucou',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  },
  {
    id: 'R10', name: 'Muku', stars: 1, cuisine: 'Japanese',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: '', cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/muku',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  },
  {
    id: 'R11', name: 'Huso', stars: 1, cuisine: 'Contemporary',
    price_band: '$$$$ (MICHELIN)', zip: '',
    address: { v: '', flag: 'F-02' },
    hours: { v: '', flag: 'F-02' },
    exceptions: '', cost2: { v: '', flag: 'F-06' },
    michelin: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/huso-1218089',
    official: '', resy: '', instagram: '', facebook: '', youtube: '', tiktok: '', phone: ''
  }
];

/* ---------- 5. ACTIVITIES -------------------------------------------------
   Only venues whose official page was actually read appear here.
   ------------------------------------------------------------------------ */
window.ACTIVITIES = [
  {
    id: 'A1', name: 'The Metropolitan Museum of Art (The Met Fifth Avenue)',
    category: 'Museum / art',
    address: '1000 Fifth Avenue, New York, NY 10028',
    hours: { v: 'Not captured from the official page', flag: 'F-07' },
    exceptions: 'Pay-what-you-wish admission restricted to NY State residents and NY/NJ/CT students (ID + NY billing address required online). Closed-day information not captured.',
    cost: 'Adults $30 · Seniors 65+ $22 · Students $17 · Under 12 free',
    booking: 'Advance tickets optional',
    official: 'https://www.metmuseum.org/plan-your-visit',
    instagram: '', youtube: '', tiktok: '',
    transit: 'Subway 4/5/6 to 86th St then 3 blocks west, or M1/M2/M3/M4 bus to 82nd–83rd St (stated by the museum)'
  },
  {
    id: 'A2', name: '9/11 Memorial (reflecting pools)',
    category: 'Memorial / free',
    address: { v: '', flag: 'F-15' },
    hours: 'Open daily 8:00 AM – 8:00 PM',
    exceptions: 'Free and open to the public; no ticket required.',
    cost: 'Free',
    booking: 'No ticket needed',
    official: 'https://www.911memorial.org/visit',
    instagram: '', youtube: '', tiktok: '',
    transit: 'World Trade Center / Cortlandt St stations (area served by multiple lines)'
  },
  {
    id: 'A3', name: '9/11 Memorial Museum',
    category: 'Museum / history',
    address: { v: '', flag: 'F-15' },
    hours: 'Wed–Mon plus select Tuesdays, 9:00 AM – 7:00 PM (last entry 5:30 PM)',
    exceptions: 'Closed most Tuesdays — the official page says “six days a week (plus select Tuesdays)”. Advance ticket purchase required.',
    cost: { v: '', flag: 'F-08' },
    booking: 'Advance ticket required',
    official: 'https://www.911memorial.org/visit',
    instagram: '', youtube: '', tiktok: '',
    transit: 'World Trade Center / Cortlandt St stations'
  },
  {
    id: 'A4', name: 'Top of the Rock Observation Deck',
    category: 'Observation deck',
    address: { v: '', flag: 'F-15' },
    hours: '8:00 AM – 12:00 AM (live “OPEN 8 AM – 12 AM” indicator on the official ticket page)',
    exceptions: 'Timed admission — you pick a date and entry time. Prices vary by date/time band.',
    cost: 'Timed admission from $42 · All-Inclusive Pass (deck + The Beam + SKYLIFT) from $82',
    booking: 'Timed ticket recommended',
    official: 'https://www.rockefellercenter.com/tickets/top-of-the-rock-observation-deck/',
    instagram: '', youtube: '', tiktok: '',
    transit: 'Rockefeller Center, Midtown Manhattan — subway stations nearby are not named on the official ticket page'
  }
];

/* ---------- 6. ACTIVITY CANDIDATE BACKLOG (not yet verified) --------------- */
window.ACTIVITY_BACKLOG = [
  { name: 'Central Park', why: 'Free, open-air, fits any weather gap', official: 'https://www.centralparknyc.org/', status: 'Hours not yet read from the official source' },
  { name: 'The High Line', why: 'Free elevated park, Chelsea — walkable from H1', official: 'https://www.thehighline.org/visit/', status: 'Official page returned only a cookie notice — hours unread' },
  { name: 'Brooklyn Bridge walk', why: 'Free, iconic, ~1 hour each way', official: 'https://www.nycgovparks.org/parks/brooklyn-bridge-park', status: 'Not yet verified' },
  { name: 'Museum of Modern Art (MoMA)', why: 'Major museum, Midtown', official: 'https://www.moma.org/plan-your-visit/', status: 'Official page failed to load twice — hours/price unread (F-07)' },
  { name: 'American Museum of Natural History', why: 'Upper West Side, pairs with Central Park', official: 'https://www.amnh.org/plan-your-visit', status: 'Homepage read; hours live on a separate page — unread' },
  { name: 'Broadway show', why: 'Peak NYC evening; February is a discount month', official: 'https://www.playbill.com/', status: 'No ticketing source verified yet (F-14)' },
  { name: 'Statue of Liberty / Ellis Island ferry', why: 'Half-day, weather-dependent', official: 'https://www.nps.gov/stli/index.htm', status: 'Not yet verified' },
  { name: 'Chelsea Market / food halls', why: 'Rainy-day eating, near H1', official: 'https://www.chelseamarket.com/', status: 'Not yet verified' }
];

/* ---------- 7. ITINERARY (7 nights, 15–22 Feb 2027) -----------------------
   Every scheduled venue is only placed on a day the venue is verifiably open.
   ------------------------------------------------------------------------ */
window.ITINERARY = [
  { day: 'Mon 15 Feb', kind: 'Arrival', morning: 'Arrive, check in (H1/H2/H3), settle in',
    afternoon: 'Walk the neighbourhood; no timed ticket',
    evening: 'Dinner: Atera ★★ — verified open Monday 7:00–10:00 PM',
    why: 'Atera is the only 2★/3★ venue whose Monday hours were verified as starting at 7 PM.' },
  { day: 'Tue 16 Feb', kind: 'Culture', morning: 'The Met (Fifth Avenue) — arrive at opening',
    afternoon: 'Central Park walk back south',
    evening: 'Dinner: Eleven Madison Park ★★★ — verified open Tue 5:30–10:00 PM',
    why: 'Met hours not yet verified (F-07) — keep this day flexible; 9/11 Museum is closed most Tuesdays.' },
  { day: 'Wed 17 Feb', kind: 'Downtown', morning: '9/11 Memorial (free, daily 8–8) then Museum (open Wed 9–7)',
    afternoon: 'Walk Tribeca / SoHo',
    evening: 'Dinner: Le Bernardin ★★★ — verified open Wed 5:00–10:30 PM',
    why: 'The only weekday where both the 9/11 Museum (Wed) and Le Bernardin’s captured hours line up.' },
  { day: 'Thu 18 Feb', kind: 'Flex / preferred-window end', morning: 'Open — this is the last day of the preferred 15–18 Feb window',
    afternoon: 'Shopping / High Line (pending verification)',
    evening: 'Dinner: Per Se ★★★ — verified open daily 4:30–9:00 PM',
    why: 'Le Bernardin Thu–Sun hours are unverified (F-03), so Per Se is used for Thursday.' },
  { day: 'Fri 19 Feb', kind: 'Midtown', morning: 'Top of the Rock (open 8 AM–12 AM, timed ticket)',
    afternoon: 'Museum Mile or shopping',
    evening: 'Dinner: Eleven Madison Park ★★★ — verified Fri 12–1 PM and 5:30–11 PM',
    why: 'EMP is open for both lunch and dinner Fri–Sun.' },
  { day: 'Sat 20 Feb', kind: 'Downtown / Brooklyn', morning: 'Brooklyn Bridge walk (pending verification)',
    afternoon: 'DUMBO / Williamsburg',
    evening: 'Dinner: Atera ★★ — verified Sat 1:30–10:00 PM (earlier service than weeknights)',
    why: 'Saturday is the only day Atera opens in the afternoon.' },
  { day: 'Sun 21 Feb', kind: 'Wind-down', morning: 'Neighbourhood you liked most',
    afternoon: 'Pack, late check-out request',
    evening: 'Dinner: Per Se ★★★ or Le Bernardin ★★★ (Sunday hours unverified, F-03)',
    why: 'Sunday is deliberately light — the only verified Sunday-serviced 3★ is Per Se (daily 4:30–9).' },
  { day: 'Mon 22 Feb', kind: 'Departure', morning: 'Check out, airport transfer',
    afternoon: '—', evening: '—', why: 'Check-out date of the 7-night rate used in the hotel table.' }
];

/* ---------- 8. BUDGET ----------------------------------------------------- */
window.BUDGET = [
  { item: 'Hotel — Hyatt Place NY/Chelsea, King Room, 7 nights', amount: 1305, basis: 'All-in estimate: $1,113 pre-tax + 14.75% tax + $4/night city tax', status: 'verified', src: 'https://www.booking.com/hotel/us/hyatt-place-new-york-chelsea.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1' },
  { item: 'Hotel — Arlo NoMad, Queen Room, 7 nights', amount: 1428, basis: 'All-in estimate: $1,213.96 pre-tax + 14.75% tax + $4 city tax + $1 tourism fee per night', status: 'verified', src: 'https://www.booking.com/hotel/us/arlo-nomad.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1' },
  { item: 'Hotel — 11 Howard, Queen Room, 7 nights (non-refundable)', amount: 1774, basis: 'All-in estimate: $1,522 pre-tax + 14.74% tax + $4 city tax per night', status: 'verified', src: 'https://www.booking.com/hotel/us/11-howard.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1' },
  { item: 'Hotel — The Beekman, King Room, 7 nights (non-refundable)', amount: 5220, basis: 'All-in estimate: $4,488 pre-tax + 14.75% + $6 destination + $2 tax + $2 tourism per night', status: 'verified', src: 'https://www.booking.com/hotel/us/the-beekman-a-thompson-hotel.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1' },
  { item: 'Subway / local bus fares', amount: '', basis: 'MTA lists $3 per ride (subway and local bus). Cost depends on how many rides you take — not modelled.', status: 'verified', src: 'https://www.mta.info/fares-tolls' },
  { item: 'The Met — 2 adult tickets', amount: 60, basis: '$30 per adult, official ticket table', status: 'verified', src: 'https://www.metmuseum.org/plan-your-visit' },
  { item: 'Top of the Rock — 2 timed tickets', amount: 84, basis: '“From $42” each — live price varies by date/time band, so $84 is the floor', status: 'verified', src: 'https://www.rockefellercenter.com/tickets/top-of-the-rock-observation-deck/' },
  { item: '9/11 Memorial Museum — 2 tickets', amount: '', basis: 'Ticket price not captured from the official page (F-08)', status: 'unverified', src: 'https://www.911memorial.org/visit' },
  { item: 'Michelin dinners — 4 dinners for 2', amount: '', basis: 'No per-person menu price is published on any page reachable in this session (F-06). The MICHELIN price band is $$$$ for every starred row.', status: 'unverified', src: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin' },
  { item: 'Flights / airfare', amount: '', basis: 'Not researched in this session (F-12)', status: 'unverified', src: '' },
  { item: 'Broadway / theatre tickets', amount: '', basis: 'Not researched in this session (F-14)', status: 'unverified', src: '' }
];

/* ---------- 9. BOOKING-TIMING EVIDENCE ----------------------------------- */
window.PRICE_WINDOWS = [
  { window: '15–22 Feb 2027 (primary)', nights: 7, observed: 'Priced in this session for 4 hotels',
    note: 'Hyatt Place $1,113 · Arlo NoMad $1,213.96 · 11 Howard $1,522 · Beekman $4,488 (all pre-tax)',
    status: 'verified' },
  { window: 'Booking channel / timing', nights: 7, observed: 'Promotional discount active on 2026-11-25',
    note: 'Arlo NoMad showed a “Black Friday Deal — 39% off, valid on stays 19 Nov 2026 to 31 Dec 2027”. Booking now, inside that promo window, is cheaper than the same dates at list price.',
    status: 'verified' },
  { window: 'Other candidate weeks (22 Feb–1 Mar, 1–8 Mar, 8–15 Mar, 15–22 Mar 2027)', nights: 7,
    observed: 'Not priced', note: 'Cross-window comparison was not run in this session — see Q-05 / F-09.',
    status: 'unverified' }
];

/* ---------- 10. SUGGESTIONS ---------------------------------------------- */
window.SUGGESTIONS = [
  { id: 'S1', title: 'Add a routing-API integration so the “1 hour or less” rule is measured, not assumed',
    impact: 'High', effort: 'Medium',
    problem: 'The brief asks hotels to be ranked by MICHELIN venues reachable within 1 hour by subway/bus. This site can only assert same-ZIP proximity, because no transit-routing source was reachable in the session.',
    proposal: 'Wire a Google Directions or MTA trip-planner query into the build: for each hotel × starred restaurant, store the first transit itinerary duration, then rank by count(≤60 min). Cache the results so the page stays static.',
    effort_note: 'One API key, ~70×8 = 560 route queries, cached as JSON.',
    done_when: 'Every hotel row shows a measured door-to-door transit time with a timestamp.' },
  { id: 'S2', title: 'Capture per-person menu prices from the restaurants’ own menu pages',
    impact: 'High', effort: 'Low',
    problem: 'The “cost for 2 adults” column is empty for every starred restaurant. Michelin only publishes a $$$$ band, and the restaurants’ sites are JavaScript-rendered.',
    proposal: 'Open each restaurant’s menu PDF/HTML in a real browser session and record the tasting-menu price per person, then multiply by 2 and add the stated service/tax treatment.',
    effort_note: '~20 minutes per restaurant.',
    done_when: 'Every starred row has a per-person price plus a capture date.' },
  { id: 'S3', title: 'Complete the MICHELIN index (all 69 starred + 76 Bib Gourmand)',
    impact: 'High', effort: 'Medium',
    problem: 'Only 5 of 5 three-star, 3 of 14 two-star and 3 of 50 one-star restaurants are individually catalogued here. The official list pages paginate at 48 per page, which is why the pass stopped early.',
    proposal: 'Walk the official filtered lists page by page and store name, distinction, cuisine, price band, address, and the MICHELIN URL. Then the cluster ranking becomes a real ranking.',
    effort_note: '11 listing pages + 69 detail pages.',
    done_when: 'Counts on the site match the official counters exactly, row for row.' },
  { id: 'S4', title: 'Verify social accounts only where an official page prints them',
    impact: 'Medium', effort: 'Low',
    problem: 'The brief wants a YouTube/TikTok/Instagram link for every venue. Only Le Bernardin and Eleven Madison Park had handles printed on an official booking-partner page.',
    proposal: 'Treat “official page prints the handle” as the acceptance test. Where a creator video is wanted, store the video URL with channel name and publish date instead of the account, and mark it “creator content, not official”.',
    effort_note: 'No new tooling; a rule and a checklist.',
    done_when: 'Every social cell is either a link from the venue’s own site, or visibly labelled “creator content”.' },
  { id: 'S5', title: 'Price three alternative weeks before committing',
    impact: 'High', effort: 'Low',
    problem: 'Only the 15–22 Feb window was priced. The brief explicitly allows 15 Feb–23 Mar 2027 and asks for the cheapest time to book.',
    proposal: 'Re-run the same four hotels for 22 Feb–1 Mar, 1–8 Mar, 8–15 Mar and 15–22 Mar, and add a 14-night row. Compare like-for-like pre-tax totals.',
    effort_note: '16 more rate checks.',
    done_when: 'A 5-window × 4-hotel price matrix exists with capture dates.' },
  { id: 'S6', title: 'Show the difference between the refundable and non-refundable rate',
    impact: 'Medium', effort: 'Low',
    problem: 'The gap is material: 11 Howard is $1,522 non-refundable vs $1,948 flexible (+$426); Beekman $4,488 vs $4,942 (+$454). The site shows both but does not decide.',
    proposal: 'Add an explicit “insurance price” column and a rule of thumb: pay the premium only when the trip date is not yet locked.',
    effort_note: 'Presentation change only.',
    done_when: 'Each hotel row shows the flexibility premium in dollars.' },
  { id: 'S7', title: 'Split the site into “decision” and “evidence” layers',
    impact: 'Medium', effort: 'Low',
    problem: 'A reader who wants “which hotel” currently scrolls past methodology to get there.',
    proposal: 'Keep the dashboard as the decision layer (3 cards max), and push every method note, flag and source into the register pages that already exist.',
    effort_note: 'Information architecture only.',
    done_when: 'Each decision fits on one phone screen.' },
  { id: 'S8', title: 'Add a live “re-check” button per price row',
    impact: 'Medium', effort: 'Medium',
    problem: 'Prices move daily; a static page becomes wrong silently.',
    proposal: 'Each price row links to the exact rate URL used (already done) and shows a “captured on” date. Extend it with a scheduled weekly re-capture that overwrites the JSON and shows a diff.',
    effort_note: 'A GitHub Action plus a small scraper.',
    done_when: 'No price on the site is older than 7 days without a visible warning.' },
  { id: 'S9', title: 'Verify opening hours at the venue’s own page, not the aggregator',
    impact: 'Medium', effort: 'Low',
    problem: 'The Met’s and Le Bernardin’s full weekly hours could not be captured, which weakens the itinerary.',
    proposal: 'Use a browser session (JS enabled) and photograph/save the hours block; store the exact text plus the page URL.',
    effort_note: '~10 venues.',
    done_when: 'Every row has all seven days or an explicit “closed” marker.' },
  { id: 'S10', title: 'Decide the trip length before ranking hotels',
    impact: 'High', effort: 'Low',
    problem: 'The brief allows 1–2 weeks, or even 2–4 weeks. Every cost on this site is a 7-night figure, so the comparison is only valid for a 7-night plan.',
    proposal: 'Lock 7 / 14 / 21 nights first, then re-price. Hotel totals scale roughly linearly but weekly discounts and promo windows do not.',
    effort_note: 'A single decision.',
    done_when: 'One trip length is chosen and every table header states it.' }
];

/* ---------- 11. OPEN QUESTIONS ------------------------------------------- */
window.QUESTIONS = [
  { id: 'Q-01', area: 'Dates', question: 'Is the trip 7 nights (15–22 Feb 2027), or the 4-night preferred window (15–18 Feb), or 14–28 nights?',
    known: 'Preferred vacation time is 15–18 Feb 2027; total length allowed is 1–2 weeks, possibly 2–4 weeks. Every price here is 7 nights.',
    missing: 'The chosen length. Costs, hotel choice and itinerary density all change with it.',
    how: 'Decide, then re-run the 4 hotels at the chosen length (S5, S10).', link: '' },
  { id: 'Q-02', area: 'Budget', question: 'What is the total budget for two adults, hotels included?',
    known: 'Cheapest compliant hotel is $1,113 pre-tax / ≈$1,305 all-in for 7 nights. Michelin dinners are all $$$$ band.',
    missing: 'A ceiling. Without it, “best hotel” cannot be defined — Beekman is defensible at one budget and absurd at another.',
    how: 'Set a ceiling and a split (hotel % vs food %).', link: '' },
  { id: 'Q-03', area: 'Hotel', question: 'Which single criterion dominates: price, bed size, or MICHELIN walkability?',
    known: 'Four hotels priced: $1,305 / $1,428 / $1,774 / $5,220 all-in. Only 11 Howard shares a ZIP with a verified starred kitchen.',
    missing: 'A weighting. The ranking is genuinely different under each priority.',
    how: 'Pick a priority, or accept the default order on the Hotels page.', link: 'hotels.html' },
  { id: 'Q-04', area: 'Hotel', question: 'Does a private bathroom need to be en-suite, or is a private-but-down-the-hall bathroom acceptable?',
    known: 'All four shortlisted hotels have attached private bathrooms. Cheap New York inventory that fails this rule (shared bathroom) is what made the $680–$794 seven-night rates on Booking fail the brief.',
    missing: 'Your definition. It changes the price floor by ~$400 per week.',
    how: 'Confirm “en-suite”, then keep the current filter.', link: 'hotels.html' },
  { id: 'Q-05', area: 'Pricing', question: 'Is the 15–22 Feb week actually the cheapest inside the 15 Feb–23 Mar window?',
    known: 'Four hotels priced for 15–22 Feb on 2026-11-25, including a 39% “Black Friday Deal” promotion on Arlo NoMad.',
    missing: 'Prices for the other candidate weeks — never captured (F-09).',
    how: 'Run the same four rate checks for each candidate week (S5).', link: 'hotels.html#timing' },
  { id: 'Q-06', area: 'Michelin', question: 'Which of the 69 starred restaurants do you actually want to eat at?',
    known: 'Official counts: 5 three-star, 14 two-star, 50 one-star, 76 Bib Gourmand, 224 selected.',
    missing: '48 one-star and 11 two-star entries are not individually catalogued yet (F-02), so no informed shortlist exists.',
    how: 'Complete S3, then shortlist by cuisine and neighbourhood.', link: 'michelin.html' },
  { id: 'Q-07', area: 'Michelin', question: 'How much per person is a starred dinner in February 2027?',
    known: 'Every starred restaurant sits in the $$$$ MICHELIN band.',
    missing: 'Actual menu prices — not published on any page reachable here (F-06).',
    how: 'Read each restaurant’s menu page in a browser (S2).', link: 'michelin.html' },
  { id: 'Q-08', area: 'Transit', question: 'How long is the real door-to-door transit time from each hotel to each starred restaurant?',
    known: 'MTA subway/local bus fare is $3 per ride; express bus $7.25. Same-ZIP proximity is known for the four verified venues.',
    missing: 'Measured journey times — no routing source was reachable (F-01).',
    how: 'Integrate a routing API (S1), or click the pre-built Google Maps transit links on the Hotels page.', link: 'hotels.html#clusters' },
  { id: 'Q-09', area: 'Activities', question: 'Which three or four paid attractions are actually wanted?',
    known: 'The Met is $30 per adult; Top of the Rock timed admission from $42; the 9/11 Memorial itself is free and open daily 8 AM–8 PM.',
    missing: 'MoMA, AMNH, Broadway and the High Line are unverified, and the 9/11 Museum ticket price was not captured (F-07, F-08, F-14).',
    how: 'Confirm the shortlist, then verify each one’s hours and price on its own site (S9).', link: 'activities.html' },
  { id: 'Q-10', area: 'Weather', question: 'What does mid-February weather do to the plan?',
    known: 'Nothing yet — no weather source was checked in this session.',
    missing: 'Typical February temperatures and precipitation, and which activities are weather-dependent.',
    how: 'Add a climate reference (e.g. National Weather Service climate normals) and tag each activity indoor/outdoor.', link: '' },
  { id: 'Q-11', area: 'Flights', question: 'What is the airfare and which airport?',
    known: 'Nothing — airfare was explicitly out of scope for this pass (F-12).',
    missing: 'Arrival airport (JFK/LGA/EWR), transfer cost, and whether the 15 Feb arrival is feasible on day one.',
    how: 'Price flights, then re-time day 1 (a long-haul arrival cannot support a 7 PM Atera seating).', link: '' },
  { id: 'Q-12', area: 'Accessibility', question: 'Any mobility, dietary or accessibility requirement we must filter on?',
    known: 'MICHELIN publishes facilities per restaurant (wheelchair access, vegetarian/vegan/halal/kosher options). Hotel room accessibility is listed per rate.',
    missing: 'Your requirements. One allergy can eliminate half the starred list.',
    how: 'State requirements; then filter using the MICHELIN “Services & Facilities” tags.', link: 'michelin.html' }
];

/* ---------- 12. FLAGGED FOR REVIEW --------------------------------------- */
window.FLAGGED = [
  { id: 'F-01', severity: 'High', item: 'Michelin travel times (the “1 hour or less” rule)',
    detail: 'The brief asks for hotels ranked by the number of MICHELIN restaurants within 1 hour by subway or bus. No transit-routing API or MTA trip planner was reachable from this environment, so no travel time is asserted anywhere on this site.',
    evidence: 'Only same-ZIP-code matches are claimed. Pre-built Google Maps transit links are provided so each pair can be checked in two clicks.',
    action: 'Implement S1, or click through the links and record durations manually.', link: 'hotels.html#clusters' },
  { id: 'F-02', severity: 'High', item: 'Incomplete MICHELIN index',
    detail: 'Official counters say 5 / 14 / 50 / 76 / 224. This site names all 5 three-star entries but only 3 of 14 two-star and 3 of 50 one-star. The official list pages paginate at 48 items per page and each detail page is ~5 screens of markup.',
    evidence: 'Counts come from the official distinction filter panel; the links are on the Michelin page.',
    action: 'Complete S3 before treating any cluster ranking as final.', link: 'michelin.html' },
  { id: 'F-03', severity: 'Medium', item: 'Le Bernardin Thursday–Sunday hours',
    detail: 'The official MICHELIN record was captured up to and including Thursday’s opening line before the page content changed. Thu–Sun service times are therefore not recorded here.',
    evidence: 'Friday, Saturday and Sunday rows exist on the source page but were not captured in the fetched text.',
    action: 'Re-read the MICHELIN record or le-bernardin.com and record all seven days (S9).', link: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/le-bernardin' },
  { id: 'F-04', severity: 'Medium', item: 'Arlo NoMad street address and ZIP',
    detail: 'The rate page and the official rooms page both loaded, but the postal address was not present in the captured text. Only neighbourhood-level location notes were captured.',
    evidence: 'Booking’s description places it ~1,056 ft from the Empire State Building and ~1,056 ft from the 6 train at 33rd & Park.',
    action: 'Read the official contact page; then a same-ZIP MICHELIN claim can be made or ruled out.', link: 'https://arlohotels.com/nomad/' },
  { id: 'F-05', severity: 'High', item: 'Social media links missing for 9 of 11 restaurants and all 4 activities',
    detail: 'The brief asks for a YouTube, TikTok or Instagram link per venue. Handles are only recorded where an official or booking-partner page printed them: Le Bernardin (IG + FB) and Eleven Madison Park (IG). Everything else is blank rather than guessed.',
    evidence: 'The Michelin record does not print social handles; the venues’ own sites are JavaScript-rendered and returned no link text.',
    action: 'Adopt S4’s acceptance rule and fill the cells from each venue’s own site.', link: 'michelin.html' },
  { id: 'F-06', severity: 'High', item: 'No per-person restaurant prices',
    detail: 'The “cost for 2 adults” column is empty for every starred restaurant. Michelin publishes only a $$$$ band; the restaurants’ menu pages are JavaScript-rendered (le-bernardin.com/menus returned a single image, elevenmadisonpark.com returned a slide carousel).',
    evidence: 'Resy confirms the $$$$ band for Le Bernardin but prints no per-person figure.',
    action: 'Capture menu prices in a browser session (S2).', link: 'michelin.html' },
  { id: 'F-07', severity: 'Medium', item: 'The Met and MoMA hours not captured',
    detail: 'The Met’s official visit page was read through all five chunks without the weekly hours block appearing. MoMA’s visit page failed to load twice.',
    evidence: 'Met ticket prices and address were captured; hours were not.',
    action: 'Re-read with JavaScript enabled; record all seven days plus holiday exceptions (Presidents’ Day falls in this window).', link: 'https://www.metmuseum.org/plan-your-visit' },
  { id: 'F-08', severity: 'Medium', item: '9/11 Memorial Museum ticket price',
    detail: 'The official page states opening hours and that advance purchase is required, but the adult ticket price was not in the captured text.',
    evidence: '“Advance ticket purchase” is confirmed; price is not.',
    action: 'Read the ticket page and record adult price; then complete the budget.', link: 'https://www.911memorial.org/visit/visit-museum-1' },
  { id: 'F-09', severity: 'Medium', item: 'Hotel prices are third-party and time-limited',
    detail: 'All four hotel prices are Booking.com rates read on 2026-11-25 for 15–22 Feb 2027, not rates from the hotels’ own booking engines. Arlo NoMad’s rate depended on a “Black Friday Deal” running 19 Nov–31 Dec 2026.',
    evidence: 'Each row links the exact rate URL used, including the 2027 dates.',
    action: 'Re-price on the hotels’ own sites before booking; treat the totals as a snapshot, not a quote.', link: 'hotels.html' },
  { id: 'F-10', severity: 'Low', item: 'Repository irregularities',
    detail: 'The repository arrived with a single 8-byte README containing “# NYFun2---” (a stray separator), no licence, no .gitignore, no CI, and no branch protection. GitHub Pages was already enabled and serving main / root.',
    evidence: 'See the Repo audit page for the exact commands and outputs.',
    action: 'Add README, licence, .gitignore and a Pages workflow; protect main if more sessions will push.', link: 'repo-audit.html' },
  { id: 'F-11', severity: 'Low', item: 'MICHELIN Keys hotels not evaluated',
    detail: 'MICHELIN also rates hotels (4 three-Key, 11 two-Key, 16 one-Key, 52 selected in NYC on 2026-11-25). None of the 83 were priced or compared, because that catalogue is a hotel-quality list, not a rate feed.',
    evidence: 'Counters read from guide.michelin.com/us/en/hotels-stays/nyc.',
    action: 'If a design-led stay matters more than price, price the four three-Key hotels next.', link: 'https://guide.michelin.com/us/en/hotels-stays/nyc' },
  { id: 'F-12', severity: 'High', item: 'Airfare not researched',
    detail: 'No flight pricing or airport-transfer cost appears anywhere in the budget. The date range is fixed but the door-to-door cost is not.',
    evidence: 'Budget table row marked unverified.',
    action: 'Price flights into JFK/LGA/EWR for 15 Feb 2027 and return 22 Feb 2027.', link: 'itinerary.html#budget' },
  { id: 'F-13', severity: 'Low', item: 'Only the 7-night length is costed',
    detail: 'The brief permits 1–2 weeks and possibly 2–4 weeks; no 14- or 28-night totals exist.',
    evidence: 'Every price column header says “7 nights”.',
    action: 'Decide length (Q-01) and re-price (S5/S10).', link: 'hotels.html' },
  { id: 'F-15', severity: 'Low', item: 'Street addresses for two activities not captured',
    detail: 'The official 9/11 Memorial page states hours and ticket rules but did not print a street address in the captured text, and the Top of the Rock ticket page did not print one either. Both addresses are therefore blank rather than recalled from memory.',
    evidence: 'Only The Met’s address (1000 Fifth Avenue, NY 10028) was printed on an official page read in this session.',
    action: 'Read the “getting here” / contact page for each venue and record the address.', link: 'activities.html' },
  { id: 'F-14', severity: 'Medium', item: 'No theatre / event ticketing verified',
    detail: 'No Broadway, concert or event source was checked, so no show is scheduled and no ticket cost is in the budget.',
    evidence: 'Activity backlog lists Broadway as unverified.',
    action: 'Pick a show and verify price and availability for the exact date.', link: 'activities.html' }
];

/* ---------- 13. SOURCES -------------------------------------------------- */
window.SOURCES = [
  { id: 'S-01', what: 'MICHELIN distinction counts for NYC (5 / 14 / 50 / 76 / 224)', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin', type: 'Official', read: '2026-11-25' },
  { id: 'S-02', what: 'All 5 three-star restaurants, names + cuisines + price band', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin', type: 'Official', read: '2026-11-25' },
  { id: 'S-03', what: 'Two-star list — Atera, Saga, Joo Ok named', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/2-stars-michelin', type: 'Official', read: '2026-11-25' },
  { id: 'S-04', what: 'One-star list — Le Coucou, Muku, Huso named', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin', type: 'Official', read: '2026-11-25' },
  { id: 'S-05', what: 'Le Bernardin — address, price band, Mon–Wed hours, phone, website', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/le-bernardin', type: 'Official', read: '2026-11-25' },
  { id: 'S-06', what: 'Eleven Madison Park — address, full weekly hours, phone, website', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/eleven-madison-park', type: 'Official', read: '2026-11-25' },
  { id: 'S-07', what: 'Per Se — address, daily hours, phone, website, Tock booking', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/per-se', type: 'Official', read: '2026-11-25' },
  { id: 'S-08', what: 'Atera — address, full weekly hours, phone, website', url: 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/atera', type: 'Official', read: '2026-11-25' },
  { id: 'S-09', what: 'MICHELIN hotel catalogue for NYC (83 hotels; 4 three-Key / 11 two-Key / 16 one-Key / 52 selected)', url: 'https://guide.michelin.com/us/en/hotels-stays/nyc', type: 'Official', read: '2026-11-25' },
  { id: 'S-10', what: 'Le Bernardin address, Instagram, Facebook, dress code, cancellation policy, $$$$ band', url: 'https://resy.com/cities/new-york-ny/venues/le-bernardin', type: 'Official booking partner', read: '2026-11-25' },
  { id: 'S-11', what: 'Eleven Madison Park address, Instagram, Facebook', url: 'https://resy.com/cities/new-york-ny/venues/eleven-madison-park', type: 'Official booking partner', read: '2026-11-25' },
  { id: 'S-12', what: 'Hyatt Place NY/Chelsea — rate for 15–22 Feb 2027, bed, attached bathroom, breakfast, cancellation', url: 'https://www.booking.com/hotel/us/hyatt-place-new-york-chelsea.en-us.html?checkin=2027-02-15&checkout=2027-02-22', type: 'Rate aggregator (snapshot)', read: '2026-11-25' },
  { id: 'S-13', what: 'Arlo NoMad — rate for 15–22 Feb 2027, Queen Room, resort fee, promo', url: 'https://www.booking.com/hotel/us/arlo-nomad.en-us.html?checkin=2027-02-15&checkout=2027-02-22', type: 'Rate aggregator (snapshot)', read: '2026-11-25' },
  { id: 'S-14', what: '11 Howard — rate for 15–22 Feb 2027, Queen Room, resort fee, cancellation', url: 'https://www.booking.com/hotel/us/11-howard.en-us.html?checkin=2027-02-15&checkout=2027-02-22', type: 'Rate aggregator (snapshot)', read: '2026-11-25' },
  { id: 'S-15', what: 'The Beekman — rate for 15–22 Feb 2027, King Room, private bathroom, taxes', url: 'https://www.booking.com/hotel/us/the-beekman-a-thompson-hotel.en-us.html?checkin=2027-02-15&checkout=2027-02-22', type: 'Rate aggregator (snapshot)', read: '2026-11-25' },
  { id: 'S-16', what: 'Arlo NoMad official room list — Queen / King / Bunk room types', url: 'https://arlohotels.com/nomad/rooms/', type: 'Official', read: '2026-11-25' },
  { id: 'S-17', what: 'Hyatt Place NY/Chelsea official address and parking/transport details', url: 'https://www.hyatt.com/hyatt-place/en-US/lgazc-hyatt-place-new-york-chelsea/hotel-info', type: 'Official', read: '2026-11-25 (via search result capture)' },
  { id: 'S-18', what: 'MTA subway and local bus fare: $3 per ride; express bus $7.25', url: 'https://www.mta.info/fares-tolls', type: 'Official', read: '2026-11-25' },
  { id: 'S-19', what: 'The Met — address, ticket table (adult $30), pay-what-you-wish rules, transit directions', url: 'https://www.metmuseum.org/plan-your-visit', type: 'Official', read: '2026-11-25' },
  { id: 'S-20', what: '9/11 Memorial (free, daily 8 AM–8 PM) and Museum (Wed–Mon + select Tue, 9–7, last entry 5:30)', url: 'https://www.911memorial.org/visit', type: 'Official', read: '2026-11-25' },
  { id: 'S-21', what: 'Top of the Rock — open 8 AM–12 AM, timed admission from $42, All-Inclusive from $82', url: 'https://www.rockefellercenter.com/tickets/top-of-the-rock-observation-deck/', type: 'Official', read: '2026-11-25' },
  { id: 'S-22', what: 'Booking.com New York search used to establish the market floor and rule out shared-bathroom inventory', url: 'https://www.booking.com/searchresults.en-us.html?ss=New+York&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&order=price&nflt=ht_id%3D204', type: 'Rate aggregator (snapshot)', read: '2026-11-25' }
];

/* ---------- 14. REPO AUDIT ----------------------------------------------- */
window.REPO_FINDINGS = [
  { id: 'R-01', severity: 'Medium', finding: 'Repository contained one 8-byte file: README.md holding “# NYFun2---”',
    detail: 'The trimmed content is a heading followed by three hyphens, which renders as a horizontal rule and an empty page. There was no project description, no data, no site, and no docs.',
    action: 'Replaced with a real README documenting scope, sources, method and how to publish.' },
  { id: 'R-02', severity: 'Medium', finding: 'No licence file',
    detail: 'A public repository with no licence grants no reuse rights, and it makes third-party reuse of the data legally ambiguous.',
    action: 'Add a licence (MIT for code, CC BY 4.0 for the data) and reference it from the README.' },
  { id: 'R-03', severity: 'Low', finding: 'No .gitignore',
    detail: 'Nothing prevents editor folders, OS files, node_modules or local caches from being committed later.',
    action: 'Added a minimal .gitignore.' },
  { id: 'R-04', severity: 'Low', finding: 'No CI / no build step / no link checking',
    detail: 'Pages publishes whatever is committed to main, so a broken relative link or a typo in the JS ships silently.',
    action: 'Add a workflow that runs a link check plus an HTML/JS syntax check on every push.' },
  { id: 'R-05', severity: 'Low', finding: 'Pages already enabled on main, root path',
    detail: 'Verified through the API: build_type legacy, source main /, public, https enforced, URL https://kanlerxz87-cyber.github.io/NYFun2/. That means the site must live at repository root, not in /docs, unless the Pages source is changed.',
    action: 'Site published at repository root so no Pages reconfiguration is needed.' },
  { id: 'R-06', severity: 'Info', finding: 'No branch protection and a single commit history',
    detail: 'One commit (“Initial commit”) on main. Nothing prevents concurrent sessions from force-pushing over each other.',
    action: 'Protect main and route work through pull requests (recorded in COORDINATION.md).' },
  { id: 'R-07', severity: 'Info', finding: 'COORDINATION.md did not exist',
    detail: 'The shared task board required by the brief was absent, so task ownership and file scopes were undefined.',
    action: 'Created COORDINATION.md with a task board, session registry, and claim/handoff rules.' }
];
