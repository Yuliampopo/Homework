from dataclasses import dataclass


@dataclass(order=True)
class Date:
    year: int
    month: int
    day: int


@dataclass(order=True)
class DateRange:
    begin_date: Date
    end_date: Date


def get_ranges_wo_insurance(insurance_periods: list[DateRange]) -> list[DateRange]:
    periods = insurance_periods.copy()
    result = []
    while len(periods) > 1:
        first_period = min(periods)
        periods.remove(first_period)
        second_period = min(periods)
        if first_period.end_date > second_period.begin_date:
            second_period.begin_date = first_period.begin_date
            second_period.end_date = max(first_period.end_date, second_period.end_date)
        else:
            result.append(DateRange(first_period.end_date, second_period.begin_date))
    return result


if __name__ == '__main__':
    _insurances = [
        DateRange(Date(2020, 1, 1), Date(2020, 6, 25)),
        DateRange(Date(2020, 7, 1), Date(2020, 8, 31)),
        DateRange(Date(2020, 6, 29), Date(2020, 7, 31)),
        DateRange(Date(2020, 10, 1), Date(2020, 12, 31)),
    ]
    assert get_ranges_wo_insurance(_insurances) == [
        DateRange(Date(2020, 6, 25), Date(2020, 6, 29)),
        DateRange(Date(2020, 8, 31), Date(2020, 10, 1)),
    ]

    assert get_ranges_wo_insurance([]) == []

    _insurances = [
        DateRange(Date(2020, 1, 1), Date(2020, 7, 15)),
        DateRange(Date(2020, 7, 1), Date(2020, 12, 31)),
    ]
    assert get_ranges_wo_insurance(_insurances) == []
