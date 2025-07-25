import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from modules.connect_and_query import get_session
from flights.data.models import Carrier, Airport, State, TimeBlock, Flight

PARQUET_PATH = "./flights/data/processed/all_from_subject.parquet"
BATCH_START = 0
BATCH_END = 100_000

def get_or_create(session: Session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        instance = session.query(model).filter_by(**kwargs).first()
    return instance

def safe_float(val):
    try:
        if pd.isnull(val) or val == '':
            return None
        return float(val)
    except (ValueError, TypeError):
        return None

def main():
    cols = [
        # Variables temporelles
        "DAY_OF_WEEK", "FL_DATE",
        # Informations sur le vol
        "UNIQUE_CARRIER", "AIRLINE_ID", "FL_NUM", "TAIL_NUM",
        # Aéroport d'origine
        "ORIGIN", "ORIGIN_CITY_NAME", "ORIGIN_STATE_ABR", "ORIGIN_STATE_FIPS", "ORIGIN_STATE_NM", "ORIGIN_WAC",
        # Aéroport de destination
        "DEST", "DEST_CITY_NAME", "DEST_STATE_ABR", "DEST_STATE_FIPS", "DEST_STATE_NM", "DEST_WAC",
        # Horaires et retards
        "CRS_DEP_TIME", "DEP_TIME", "DEP_DELAY", "DEP_DELAY_NEW", "DEP_DEL15", "DEP_DELAY_GROUP",
        "DEP_TIME_BLK", "TAXI_OUT", "WHEELS_OFF", "WHEELS_ON", "TAXI_IN",
        "CRS_ARR_TIME", "ARR_TIME", "ARR_DELAY", "ARR_DELAY_NEW", "ARR_DEL15", "ARR_DELAY_GROUP",
        "ARR_TIME_BLK",
        # Annulations et détournements
        "CANCELLED", "CANCELLATION_CODE", "DIVERTED",
        # Durées et distances
        "CRS_ELAPSED_TIME", "ACTUAL_ELAPSED_TIME", "AIR_TIME"
    ]

    df = pd.read_parquet(PARQUET_PATH, columns=cols)
    df = df.iloc[BATCH_START:BATCH_END]

    session = get_session()


    for _, row in df.iterrows():
        # State ORIGIN
        origin_state = get_or_create(
            session, State,
            abbr=row["ORIGIN_STATE_ABR"] if pd.notnull(row["ORIGIN_STATE_ABR"]) else None,
            fips=row["ORIGIN_STATE_FIPS"] if pd.notnull(row["ORIGIN_STATE_FIPS"]) else None,
            name=row["ORIGIN_STATE_NM"] if pd.notnull(row["ORIGIN_STATE_NM"]) else None
        ) if pd.notnull(row["ORIGIN_STATE_ABR"]) else None
        # State DEST
        dest_state = get_or_create(
            session, State,
            abbr=row["DEST_STATE_ABR"] if pd.notnull(row["DEST_STATE_ABR"]) else None,
            fips=row["DEST_STATE_FIPS"] if pd.notnull(row["DEST_STATE_FIPS"]) else None,
            name=row["DEST_STATE_NM"] if pd.notnull(row["DEST_STATE_NM"]) else None
        ) if pd.notnull(row["DEST_STATE_ABR"]) else None

        # Airport ORIGIN
        origin = get_or_create(
            session, Airport,
            code=row["ORIGIN"],
            city_name=row["ORIGIN_CITY_NAME"] if pd.notnull(row["ORIGIN_CITY_NAME"]) else None,
            wac=int(row["ORIGIN_WAC"]) if pd.notnull(row["ORIGIN_WAC"]) else None,
            state_id=origin_state.id if origin_state else None
        )
        # Airport DEST
        dest = get_or_create(
            session, Airport,
            code=row["DEST"],
            city_name=row["DEST_CITY_NAME"] if pd.notnull(row["DEST_CITY_NAME"]) else None,
            wac=int(row["DEST_WAC"]) if pd.notnull(row["DEST_WAC"]) else None,
            state_id=dest_state.id if dest_state else None
        )

        carrier = get_or_create(session, Carrier, code=row["UNIQUE_CARRIER"], airline_id=row["AIRLINE_ID"])
        dep_time_blk = get_or_create(session, TimeBlock, block=row["DEP_TIME_BLK"]) if pd.notnull(row["DEP_TIME_BLK"]) else None
        arr_time_blk = get_or_create(session, TimeBlock, block=row["ARR_TIME_BLK"]) if pd.notnull(row["ARR_TIME_BLK"]) else None

        flight = Flight(
            flight_date = row["FL_DATE"] if isinstance(row["FL_DATE"], datetime) else pd.to_datetime(row["FL_DATE"]).date(),
            day_of_week = int(row["DAY_OF_WEEK"]),
            flight_number = int(row["FL_NUM"]),
            tail_num = str(row["TAIL_NUM"]) if pd.notnull(row["TAIL_NUM"]) else None,
            carrier_id = carrier.id,
            origin_id = origin.id,
            dest_id = dest.id,
            dep_time_blk_id = dep_time_blk.id if dep_time_blk else None,
            arr_time_blk_id = arr_time_blk.id if arr_time_blk else None,
            crs_dep_time = str(row["CRS_DEP_TIME"]) if pd.notnull(row["CRS_DEP_TIME"]) else None,
            dep_time = str(row["DEP_TIME"]) if pd.notnull(row["DEP_TIME"]) else None,
            dep_delay = safe_float(row["DEP_DELAY"]),
            dep_delay_new = safe_float(row["DEP_DELAY_NEW"]),
            dep_del15 = bool(row["DEP_DEL15"]) if pd.notnull(row["DEP_DEL15"]) else None,
            dep_delay_group = int(row["DEP_DELAY_GROUP"]) if pd.notnull(row["DEP_DELAY_GROUP"]) else None,
            taxi_out = safe_float(row["TAXI_OUT"]),
            wheels_off = str(row["WHEELS_OFF"]) if pd.notnull(row["WHEELS_OFF"]) else None,
            wheels_on = str(row["WHEELS_ON"]) if pd.notnull(row["WHEELS_ON"]) else None,
            taxi_in = safe_float(row["TAXI_IN"]),
            crs_arr_time = str(row["CRS_ARR_TIME"]) if pd.notnull(row["CRS_ARR_TIME"]) else None,
            arr_time = str(row["ARR_TIME"]) if pd.notnull(row["ARR_TIME"]) else None,
            arr_delay = safe_float(row["ARR_DELAY"]),
            arr_delay_new = safe_float(row["ARR_DELAY_NEW"]),
            arr_del15 = bool(row["ARR_DEL15"]) if pd.notnull(row["ARR_DEL15"]) else None,
            arr_delay_group = int(row["ARR_DELAY_GROUP"]) if pd.notnull(row["ARR_DELAY_GROUP"]) else None,
            cancelled = bool(row["CANCELLED"]) if pd.notnull(row["CANCELLED"]) else None,
            cancellation_code = str(row["CANCELLATION_CODE"]) if pd.notnull(row["CANCELLATION_CODE"]) else None,
            diverted = bool(row["DIVERTED"]) if pd.notnull(row["DIVERTED"]) else None,
            crs_elapsed_time = safe_float(row["CRS_ELAPSED_TIME"]),
            actual_elapsed_time = safe_float(row["ACTUAL_ELAPSED_TIME"]),
            air_time = safe_float(row["AIR_TIME"])
        )
        session.add(flight)

    session.commit()
    session.close()
    print(f"{BATCH_END - BATCH_START} lignes insérées.")



def clean_table():
    """
    Nettoie la table Flight en supprimant les entrées avec des valeurs manquantes critiques.
    """
    session = get_session()

    # Supprimer d'abord les tables dépendantes 
    session.query(Flight).delete()
    session.query(Airport).delete()
    session.query(State).delete()
    session.query(Carrier).delete()
    session.query(TimeBlock).delete()

    session.commit()
    session.close()
    print("Toutes les tables ont été vidées.")


if __name__ == "__main__":
    # clean_table()
    main()
