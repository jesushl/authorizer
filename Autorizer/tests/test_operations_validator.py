from unittest import TestCase
import json
# Models
# Validators 
from operations_validator import OperationsValidator


class TestOperationsValidator(TestCase):
    def setUp(self) -> None:
        self.operation_example_1 = json.load(
            open('tests/text_examples/test_example_input_1.txt')
        )

    def test_validate_operation(self):
        operations_validator = OperationsValidator()
        op_1 = self.operation_example_1[0]
        operations_validator.validate_operation(op_1)
        logs = operations_validator.actions_log
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 100}, "violations": []}',
            str(logs[0])
        )
       
    def test_validate_operations(self):
        operations_validator = OperationsValidator()
        operations_validator.validate_operations(operations=self.operation_example_1)
        logs = operations_validator.actions_log
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 100}, "violations": []}',
            str(logs[0])
        )
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 80}, "violations": []}',
            str(logs[1])
        )
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 80}, "violations": ["insufficient-limit"]}',
            str(logs[2])
        )
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 50}, "violations": []}',
            str(logs[3])
        )
        # testing case 2 about acccount already initialized
        operation_example_2 = json.load(
            open('tests/text_examples/test_example_input_2.txt')
        )
        operations_validator_2 = OperationsValidator()
        operations_validator_2.validate_operations(operations=operation_example_2)
        logs = operations_validator_2.actions_log
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 175}, "violations": []}',
            str(logs[0])
        )
        self.assertEqual(
            '{"account": {"active-card": true, "available-limit": 175}, "violations": ["account-already-initialized"]}',
            str(logs[1])
        )

    def test_validate_card_not_active(self):
        operation_example = json.load(
            open('tests/text_examples/test_example_input_3.txt')
        )
        operations_validator = OperationsValidator()
        operations_validator.validate_operations(operations=operation_example)
        logs = operations_validator.actions_log
        self.assertEqual(
            '{"account": {"active-card": false, "available-limit": 100}, "violations": []}',
            str(logs[0])
        )
        self.assertEqual(
            '{"account": {"active-card": false, "available-limit": 100}, "violations": ["card-not-active"]}',
            str(logs[1])
        )
        self.assertEqual(
            '{"account": {"active-card": false, "available-limit": 100}, "violations": ["card-not-active"]}',
            str(logs[2])
        )
