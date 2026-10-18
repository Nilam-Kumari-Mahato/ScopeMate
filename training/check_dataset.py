"""Validate JSONL training examples and their nested assistant response schema."""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {
    "project_type": "string",
    "requirements": "string_array",
    "deliverables": "string_array",
    "budget": "nullable_string",
    "timeline": "nullable_string",
    "revision_limit": "nullable_nonnegative_integer",
    "missing_information": "string_array",
    "assumptions": "string_array",
    "clarifying_questions": "string_array",
}


def reject_constant(value):
    raise ValueError(f"invalid JSON constant {value}")


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def parse_json(text):
    return json.loads(
        text,
        parse_constant=reject_constant,
        object_pairs_hook=reject_duplicate_keys,
    )


def validate_response(response, line_number):
    errors = []
    if not isinstance(response, dict):
        return [f"line {line_number}: assistant JSON must be an object"]

    actual_fields = set(response)
    required_fields = set(REQUIRED_FIELDS)
    missing = sorted(required_fields - actual_fields)
    extra = sorted(actual_fields - required_fields)
    if missing:
        errors.append(f"line {line_number}: missing assistant fields: {', '.join(missing)}")
    if extra:
        errors.append(f"line {line_number}: unexpected assistant fields: {', '.join(extra)}")

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in response:
            continue
        value = response[field]
        valid = False

        if expected_type == "string":
            valid = type(value) is str
        elif expected_type == "string_array":
            valid = (
                type(value) is list
                and all(type(item) is str for item in value)
            )
        elif expected_type == "nullable_string":
            valid = value is None or type(value) is str
        elif expected_type == "nullable_nonnegative_integer":
            valid = value is None or (type(value) is int and value >= 0)

        if not valid:
            errors.append(
                f"line {line_number}: {field} must have type {expected_type}"
            )
    return errors


def validate_file(path):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"ERROR: cannot read {path}: {error}", file=sys.stderr)
        return 2

    line_count = 0
    errors = []
    for line_count, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            errors.append(f"line {line_count}: blank lines are not valid JSONL records")
            continue

        try:
            example = parse_json(line)
        except (json.JSONDecodeError, ValueError) as error:
            errors.append(f"line {line_count}: invalid outer JSON: {error}")
            continue

        if not isinstance(example, dict):
            errors.append(f"line {line_count}: outer JSON value must be an object")
            continue

        messages = example.get("messages")
        if not isinstance(messages, list):
            errors.append(f"line {line_count}: 'messages' must be an array")
            continue

        malformed_message = False
        assistant_messages = []
        for index, message in enumerate(messages, start=1):
            if not isinstance(message, dict):
                errors.append(
                    f"line {line_count}: message {index} must be an object"
                )
                malformed_message = True
                continue
            if type(message.get("role")) is not str:
                errors.append(
                    f"line {line_count}: message {index} role must be a string"
                )
                malformed_message = True
            if type(message.get("content")) is not str:
                errors.append(
                    f"line {line_count}: message {index} content must be a string"
                )
                malformed_message = True
            if message.get("role") == "assistant":
                assistant_messages.append(message)

        if malformed_message:
            continue
        if len(assistant_messages) != 1:
            errors.append(
                f"line {line_count}: expected exactly one assistant message; "
                f"found {len(assistant_messages)}"
            )
            continue

        try:
            response = parse_json(assistant_messages[0]["content"])
        except (json.JSONDecodeError, ValueError) as error:
            errors.append(f"line {line_count}: invalid assistant JSON: {error}")
            continue
        errors.extend(validate_response(response, line_count))

    if line_count == 0:
        errors.append("dataset contains no records")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {line_count} record(s) checked; {len(errors)} error(s)")
        return 1

    print(f"PASS: {line_count} record(s) checked; outer JSONL and assistant schema valid")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate JSONL records and nested ScopeMate assistant responses."
    )
    parser.add_argument(
        "dataset",
        nargs="?",
        type=Path,
        default=ROOT / "dataset" / "train.jsonl",
        help="JSONL file to check (default: dataset/train.jsonl)",
    )
    args = parser.parse_args()
    return validate_file(args.dataset)


if __name__ == "__main__":
    raise SystemExit(main())
