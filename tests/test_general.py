import pytest
import os
from unittest.mock import Mock, patch
from search_trends.src.timeline import Timeline
import datetime

@pytest.fixture(autouse=True)
def set_env_vars():
    """Fixture to set environment variables before tests and clean up after"""
    os.environ['API_KEY'] = 'dummy_api_key'
    yield
    # Clean up after tests
    if 'API_KEY' in os.environ:
        del os.environ['API_KEY']

@pytest.fixture
def timeline():
    with patch('search_trends.src.timeline.build') as mock_build:
        # Create a mock service
        mock_service = Mock()
        mock_build.return_value = mock_service
        timeline = Timeline()
        timeline.service = mock_service
        return timeline

def test_date_to_string_full_date(timeline):
    """Test date conversion with full date format"""
    result = timeline.date_to_string("Jul 04 2004")
    assert result == "2004-07-04"

def test_date_to_string_month_year(timeline):
    """Test date conversion with month and year format"""
    result = timeline.date_to_string("Jul 2004")
    assert result == "2004-07-01"

def test_date_to_string_year(timeline):
    """Test date conversion with year only format"""
    result = timeline.date_to_string("2004")
    assert result == "2004-01-01"

def test_date_to_string_invalid_format(timeline):
    """Test date conversion with invalid format"""
    with pytest.raises(ValueError):
        timeline.date_to_string("invalid date")

def test_get_search_volumes_country(timeline):
    """Test getting search volumes with country restriction"""
    # Mock the API response
    mock_response = {
        'lines': [
            {
                'term': 'python',
                'points': [
                    {'date': 'Jul 04 2004', 'value': 75}
                ]
            }
        ]
    }
    timeline.service.getTimelinesForHealth.return_value.execute.return_value = mock_response

    result = timeline.get_search_volumes(
        terms=['python'],
        start_date='2004-07-04',
        end_date='2004-07-04',
        frequency='DAY',
        geo_restriction='country',
        geo_restriction_option='US'
    )

    assert result == [['python', '2004-07-04', 75]]
    timeline.service.getTimelinesForHealth.assert_called_once()

def test_get_search_volumes_region(timeline):
    """Test getting search volumes with region restriction"""
    mock_response = {
        'lines': [
            {
                'term': 'python',
                'points': [
                    {'date': 'Jul 04 2004', 'value': 75}
                ]
            }
        ]
    }
    timeline.service.getTimelinesForHealth.return_value.execute.return_value = mock_response

    result = timeline.get_search_volumes(
        terms=['python'],
        start_date='2004-07-04',
        end_date='2004-07-04',
        frequency='DAY',
        geo_restriction='region',
        geo_restriction_option='US-NY'
    )

    assert result == [['python', '2004-07-04', 75]]

def test_get_related_topics(timeline):
    """Test getting related topics"""
    mock_response = {'some': 'data'}
    timeline.service.getTopTopics.return_value.execute.return_value = mock_response

    result = timeline.get_related(
        term='python',
        geography='US',
        start_date='2004-07-04',
        end_date='2004-07-04',
        type='topic'
    )

    assert result == mock_response
    timeline.service.getTopTopics.assert_called_once_with(
        term='python',
        restriction_geo='US',
        restrictions_startDate='2004-07-04',
        restrictions_endDate='2004-07-04'
    )

def test_get_related_queries(timeline):
    """Test getting related queries"""
    mock_response = {'some': 'data'}
    timeline.service.getTopQueries.return_value.execute.return_value = mock_response

    result = timeline.get_related(
        term='python',
        geography='US',
        start_date='2004-07-04',
        end_date='2004-07-04',
        type='query'
    )

    assert result == mock_response
    timeline.service.getTopQueries.assert_called_once_with(
        term='python',
        restriction_geo='US',
        restrictions_startDate='2004-07-04',
        restrictions_endDate='2004-07-04'
    )