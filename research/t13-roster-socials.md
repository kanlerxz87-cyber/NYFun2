# T13 — Live MICHELIN all-starred roster re-verification (session fc6d5f66, 2026-11-25)

Source: https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred (pages 1–2, fetched 2026-11-25)
Official filter counters: 5 × 3-star, 14 × 2-star, 50 × 1-star = 69 starred; 76 Bib Gourmand; 224 Selected.

## Complete live roster (69), transcribed from the two list pages
3★ (5): Sushi Sho, Jungsik New York, Eleven Madison Park, Le Bernardin, Per Se
2★ (14): Atera, Saga, Joo Ok, César, Odo, Chef's Table at Brooklyn Fare, Atomix, Aska (Brooklyn), Aquavit, Jean-Georges, Gabriel Kreuther, Masa, Sushi Noz, The Modern
1★ (50): Le Coucou, Muku, Huso, Yamada, Bridges, Corima, Jua, Frevo, Torien, Tempura Matsui, Estela, Sushi Nakazawa New York, Noda, Jeju Noodle Bar, Semma, Yoshino, Cote, Crown Shy, Shmoné, Gramercy Tavern, Oiji Mi, Family Meal at Blue Hill, Dirt Candy, Tuome, Bar Miller, bōm, Noz 17, Torrisi, Casa Mono, Kosaka, Sixty Three Clinton, Nōksu, Icca, L'Abeille, Tsukimi, Rezdôra, Francie (Brooklyn), Oxomoco (Brooklyn), The Four Horsemen (Brooklyn), Shota Omakase (Brooklyn), Restaurant Yuu (Brooklyn), Le Pavillon, Kochi, Café Boulud at Maison Barnes, Jōji, YingTao, Daniel, Essential by Christophe, Mari, Meju (Queens)

## Irregularity found (flag for review)
The namespaced kit `sessions/33cfdba4/data/restaurants.json` carries 72 rows but the live all-starred list has 69.
Three kit rows are NOT in the live starred selection (likely 2025-article carryovers):
- Blue Hill at Stone Barns (kit: 2★)
- Shion 69 Leonard Street (kit: 1★)
- La Bastide by Andrea Calstier (kit: 1★)
Their current distinction is unverified; they are excluded from the canonical starred roster and flagged.

## Michelin detail pages fetched this session (address/hours/website/price band)
- Cote: 16 W. 22nd St 10010; Korean, Steakhouse; $$$$; Mon–Wed 17–23, Thu–Sat 17–24, Sun 17–23; cotekoreansteakhouse.com; Resy.
- Aska: 47 S. 5th St, Brooklyn 11249; Scandinavian, Contemporary; $$$$; Mon closed, Tue–Fri 17–23 (Sat/Sun cut off in capture — re-check); askanyc.com; own bookings.
- César: 333 Hudson St 10013; Contemporary, Fish and Seafood; $$$$; Mon–Fri 18–23, Sat–Sun 17:30–23; cesar.restaurant; Tock.
- Chef's Table at Brooklyn Fare: 431 W. 37th St 10018; Contemporary; $$$$; Mon closed, Tue–Thu 18–23, Fri–Sun 17–23; brooklynfare.com/chefs-table; Resy.
- Joo Ok: 22 W. 32nd St, 16th Fl 10001; Korean, Contemporary; $$$$; Mon–Sat 17:30–23:30, Sun closed; joo-ok.com; Resy.
- Masa: 10 Columbus Circle Ste 401, 10019; Japanese, Sushi; $$$$; Mon & Sun closed, Tue–Sat 12–14:30 & 17:30–22; masanyc.com; Tock.
- Odo: 17 W. 20th St 10011; Japanese, Contemporary; $$$$; odo.nyc; Tock (hours below the fold — re-check).
- Saga: 70 Pine St 10005; Contemporary; $$$$; daily 17–21:30; saga-nyc.com; Resy.
- Sushi Noz: 181 E. 78th St 10075; Japanese, Sushi; $$$$; Mon–Sat 17:45–23, Sun closed; sushinoz.com; OpenTable.
- The Modern: 9 W. 53rd St 10019; Contemporary; $$$$; Mon–Thu & Sun 12–14:30 & 17–21, Fri–Sat 12–14:30 & 17–21:30; themodernnyc.com; OpenTable. RESOLVES canonical "hours unverified" flag.

## Official menu prices verified (T10)
- Eleven Madison Park (official FAQ https://www.elevenmadisonpark.com/faq): Full Tasting $385/guest → $770 for 2; Bar Tasting $255/guest → $510 for 2. Wine pairing from $125/guest. Gratuity NOT included. No dress code. Reservations open 1st of month for following month; all sales final/non-refundable.
- Le Bernardin (official accessible menus): Chef's Tasting $350/person ($530 with wine pairing) → $700 / $1,060 for 2; Dinner prix fixe $225 (4 courses) → $450 for 2; Lunch prix fixe $142 (3 courses) → $284 for 2. Supplements extra (caviar $145/oz etc.).
- Per Se (official Tock channel https://www.exploretock.com/perse/experience/288603/main-dining-room-tasting-menu): Main Dining Room tasting $425/person (per Tock experience description) → $850 for 2; $200/person deposit. Salon four-course $150/person deposit. Official socials printed on Tock: facebook.com/perse, instagram.com/perseny, twitter.com/PerSeNY.
