#!/usr/bin/env python3
"""Generates the workshop dataset. Deterministic: same seed, same numbers, always."""
import csv, json, random, os
from datetime import date, timedelta

random.seed(20260902)
OUT = "/home/claude/data"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- geography
GEO = {
    "Kenya": ["Kakamega", "Bungoma", "Trans Nzoia", "Siaya"],
    "Rwanda": ["Musanze", "Nyagatare", "Huye"],
    "Uganda": ["Mbale", "Kapchorwa", "Tororo"],
}
SITE_WORDS = ["Mukuyu","Nzoia","Chebukwa","Lusala","Kimilili","Namwela","Bukembe","Sirisia",
    "Rugeshi","Kinigi","Gataraga","Rwimbogo","Karama","Mukura","Cyanika","Busiu","Bufumbo",
    "Nakaloke","Kaserem","Sipi","Kamu","Malaba","Mulanda","Nagongera","Ikoba","Shitoli",
    "Namanjalala","Kwanza","Endebess","Sango","Buyofu","Tande","Wamono","Kibisi","Naboa",
    "Kisoko","Rubaya","Gitovu","Bunambutye","Chema"]

FIRST = ["Achieng","Wafula","Nekesa","Barasa","Chelimo","Wanjiru","Odhiambo","Nafula","Kiptoo",
    "Auma","Simiyu","Naliaka","Cheruiyot","Adhiambo","Masika","Wekesa","Jepkosgei","Otieno",
    "Nanjala","Kipruto","Uwase","Mukamana","Habimana","Uwimana","Niyonzima","Mutesi","Ndayisenga",
    "Nakato","Wasswa","Nabirye","Okello","Amongi","Wanyama","Kirabo","Musimenta","Atieno",
    "Were","Nasimiyu","Chepkoech","Mugisha","Ingabire","Twagirayezu","Namusoke","Ojok"]
LAST = ["Omondi","Wanyonyi","Barasa","Wekesa","Simiyu","Juma","Kiplagat","Otieno","Namunyu",
    "Makokha","Sifuna","Wafula","Chemutai","Rotich","Mutai","Uwimana","Nsengimana","Bizimana",
    "Mukamurenzi","Hakizimana","Ntawukuriryayo","Kagabo","Okello","Wanyama","Nabukenya","Owor",
    "Kirya","Masaba","Cherop","Watulo","Nandwa","Situma","Khaemba","Wangila","Namulundu"]

GROUP_SUFFIX = ["Farmers Group","Cooperative","Self Help Group","Growers","Union","Collective"]
GROUP_NAME = ["Tumaini","Amani","Bidii","Umoja","Imani","Jitegemee","Mavuno","Neema","Baraka",
    "Ushirika","Twiyubake","Duterimbere","Abadahigwa","Icyerekezo","Terimbere","Kwetu","Mwangaza",
    "Juhudi","Maendeleo","Shirikisho","Nguvu","Chapa Kazi","Vumilia","Faraja","Riziki","Subira"]

# ---------------------------------------------------------------- products
PRODUCTS = [
    ("P-01", "Hybrid maize seed 2kg",      "Seed",      45000),
    ("P-02", "Hybrid maize seed 10kg",     "Seed",     210000),
    ("P-03", "Bean seed 5kg",              "Seed",      62000),
    ("P-04", "DAP fertiliser 50kg",        "Fertiliser",625000),
    ("P-05", "CAN fertiliser 50kg",        "Fertiliser",520000),
    ("P-06", "NPK fertiliser 25kg",        "Fertiliser",341000),
    ("P-07", "Solar home light",           "Solar",     280000),
    ("P-08", "Grevillea seedlings x20",    "Trees",      36000),
    ("P-09", "Storage bags x5",            "Storage",    47500),
    ("P-10", "Vegetable seed pack",        "Seed",       28000),
]

SEASONS = [
    ("2025A", date(2025, 1, 15), date(2025, 9, 30)),
    ("2025B", date(2025, 7,  1), date(2026, 2, 28)),
    ("2026A", date(2026, 1, 12), date(2026, 9, 30)),
]

CHANNELS = ["Mobile money", "Mobile money", "Mobile money", "Bank deposit", "Cash at site"]

# archetypes: (label, weight, repayment range)
ARCHETYPES = [
    ("strong",     30, (0.96, 1.00)),
    ("steady",     34, (0.82, 0.97)),
    ("mixed",      21, (0.55, 0.85)),
    ("struggling", 11, (0.25, 0.60)),
    ("distressed",  4, (0.02, 0.30)),
]

sites, groups, farmers, orders, items, payments = [], [], [], [], [], []
sid = gid = fid = oid = iid = pid = 0
word_pool = SITE_WORDS[:]
random.shuffle(word_pool)
wi = 0

