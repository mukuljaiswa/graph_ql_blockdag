from locust import HttpUser, task, between

class GraphQLUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(0.5, 1.5)
    graphql_endpoint = "/subgraphs/name/erc20"
    headers = {"Content-Type": "application/json"}

    def post_graphql_query(self, query: str, request_name: str):
        self.client.post(
            self.graphql_endpoint,
            json={"query": query},
            headers=self.headers,
            name=request_name
        )

    # Task weight: 1
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
        self.post_graphql_query(query, "(1) Token Information")

    # Task weight: 2
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
        self.post_graphql_query(query, "(2) Account Balances")

    # Task weight: 3
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
        self.post_graphql_query(query, "(3) Transfer History")
