# Hotels verification (T14) — 2026-11-25

Spot-checks against official hotel / brand pages and booking engines (Booking.com snapshots are clearly labelled).

## Verified facts

| Hotel | Verified facts | Source |
|---|---|---|
| Hyatt Place New York / Chelsea | Address **140 West 24th Street, NY 10011**; 4.0/5 (1,425 reviews, hyatt.com); "Excellent location – rated 9.2/10!" Booking.com, Feb 15–22 2027 snapshot | https://www.hyatt.com/hyatt-place/en-US/lgazc-hyatt-place-new-york-chelsea/hotel-info (address); https://www.booking.com/hotel/us/hyatt-place-new-york-chelsea.en-us.html?checkin=2027-02-15&checkout=2027-02-22 (price snapshot, captured 2026-11-25; listed in data as $1,113 pre-tax / $1,305 all-in — aggregator basis) |
| Arlo NoMad | Rooms: Essential King, Terrace Queen, Queen City, Accessible City Queen, Twin Bunk (definitely queen-bed options); "Boutique Hotel in the Flatiron District" | https://arlohotels.com/nomad/rooms/ |

## Documented (not changed)
- citizenM New York Times Square: room spec "XL king bed; room designed for up to two adults; power shower" from the brand page (Marriott/citizenM). The official citizenM hotel page returned HTTP 500 from the sandbox; the room spec in data/hotels.json stands as published, per policy.
- 11 Howard, The Beekman, The Fifth Avenue Hotel, others: address/room/bath/rate kept as blanks with flags; unverified per policy.

## Irregularities
- Arlo NoMad rate depends on a "Black Friday Deal" (39% off) valid 19 Nov 2026 → 31 Dec 2027; the listed $1,213.96 pre-tax / $1,428 all-in was the deal rate when captured (flag in data).
- 11 Howard: guest score differs between hotel (18) and restaurant pages (18.1) — logged in data/hotels.json.
