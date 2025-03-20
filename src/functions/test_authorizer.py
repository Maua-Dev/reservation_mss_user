def lambda_handler(event, context):
    try:
        methodArn = event["methodArn"]
        return generate_policy("user", "Allow", methodArn)
    except Exception as e:
        print(f"Error: {e}")
        return generate_policy("user", "Deny", event["methodArn"])

def generate_policy(principal_id, effect, method_arn, context=None):
    '''
    This function generates the policy document based on the principal ID, effect, method ARN, and context.

    Args:
        principal_id (str): The principal ID.
        effect (str): The effect (Allow or Deny).
        method_arn (str): The method ARN.
        context (dict): The context object.

    Returns:
        dict: The policy document.
    '''

    # Generating the policy document
    auth_response = {"principalId": principal_id}

    if effect:
        policy_document = {
            "Version": "2012-10-17",  # Version of the policy
            "Statement": [
                {
                    "Action": "execute-api:Invoke",  # Action to allow
                    "Effect": effect,  # Effect (Allow or Deny)
                    "Resource": method_arn,  # Resource path
                }
            ],
        }
        auth_response["policyDocument"] = policy_document

    if context:
        auth_response["context"] = context  # Adding the context to the response

    return auth_response