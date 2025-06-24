from locust import HttpUser, task, between

class GraphQLUser(HttpUser):
    
    host = "http://localhost:8000"
    wait_time = between(0.5, 1.5)
    
    @task(1)
    def get_token_information(self):
        query = """
        {
          tokens {
            id
            name
            symbol
            decimals
            totalSupply
          }
        }
        """
        self.client.post(
            "/subgraphs/name/erc20",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            name="(1) Token Information"  # Unique name for reporting
        )
    
    @task(2)
    def get_account_balances(self):
        query = """
        {
          accountBalances(first: 10, orderBy: amount, orderDirection: desc) {
            id
            amount
            account {
              address
            }
            token {
              symbol
            }
          }
        }
        """
        self.client.post(
            "/subgraphs/name/erc20",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            name="(2) Account Balances"  # Unique name for reporting
        )
    
    @task(3)
    def get_transfer_history(self):
        query = """
        {
          transfers(first: 10, orderBy: blockNumber, orderDirection: desc) {
            id
            from
            to
            value
            blockNumber
            transactionHash
            token {
              symbol
            }
          }
        }
        """
        self.client.post(
            "/subgraphs/name/erc20",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            name="(3) Transfer History"  # Unique name for reporting
        )