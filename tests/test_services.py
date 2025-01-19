import pytest
from unittest.mock import patch
from src.services import calculate_deposit_logic

@pytest.mark.parametrize(
    "date_str, periods, amount, rate, expected",
    [
        ("31.01.2021", 3, 10000, 6.0, {
            "31.01.2021": 10050.0,
            "28.02.2021": 10100.25,
            "31.03.2021": 10150.75,
        }),
        ("15.02.2021", 2, 20000, 5.0, {
            "15.02.2021": 20000.0,  # тут не последний день месяца
            "15.03.2021": 20083.33, # пример
        })
    ]
)
def test_calculate_deposit_logic(date_str, periods, amount, rate, expected):
    result = calculate_deposit_logic(date_str, periods, amount, rate)
    assert result == pytest.approx(expected, 0.01)


@pytest.mark.asyncio
async def test_calculate_and_store():
    with patch("src.services.database.execute") as mock_execute:
        results = await calculate_and_store("31.01.2021", 3, 10000, 6.0)

        expected = {
            "31.01.2021": 10050.0,
            "28.02.2021": 10100.25,
            "31.03.2021": 10150.75,
        }
        assert results == pytest.approx(expected, 0.01)

        mock_execute.assert_called_once()



