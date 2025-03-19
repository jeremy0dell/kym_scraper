import os
import time
import json
import re
from dotenv import load_dotenv
from coinbase_agentkit import (
    CdpWalletProvider,
    CdpWalletProviderConfig
)
from decimal import Decimal
from cdp import ExternalAddress  # Import ExternalAddress for faucet request

# Load environment variables
load_dotenv()

class TokenCreator:
    def __init__(self):
        # Get API credentials from environment variables
        self.cdp_api_key_name = os.getenv("CDP_API_KEY_NAME")
        self.cdp_api_key_private_key = os.getenv("CDP_API_KEY_PRIVATE_KEY")
        
        # Get network ID from environment variables or use default
        self.network_id = os.getenv("NETWORK_ID", "base-sepolia")
        
        # Initialize wallet provider with config
        self.wallet_provider = CdpWalletProvider(CdpWalletProviderConfig(
            api_key_name=self.cdp_api_key_name,
            api_key_private_key=self.cdp_api_key_private_key,
            network_id=self.network_id
        ))
        
    def get_wallet_info(self):
        """Get information about the connected wallet"""
        address = self.wallet_provider.get_address()
        
        # Get balance in ETH (converting from wei)
        balance_wei = self.wallet_provider.get_balance()
        balance_eth = Decimal(balance_wei) / Decimal(10**18)
        
        # Get network information
        network = self.wallet_provider.get_network()
        
        return {
            "address": address,
            "balance_wei": str(balance_wei),
            "balance_eth": str(balance_eth),
            "network_id": network.network_id,
            "chain_id": network.chain_id
        }
    
    def request_faucet_funds(self, asset_id="eth"):
        """Request test tokens from the faucet (only works on base-sepolia)"""
        wallet_info = self.get_wallet_info()
        
        # Verify we're on base-sepolia network
        if wallet_info["network_id"] != "base-sepolia":
            raise ValueError("Faucet is only available on base-sepolia network")
        
        try:
            # Create an ExternalAddress instance for the wallet
            address = ExternalAddress(
                "base-sepolia",
                self.wallet_provider.get_address()
            )
            
            # Request funds from faucet
            print(f"Requesting {asset_id.upper()} from the faucet...")
            faucet_tx = address.faucet(asset_id)
            faucet_tx.wait()
            
            print(f"Received {asset_id.upper()} from the faucet!")
            print(f"Transaction: {faucet_tx.transaction_link}")
            
            # Wait a moment for the balance to update
            print("Waiting for transaction to be confirmed...")
            time.sleep(10)
            
            # Get and display the new balance
            new_wallet_info = self.get_wallet_info()
            print(f"New balance: {new_wallet_info['balance_eth']} ETH")
            
            return True
        except Exception as e:
            print(f"Error requesting faucet funds: {str(e)}")
            raise
    
    def _extract_address_from_transaction(self, tx_hash):
        """Extract the deployed contract address from a transaction receipt"""
        try:
            # Get the transaction receipt
            receipt = self.wallet_provider._web3.eth.get_transaction_receipt(tx_hash)
            
            # The contract address is typically in the contractAddress field
            if receipt and receipt.get('contractAddress'):
                return receipt['contractAddress']
            
            return None
        except Exception as e:
            print(f"Error extracting address from transaction: {str(e)}")
            return None
            
    def _extract_tx_hash_from_response(self, response_obj):
        """Try to extract transaction hash from the contract deployment response"""
        # First, check common attributes
        if hasattr(response_obj, 'transaction_hash'):
            return response_obj.transaction_hash
            
        if hasattr(response_obj, 'tx_hash'):
            return response_obj.tx_hash
            
        # Try to find it in nested objects
        if hasattr(response_obj, 'transaction'):
            tx = response_obj.transaction
            if hasattr(tx, 'transaction_hash'):
                return tx.transaction_hash
                
        # If nothing works, check the string representation
        obj_str = str(response_obj)
        # Look for patterns like 0x followed by 64 hex characters (common tx hash format)
        tx_hash_match = re.search(r'0x[a-fA-F0-9]{64}', obj_str)
        if tx_hash_match:
            return tx_hash_match.group(0)
            
        return None
    
    def deploy_token(self, name, symbol, total_supply):
        """Deploy a new ERC20 token with the given parameters"""
        token_params = {
            "name": name,
            "symbol": symbol,
            "total_supply": total_supply
        }
        
        print(f"Deploying token with parameters: {json.dumps(token_params, indent=2)}")
        print("Deployment in progress, this may take a minute...")
        
        try:
            # Deploy the token using the wallet provider's deploy_token method
            token_contract = self.wallet_provider.deploy_token(
                name=name,
                symbol=symbol,
                total_supply=total_supply
            )
            
            # Get token address - the SmartContract object doesn't have an 'address' attribute
            # Instead, we need to check the contract properties to find the address
            if hasattr(token_contract, 'contract_address'):
                token_address = token_contract.contract_address
            elif hasattr(token_contract, 'address_id'):
                token_address = token_contract.address_id
            elif hasattr(token_contract, 'id'):
                token_address = token_contract.id
            else:
                # Inspect the returned object to find its structure
                print("Returned contract type:", type(token_contract))
                print("Contract attributes:", dir(token_contract))
                
                # Try to access deployment info if available
                if hasattr(token_contract, 'deployment'):
                    deployment = token_contract.deployment
                    if hasattr(deployment, 'address'):
                        token_address = deployment.address
                    else:
                        print("Deployment attributes:", dir(deployment))
                
                # Try to extract the transaction hash
                tx_hash = self._extract_tx_hash_from_response(token_contract)
                if tx_hash:
                    print(f"Found transaction hash: {tx_hash}")
                    # Try to get contract address from transaction receipt
                    token_address = self._extract_address_from_transaction(tx_hash)
                    if token_address:
                        print(f"Extracted contract address from transaction: {token_address}")
                    else:
                        print("Unable to extract address from transaction")
                
                # As a fallback, convert to string to see if the address is included
                contract_str = str(token_contract)
                print("Contract string representation:", contract_str)
                
                # Look for addresses in the string representation 
                address_match = re.search(r'0x[a-fA-F0-9]{40}', contract_str)
                if address_match and not token_address:
                    token_address = address_match.group(0)
                    print(f"Extracted address from string representation: {token_address}")
                
                # If we still can't find the address, ask the user to check the logs
                if not token_address:
                    print("\nCouldn't automatically determine the token address.")
                    print("Check the logs above for deployment information.")
                    token_address = input("Please enter the token address from the logs: ")
            
            # Save token information to a file
            self._save_token_info(name, symbol, total_supply, token_address)
            
            return {
                "token_address": token_address,
                "token_contract": token_contract
            }
        except Exception as e:
            print(f"Error deploying token: {str(e)}")
            
            # Print more detailed error information
            import traceback
            traceback.print_exc()
            
            raise
    
    def _save_token_info(self, name, symbol, total_supply, token_address):
        """Save token information to a file"""
        timestamp = int(time.time())
        filename = f"token_{symbol.lower()}_{timestamp}.json"
        
        token_info = {
            "name": name,
            "symbol": symbol,
            "total_supply": total_supply,
            "token_address": token_address,
            "creation_time": timestamp,
            "network_id": self.network_id,
            "creator_address": self.wallet_provider.get_address()
        }
        
        with open(filename, 'w') as f:
            json.dump(token_info, f, indent=2)
        
        print(f"Token information saved to {filename}")

