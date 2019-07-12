from unittest import mock
from flocx_market.api.service import WSGIService


@mock.patch('flocx_market.api.service.app')
@mock.patch('flocx_market.api.service.Migrate')
@mock.patch('flocx_market.api.service.orm')
@mock.patch('flocx_market.api.service.wsgi')
class TestService:
    def test_create_service(self, mock_wsgi, mock_orm, mock_migrate, mock_app):
        service = WSGIService('testing')
        assert service.name == 'testing'
        assert mock_app.create_app.call_count == 1
        mock_wsgi.Server.assert_called()

    def test_start_service(self, mock_wsgi, mock_orm, mock_migrate, mock_app):
        service = WSGIService('testing')
        service.start()
        service.server.start.assert_called()

    def test_stop_service(self, mock_wsgi, mock_orm, mock_migrate, mock_app):
        service = WSGIService('testing')
        service.stop()
        service.server.stop.assert_called()

    def test_wait_service(self, mock_wsgi, mock_orm, mock_migrate, mock_app):
        service = WSGIService('testing')
        service.wait()
        service.server.wait.assert_called()

    def test_reset_service(self, mock_wsgi, mock_orm, mock_migrate, mock_app):
        service = WSGIService('testing')
        service.reset()
        service.server.reset.assert_called()
