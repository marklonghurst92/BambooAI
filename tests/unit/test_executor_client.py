import requests
from bambooai.executor_client import ExecutorAPIClient


class MockResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError('error')

    def json(self):
        return self._data


def test_execute_code_success(monkeypatch):
    def mock_post(url, json):
        return MockResponse({'results': 'ok', 'error': None, 'plot_images': [], 'generated_datasets': []})

    monkeypatch.setattr(requests, 'post', mock_post)
    client = ExecutorAPIClient(base_url='http://test')
    resp = client.execute_code('print(1)')
    assert resp['results'] == 'ok'
    assert resp['error'] is None


def test_execute_code_request_exception(monkeypatch):
    def mock_post(url, json):
        raise requests.RequestException('boom')

    monkeypatch.setattr(requests, 'post', mock_post)
    client = ExecutorAPIClient(base_url='http://test')
    resp = client.execute_code('print(1)')
    assert resp['results'] is None
    assert 'boom' in resp['error']


def test_dataframe_to_string(monkeypatch):
    def mock_post(url, json):
        return MockResponse({'data': 'df head'})

    monkeypatch.setattr(requests, 'post', mock_post)
    client = ExecutorAPIClient(base_url='http://test')
    result = client.dataframe_to_string('df1', num_rows=5)
    assert result == 'df head'