def main():
    creator = TokenCreator()
    
    # Get wallet information
    wallet_info = creator.get_wallet_info()
    print(f"Wallet Information:")
    print(json.dumps(wallet_info, indent=2))
    
    # Check if we have enough balance
    balance_eth = Decimal(wallet_info["balance_eth"])
    if balance_eth < 0.01:  # Assuming we need at least 0.01 ETH for gas
        print("Wallet balance is too low for deployment.")
        
        # Verify we're on base-sepolia before offering faucet
        if wallet_info["network_id"] == "base-sepolia":
            print("Would you like to request funds from the faucet? (y/n)")
            choice = input().lower()
            
            if choice == 'y':
                creator.request_faucet_funds()
            else:
                print("Please fund your wallet and try again.")
                return
        else:
            print(f"Faucet is only available on base-sepolia network. Current network: {wallet_info['network_id']}")
            print("Please fund your wallet and try again.")
            return
    
    # Deploy a new token
    token_name = input("Enter token name: ")
    token_symbol = input("Enter token symbol: ")
    token_supply = input("Enter token total supply: ")
    
    result = creator.deploy_token(token_name, token_symbol, token_supply)
    
    print(f"\nToken deployed successfully!")
    print(f"Token address: {result['token_address']}")

if __name__ == "__main__":
    main()
