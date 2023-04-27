from typing import Dict

"""
Make sure that there is only one copy of each transaction / account in the memory during run time. 
"""

in_mem_account_ids: Dict = {}  # Hash to object
in_mem_txns_id: Dict = {}
