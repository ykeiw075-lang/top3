import os
import sys
import tempfile
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from main import read_participants, validate_participants, split_bill


class TestSplitBill(unittest.TestCase):
    def test_equal_participants(self):
        participants = [("Аня", 1), ("Борис", 1), ("Вера", 1)]
        result = split_bill(100, participants)
        self.assertEqual(result, {"Аня": 34, "Борис": 33, "Вера": 33})
        self.assertEqual(sum(result.values()), 100)

    def test_empty_participants(self):
        with self.assertRaises(ValueError):
            split_bill(100, [])

    def test_one_participant(self):
        result = split_bill(100, [("Аня", 1)])
        self.assertEqual(result, {"Аня": 100})

    def test_exact_boundary(self):
        participants = [("Аня", 1), ("Борис", 1), ("Вера", 1)]
        result = split_bill(100, participants)
        self.assertEqual(sum(result.values()), 100)

    def test_zero_weight(self):
        with self.assertRaises(ValueError):
            validate_participants([(1, "Аня", "0")])

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            validate_participants([(1, "Аня", "abc")])

    def test_read_valid_csv(self):
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="", delete=False
        ) as file:
            file.write("Аня;1\nБорис;1\nВера;1\n")
            path = file.name

        try:
            rows = read_participants(path)
            participants = validate_participants(rows)
            self.assertEqual(len(participants), 3)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