for country, districts in GEO.items():
    cc = {"Kenya": "KE", "Rwanda": "RW", "Uganda": "UG"}[country]
    for district in districts:
        for _ in range(random.randint(3, 5)):
            sid += 1
            name = word_pool[wi % len(word_pool)]; wi += 1
            site_id = f"S-{sid:03d}"
            sites.append({"site_id": site_id, "site_name": name, "district": district,
                          "country": country, "country_code": cc})

            for _ in range(random.randint(4, 8)):
                gid += 1
                group_id = f"G-{gid:04d}"
                gname = f"{random.choice(GROUP_NAME)} {random.choice(GROUP_SUFFIX)}"
                arche = random.choices([a[0] for a in ARCHETYPES],
                                       weights=[a[1] for a in ARCHETYPES])[0]
                lo, hi = next(a[2] for a in ARCHETYPES if a[0] == arche)
                groups.append({"group_id": group_id, "group_name": gname, "site_id": site_id,
                               "formed_date": (date(2023,1,1) + timedelta(days=random.randint(0,900))).isoformat()})

                for _ in range(random.randint(6, 14)):
                    fid += 1
                    farmer_id = f"F-{fid:05d}"
                    farmers.append({
                        "farmer_id": farmer_id,
                        "farmer_name": f"{random.choice(FIRST)} {random.choice(LAST)}",
                        "phone": f"+254{random.randint(700000000, 799999999)}" if cc == "KE"
                                 else (f"+250{random.randint(780000000, 789999999)}" if cc == "RW"
                                       else f"+256{random.randint(700000000, 789999999)}"),
                        "group_id": group_id,
                        "enrolled_date": (date(2023,3,1) + timedelta(days=random.randint(0,850))).isoformat(),
                    })

                    # each farmer takes 1-3 seasonal packages
                    for season, start, deadline in random.sample(SEASONS, random.randint(1, 3)):
                        oid += 1
                        order_id = f"O-{oid:05d}"
                        order_date = start + timedelta(days=random.randint(0, 40))
                        principal = 0
                        for prod in random.sample(PRODUCTS, random.randint(2, 5)):
                            iid += 1
                            qty = random.randint(1, 3)
                            line = prod[3] * qty
                            principal += line
                            items.append({"order_item_id": f"I-{iid:06d}", "order_id": order_id,
                                          "product_id": prod[0], "quantity": qty,
                                          "unit_price_cents": prod[3], "line_total_cents": line})
                        fee = round(principal * 0.12)
                        total = principal + fee
                        orders.append({"order_id": order_id, "farmer_id": farmer_id,
                                       "season": season, "order_date": order_date.isoformat(),
                                       "deadline": deadline.isoformat(),
                                       "principal_cents": principal, "service_fee_cents": fee,
                                       "total_due_cents": total})

                        # repayment behaviour, dispersed within the group archetype
                        target = min(1.05, max(0.0, random.uniform(lo, hi) + random.gauss(0, 0.07)))
                        remaining = round(total * target)
                        n = 0 if remaining == 0 else random.randint(2, 7)
                        window = (deadline - order_date).days
                        for k in range(n):
                            pid += 1
                            amt = remaining if k == n - 1 else round(remaining / (n - k) * random.uniform(0.6, 1.4))
                            amt = max(0, min(amt, remaining))
                            remaining -= amt
                            if amt == 0:
                                continue
                            day = order_date + timedelta(days=max(1, int(window * ((k + 1) / n) * random.uniform(0.5, 1.15))))
                            payments.append({"payment_id": f"PM-{pid:06d}", "order_id": order_id,
                                             "payment_date": day.isoformat(), "amount_cents": amt,
                                             "channel": random.choice(CHANNELS)})

def write(name, rows, cols):
    with open(f"{OUT}/{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

write("sites", sites, ["site_id","site_name","district","country","country_code"])
write("groups", groups, ["group_id","group_name","site_id","formed_date"])
write("farmers", farmers, ["farmer_id","farmer_name","phone","group_id","enrolled_date"])
write("products", [{"product_id":p[0],"product_name":p[1],"category":p[2],"unit_price_cents":p[3]} for p in PRODUCTS],
      ["product_id","product_name","category","unit_price_cents"])
write("orders", orders, ["order_id","farmer_id","season","order_date","deadline",
                         "principal_cents","service_fee_cents","total_due_cents"])
write("order_items", items, ["order_item_id","order_id","product_id","quantity","unit_price_cents","line_total_cents"])
write("payments", payments, ["payment_id","order_id","payment_date","amount_cents","channel"])

due = sum(o["total_due_cents"] for o in orders)
paid = sum(p["amount_cents"] for p in payments)
print(f"sites {len(sites)}  groups {len(groups)}  farmers {len(farmers)}")
print(f"orders {len(orders)}  items {len(items)}  payments {len(payments)}")
print(f"due {due/100:,.0f}  paid {paid/100:,.0f}  portfolio rate {paid/due:.4f}")
