import random

statements = [
        "You sold a screenshot of an NFT and gained ",
        "You found a wallet on the road. it had ",
        "You worked as an Uber driver and gained ",
        "Your decisions in the market paid off. You gained "
        ]


class Work():

    def getRandomMoney(self):
        
        random_money = [random.randint(0,999), random.randint(999,2999), random.randint(2999, 9999),random.randint(9999, 99999)]
        random_money_weights = [0.75,0.15, 0.05,0.05]

        return random.choices(random_money, weights=random_money_weights, k=1)

    @classmethod
    def getWorkStatement(cls):
        statement = random.choice(statements)
        money = cls.getRandomMoney(cls)[0]
        print(statement, end="\n")
        print(money)

        return f"{statement}${money}", money



print(Work.getWorkStatement())
