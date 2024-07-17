# Number of Questions -> /survey route
nquestions = 15

# Set treatment variables
def set_treatments(profile, **kwargs):
    return profile

def choice_message(label, price, repay):

    price = 'Ksh {:,.0f}'.format(price)
    repay = 'Ksh {:,.0f}'.format(repay)

    

    # Create the HTML table
    html_table = f"""
        <table style="background-color: lightgray; border-collapse: collapse; border: 1px solid black;">
            <tbody>
                <tr>
                    <th style="padding: 20px"><b>{label}</b></th>
                </tr>
                <tr>
                    <td style="padding: 20px; border-top: 1px solid black"><strong>Deposit:</strong> {price}</td>
                </tr>
                <tr>
                    <td style="padding: 20px; border-top: 1px solid black"><strong>Weekly Repayment #1 to #4:</strong> {repay}</td>
                </tr>
            </tbody>
        </table>
    """
    return html_table

def convert_design(design, profile, request_data, choice_message=choice_message,  **kwargs):

    # Number of questions
    Q = request_data.get('question_number') or len(profile.get('design_history'))

    output = {f'{key}_{Q}': value for key, value in design.items()}


    output[f'message_0_{Q}'] = choice_message("Solar A", design['price_a'], design['repay_a'])
    output[f'message_1_{Q}'] = choice_message("Solar B", design['price_b'], design['repay_b'])

    return output

def convert_design_surveycto(design, profile, request_data, **kwargs):

    output = ""
    vars = ['price', 'repay']

    for var in vars:
        if var == 'price' or var == 'repay':
            # Format as currency with no decimal places
            row = f"{var}:{design.get(f'{var}_a'):,.0f}:{design.get(f'{var}_b'):,.0f}"
        else:
            row = f"{var}:{design.get(f'{var}_a')}:{design.get(f'{var}_b')}"

        output += row + "|"

    print(output)

    return {'output': output}

def convert_dict_to_string(obj, parent_key='', split_to_rows='|', split_to_vars=':'):
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

