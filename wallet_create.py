from eth_account import Account
import secrets


def wallet_generate():
    ret_dict = {}
    private_blank = secrets.token_hex(32)
    private_key = "0x" + private_blank
    wallet = Account.from_key(private_key)
    wallet_address = wallet.address
    ret_dict[private_key] = wallet_address

    return ret_dict


wallet_dict = wallet_generate()
for private_key, wallet_address in wallet_dict.items():
    print(f"Key: {private_key}\nAddress: {wallet_address}")
