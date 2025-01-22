from app import app
import pytest

def test_app_layout():
    """Test if app layout is properly initialized"""
    assert app.layout is not None

def test_sidebar_components():
    """Test if sidebar contains all required components"""
    sidebar = app.layout.children[0]
    assert any(component.id == 'date-picker' for component in sidebar.children)
    assert any(component.id == 'group-dropdown' for component in sidebar.children)
    assert any(component.id == 'status-checklist' for component in sidebar.children)

def test_content_components():
    """Test if main content contains all required components"""
    content = app.layout.children[1]
    assert 'Dashboard de Demandas' in str(content.children)
    assert any('status-graph' in str(component) for component in content.children)
    assert any('group-graph' in str(component) for component in content.children)
