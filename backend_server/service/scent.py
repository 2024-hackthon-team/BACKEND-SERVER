import datetime as dt
from statistics import mean

from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.orm import Session

import backend_server.models.scent as scent_model
import backend_server.schemas.scent as scent_schema


def _convert_to_single_measurements(
    api_data: scent_schema.ScentApiCreate,
) -> list[scent_schema.ScentSingleMeasurement]:
    single_measurements = []
    for i in range(len(api_data.index)):
        single_measurement = scent_schema.ScentSingleMeasurement(
            index=api_data.index[i],
            temperature=api_data.temperature[i],
            humidity=api_data.humidity[i],
            pressure=api_data.pressure[i],
            gas_value=api_data.gas_value[i],
        )
        single_measurements.append(single_measurement)
    return single_measurements


def _get_gas_diff(
    measurement_list: list[scent_schema.ScentSingleMeasurement],
    offset=10,
):
    return [
        measurement_list[i + 1].gas_value
        - measurement_list[i].gas_value
        + offset
        for i in range(len(measurement_list) - 1)
    ]


def _align_measurement_list(
    measurement_list: list[scent_schema.ScentSingleMeasurement],
):
    """'scent'を整列し、最初の'scent'のindexを0にします"""
    for i, measurement in enumerate(measurement_list):
        if measurement.index == 0:
            return measurement_list[i:]

    return []


def create_scent(db: Session, obj_in: scent_schema.ScentDBCreate):
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = scent_model.Scent(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def convert_api_data_to_db_data(
    scent_data: scent_schema.ScentApiCreate,
    ndigits: int = 5,
):
    now_time = dt.datetime.now()
    meas_li = _convert_to_single_measurements(scent_data)
    meas_li = _align_measurement_list(meas_li)

    correct_index_set = set(range(10))
    meas_set_li: list[scent_schema.ScentDBCreate] = []

    # 10個のデータを1セットとして扱う
    while meas_li:
        one_set = sorted(meas_li[:10], key=lambda x: x.index)

        # 1セットに0~9のindexのデータがあるかどうか
        # ない場合は、このセットをスキップ
        if correct_index_set != (
            index_set := {meas.index for meas in one_set}
        ):
            logger.warning(
                f"Find missing index: {correct_index_set - index_set} at set:"
            )
            for i in one_set:
                logger.warning(i)

            meas_li.pop(0)
            meas_li = _align_measurement_list(meas_li)
            continue

        meas_set_li.append(
            scent_schema.ScentDBCreate(
                sensored_at=now_time,
                temperature=mean([i.temperature for i in one_set]),
                humidity=mean([i.humidity for i in one_set]),
                pressure=mean([i.pressure for i in one_set]),
                gas_feature=[
                    *[i.gas_value for i in one_set],
                    *_get_gas_diff(one_set),
                ],
            )
        )

        # TODO: filter out all
        meas_li = meas_li[10:]

    if not meas_set_li:
        return None

    # すべてのセットの平均を取る
    db_in = scent_schema.ScentDBCreate(
        sensored_at=now_time,
        temperature=round(mean([i.temperature for i in meas_set_li]), ndigits),
        humidity=round(mean([i.humidity for i in meas_set_li]), ndigits),
        pressure=round(mean([i.pressure for i in meas_set_li]), ndigits),
        # i.gas_feature is a 13-dim vector
        # take average of each dimension
        gas_feature=[
            round(mean(j), ndigits)
            for j in zip(*[i.gas_feature for i in meas_set_li])
        ],
    )
    logger.debug(db_in.model_dump_json(indent=2))

    return db_in
