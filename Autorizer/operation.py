import argparse
import json
from operations_validator import OperationsValidator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transaction Validator')
    parser.add_argument('operations')
    operations = parser.parse_args().operations
    operations = operations.split('\n')
    operations_validator = OperationsValidator()
    op_in_dic = []
    for operation in operations:
        op_in_dic.append(json.loads(operation))
    operations_validator.validate_operations(op_in_dic)
    logs = operations_validator.actions_log
    for log in logs:
        print(log)
