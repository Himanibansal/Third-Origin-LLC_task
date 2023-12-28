import json
from typing import List, Optional, Union, Dict, Any


class JsonValidator:
    def validate_schema(self, json_file: str, schema_file: str) -> bool:
        try:
            # Load JSON and schema files
            with open(json_file, 'r') as json_file_handle:
                json_data = json.load(json_file_handle)

            with open(schema_file, 'r') as schema_file_handle:
                schema = json.load(schema_file_handle)

            # Validate JSON against the schema
            self._validate_required_fields(json_data, schema)
            self._validate_at_least_one_of(json_data, schema)
            self._validate_either_one_or_another(json_data, schema)
            self._validate_mutually_exclusive_fields(json_data, schema)
            self._validate_field_values(json_data, schema)

            return True  # If all validations pass

        except Exception as e:
            print(f"Validation failed: {str(e)}")
            return False

    def _validate_required_fields(self, json_data: dict, schema: dict) -> None:
        required_fields = schema.get('required_fields', [])
        for field in required_fields:
            if field not in json_data:
                raise ValueError(f"Required field '{field}' is missing in the JSON data.")

    def _validate_at_least_one_of(self, json_data: dict, schema: dict) -> None:
        at_least_one_of = schema.get('at_least_one_of', [])
        if not any(field in json_data for field in at_least_one_of):
            raise ValueError(f"At least one of {at_least_one_of} must be present in the JSON data.")

    def _validate_either_one_or_another(self, json_data: dict, schema: dict) -> None:
        either_one_or_another = schema.get('either_one_or_another', {})
        field1, field2 = either_one_or_another.get('field1'), either_one_or_another.get('field2')

        if field1 in json_data and field2 in json_data:
            raise ValueError(f"Either '{field1}' or '{field2}' should be present, not both.")

    def _validate_mutually_exclusive_fields(self, json_data: dict, schema: dict) -> None:
        mutually_exclusive_fields = schema.get('mutually_exclusive_fields', {})
        field1, field2 = mutually_exclusive_fields.get('field1'), mutually_exclusive_fields.get('field2')

        if field1 in json_data and field2 in json_data:
            raise ValueError(f"'{field1}' and '{field2}' are mutually exclusive, but both are present.")

    def _validate_field_values(self, json_data: dict, schema: dict) -> None:
        field_values = schema.get('field_values', {})
        for field, allowed_values in field_values.items():
            if field in json_data and json_data[field] not in allowed_values:
                raise ValueError(f"Invalid value '{json_data[field]}' for field '{field}'. "
                                 f"Allowed values are {allowed_values}.")


# Example
validator = JsonValidator()
result = validator.validate_schema('example.json', 'example_schema.json')
print(result)
