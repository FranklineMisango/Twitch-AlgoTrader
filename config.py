from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = "https://algobetavault.vault.azure.net/"
secret_name_one = "Alpacaconfig"
secret_name_two = "IEXCLOUDAPITOKEN"
secret_name_three = "openaikey"

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve the secret
secret_value_one = secret_client.get_secret(secret_name_one).value
secret_value_two = secret_client.get_secret(secret_name_two).value
secret_value_three = secret_client.get_secret(secret_name_three).value


# Use the secret in your config
ALPACA_CONFIG = secret_value_one
Openai_api_key = secret_value_three
IEX_CLOUD_API_TOKEN = secret_value_two
