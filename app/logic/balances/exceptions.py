class BalanceAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class BalanceMerchantDoesNotExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
