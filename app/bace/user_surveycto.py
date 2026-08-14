# Survey CTO Integration Functions

def convert_design_surveycto(design, profile, request_data, **kwargs):
    # Function to convert design for SurveyCTO route.
    # Output produces a single string that captures the design.
    # Rows are separated by "|", values within rows by ":"
    # E.g. output = "deposit:100:150|repay:20:25" maps to a table in SurveyCTO of:
    #
    #       deposit | 100  | 150
    #       repay   | 20   | 25
    #
    # See BACE SurveyCTO plug-in and BACE Manual for more details.

    output = ""
    vars = ['deposit', 'repay']

    for var in vars:
        # Format as currency with no decimal places
        row = f"{var}:{design.get(f'{var}_a'):,.0f}:{design.get(f'{var}_b'):,.0f}"
        output += row + "|"

    print(output)

    return {'output': output}

def convert_dict_to_string(obj, parent_key='', split_to_rows='|', split_to_vars=':'):
    # Function to convert a nested dictionary into a string formatted to integrate with SurveyCTO
    output = []

    for key, val in obj.items():
        # Build the full key path using underscore for nested keys
        new_key = f"{parent_key}_{key}" if parent_key else key

        if isinstance(val, dict):
            # Recursively handle nested dictionaries
            nested_output = convert_dict_to_string(val, new_key, split_to_rows, split_to_vars)
            output.append(nested_output)
        else:
            # For non-dictionary values, format them as "key:value"
            output.append(f"{new_key}{split_to_vars}{val}")

    return split_to_rows.join(output)
