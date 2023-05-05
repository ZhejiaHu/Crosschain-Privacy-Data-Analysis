from remote import get_token_transfer_from_transaction_hash, is_t20_smart_contract, construct_smart_contract_object, invoke_smart_contract_function
"""
    05/05/2023: Get the ERC20 transfer trough transaction.
                --- Test 1: https://etherscan.io/tx/0x94d5d6a5971fe099a2e0282ebb2380288d9ceca6cd4b1f7f7d692e72d6c900e3
                --- Test 2: https://etherscan.io/tx/0xb4c0a28da79e2568f9cd1f650f7bc8b2a9299059fdf974989fc3b357a4e55f85
                --- Test 3: https://etherscan.io/tx/0x44482d1f5f82ce350444088efd9dda1641e3fff05f23b61adaa73da95b1a9e32
                --- Test 4: https://etherscan.io/tx/0xabe61c2b80c927631230d2c29a4cd6a7613410e2ab0aa31ab88012a3961ee841
                --- Test 5: https://etherscan.io/tx/0x971f6c5fea64645b7f12b3e3de6e66dfb385d9c8ef680ef21a309593c503dd86
                
                Remote invoke smart contract functions to get result
                --- Test 1: https://etherscan.io/address/0x3ecab35b64345bfc472477a653e4a3abe70532d9
                
                Get the token transfer event from transaction
                -- Test 1: https://etherscan.io/tx/0xbc2b4b805f20ac0d351c80ddd6508726f612df77411c4d8a03782c2c1ce062be
                -- Test 2: https://etherscan.io/tx/0x42080ea21edba10d3e8fce9bdbf7afeacfcbb40b962ae2c5d20cd5661f47b86e
                -- Test 3: https://etherscan.io/tx/0x65aca16097c18f13a87fbf70169256f12e7368dfb4c0daa941c4bf68504e4a7f
                -- Test 4: https://etherscan.io/tx/0x4651e5ccf4336d2973ba311c6f7c5d80c7d9f371bb96741c787fe71e599b668a
                -- Test 5: https://etherscan.io/tx/0xf48a232cc5676e3084edaa560df203ae9c4dc562cc7a91eaea0bce46fdc7594e
"""


if __name__ == "__main__":
    """
    token_transfers = get_token_transfer_from_transaction_hash_("0x971f6c5fea64645b7f12b3e3de6e66dfb385d9c8ef680ef21a309593c503dd86")
    for tr in token_transfers: print(tr)
    """
    trs = get_token_transfer_from_transaction_hash("0xf48a232cc5676e3084edaa560df203ae9c4dc562cc7a91eaea0bce46fdc7594e", 1)
    for tr in trs: print(tr)






