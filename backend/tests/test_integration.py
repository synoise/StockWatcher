import unittest
import requests

class TestIntegration(unittest.TestCase):

    def test_full_workflow(self):
        # Step 1: Fetch data for multiple stocks
        stocks = ['AAPL', 'GOOGL', 'MSFT']
        responses = []
        for stock in stocks:
            response = requests.get(f'https://api.stockwatcher.com/data/{stock}')
            self.assertEqual(response.status_code, 200)
            responses.append(response.json())

        # Step 2: Analyze stocks
        for data in responses:
            self.assertIn('price', data)
            self.assertIn('volume', data)
            # Additional assertions can be added for analysis

    def test_multiple_stocks_analysis(self):
        stocks = ['AMZN', 'NFLX']
        for stock in stocks:
            response = requests.get(f'https://api.stockwatcher.com/data/{stock}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertGreater(data['price'], 0)
            self.assertGreater(data['volume'], 0)

    def test_api_error_handling(self):
        # Testing invalid stock
        response = requests.get('https://api.stockwatcher.com/data/INVALID_STOCK')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Stock not found')

if __name__ == '__main__':
    unittest.main()