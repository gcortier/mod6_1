---
# MCD et MLP pour la base Flights

## 1. MCD (Modèle Conceptuel de Données)

### Entités et attributs principaux

**Carrier**
- code (`UNIQUE_CARRIER`)
- airline_id (`AIRLINE_ID`)

**State**
- abbr (`ORIGIN_STATE_ABR` / `DEST_STATE_ABR`)
- fips (`ORIGIN_STATE_FIPS` / `DEST_STATE_FIPS`)
- name (`ORIGIN_STATE_NM` / `DEST_STATE_NM`)

**Airport**
- code (`ORIGIN` / `DEST`)
- city_name (`ORIGIN_CITY_NAME` / `DEST_CITY_NAME`)
- wac (`ORIGIN_WAC` / `DEST_WAC`)

**TimeBlock**
- block (`DEP_TIME_BLK` / `ARR_TIME_BLK`)

**Flight**
- flight_date (`FL_DATE`)
- day_of_week (`DAY_OF_WEEK`)
- flight_number (`FL_NUM`)
- tail_num (`TAIL_NUM`)
- crs_dep_time, dep_time, dep_delay, dep_delay_new, dep_del15, dep_delay_group, taxi_out, wheels_off, wheels_on, taxi_in, crs_arr_time, arr_time, arr_delay, arr_delay_new, arr_del15, arr_delay_group, cancelled, cancellation_code, diverted, crs_elapsed_time, actual_elapsed_time, air_time

#### Associations
- Un **Flight** est opéré par un **Carrier**
- Un **Flight** part d’un **Airport** (origin) et arrive à un **Airport** (dest)
- Un **Airport** appartient à un **State** mais un **State** peut avoir plusieurs **Airport**.
- Un **Flight** a un créneau de départ (**TimeBlock**) et d’arrivée (**TimeBlock**)

---

## 2. MLD (Modèle Logique de Données)

### Tables et relations

**carrier**
- id (PK)
- code (unique, not null)
- airline_id (unique, not null)

**state**
- id (PK)
- abbr (unique, not null)
- fips
- name

**airport**
- id (PK)
- code (unique, not null)
- city_name
- wac
- state_id (FK → state.id)

**time_block**
- id (PK)
- block (unique, not null)

**flight**
- id (PK)
- flight_date (date, not null)
- day_of_week (smallint, not null)
- flight_number (int, not null)
- tail_num (varchar)
- carrier_id (FK → carrier.id, not null)
- origin_id (FK → airport.id, not null)
- dest_id (FK → airport.id, not null)
- dep_time_blk_id (FK → time_block.id)
- arr_time_blk_id (FK → time_block.id)
- crs_dep_time, dep_time, dep_delay, dep_delay_new, dep_del15, dep_delay_group, taxi_out, wheels_off, wheels_on, taxi_in, crs_arr_time, arr_time, arr_delay, arr_delay_new, arr_del15, arr_delay_group, cancelled, cancellation_code, diverted, crs_elapsed_time, actual_elapsed_time, air_time

### Contraintes
- Les clés étrangères assurent l’intégrité référentielle entre les tables.
- Les codes (`code`) sont uniques pour les tables de référence.
- Un aéroport appartient à un seul état, mais un état peut avoir plusieurs aéroports.
- Un vol référence toujours un transporteur, un aéroport de départ et d’arrivée.
