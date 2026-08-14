from datetime import datetime, timezone

# Add variables to user's `profile` (created when `create_profile` route is called)
def add_to_profile(profile):
    profile['timestamp'] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return profile

# Set treatment variables
# Note: not currently called anywhere in app.py -- kept from prior round's config as a
# placeholder. Wire it into add_to_profile (e.g. `profile = set_treatments(profile, **profile)`)
# if treatment-arm assignment needs to happen at profile-creation time.
def set_treatments(profile, **kwargs):
    return profile

def choice_message(label, deposit, repay):

    deposit = 'Ksh {:,.0f}'.format(deposit)
    repay = 'Ksh {:,.0f}'.format(repay)
    repay_rest = 24*7

    # Create the HTML table
    html_table = f"""
        <table style="background-color: lightgray; border-collapse: collapse; border: 1px solid black;">
            <tbody>
                <tr>
                    <th style="padding: 20px"><b>{label}</b></th>
                </tr>
                <tr>
                    <td style="padding: 20px; border-top: 1px solid black"><strong>Deposit:</strong> {deposit}</td>
                </tr>
                <tr>
                    <td style="padding: 20px; border-top: 1px solid black"><strong>Weekly Repayment #1 to #4:</strong> {repay}</td>
                </tr>
                <tr>
                    <td style="padding: 20px; border-top: 1px solid black"><strong>Weekly Repayment #5 to #56:</strong> {repay_rest}</td>
                </tr>
            </tbody>
        </table>
    """
    return html_table

def convert_design(design, profile, request_data, choice_message=choice_message, **kwargs):
    # Function to convert design for output.
    # Note: To work correctly with the native /survey route,
    #    add the html you want to save for each option to output
    #    as f'message_{answer_val}_{Q}' as in the example below.

    # Number of questions
    Q = request_data.get('question_number') or len(profile.get('design_history'))

    output = {f'{key}_{Q}': value for key, value in design.items()}

    output[f'message_0_{Q}'] = choice_message("Solar A", design['deposit_a'], design['repay_a'])
    output[f'message_1_{Q}'] = choice_message("Solar B", design['deposit_b'], design['repay_b'])

    return output
