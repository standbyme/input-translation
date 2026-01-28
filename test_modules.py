"""Basic tests for the input translation daemon modules.

This file provides simple smoke tests to verify the basic functionality
of the refactored modules without requiring external services.
"""

import sys
from unittest.mock import MagicMock, patch


def test_config_imports():
    """Test that config module can be imported and has expected values."""
    import config
    
    assert hasattr(config, 'MODEL')
    assert hasattr(config, 'TRANSLATE_HOTKEY')
    assert hasattr(config, 'RESTART_HOTKEY')
    assert config.MODEL == "gpt-4o-mini", f"Expected gpt-4o-mini but got {config.MODEL}"
    assert config.TRANSLATE_HOTKEY == "ctrl+alt+t"
    assert config.RESTART_HOTKEY == "ctrl+alt+r"
    print("✓ Config module imports and values correct")


def test_clipboard_imports():
    """Test that clipboard module can be imported."""
    import clipboard
    
    assert hasattr(clipboard, 'safe_copy_selected_text')
    assert hasattr(clipboard, 'paste_text')
    print("✓ Clipboard module imports correct")


def test_translator_imports():
    """Test that translator module can be imported."""
    with patch('translator.load_dotenv'):
        with patch.dict('os.environ', {'API_KEY': 'test-key'}):
            import translator
            
            assert hasattr(translator, 'get_client')
            assert hasattr(translator, 'TranslationService')
            print("✓ Translator module imports correct")


def test_handlers_imports():
    """Test that handlers module can be imported."""
    with patch('translator.load_dotenv'):
        with patch.dict('os.environ', {'API_KEY': 'test-key'}):
            import handlers
            
            assert hasattr(handlers, 'HotkeyHandler')
            print("✓ Handlers module imports correct")


def test_main_imports():
    """Test that main module can be imported."""
    with patch('translator.load_dotenv'):
        with patch.dict('os.environ', {'API_KEY': 'test-key'}):
            # Import main without running it
            with patch('keyboard.add_hotkey'):
                with patch('keyboard.wait'):
                    # Just verify it can be imported
                    import main
                    print("✓ Main module imports correct")


def test_translation_service_structure():
    """Test TranslationService class structure."""
    with patch('translator.load_dotenv'):
        with patch.dict('os.environ', {'API_KEY': 'test-key'}):
            from translator import TranslationService
            
            # Mock the OpenAI client
            with patch('translator.get_client') as mock_get_client:
                mock_client = MagicMock()
                mock_get_client.return_value = mock_client
                
                service = TranslationService()
                assert service.client is not None
                assert hasattr(service, 'translate')
                print("✓ TranslationService structure correct")


def test_hotkey_handler_structure():
    """Test HotkeyHandler class structure."""
    with patch('translator.load_dotenv'):
        with patch.dict('os.environ', {'API_KEY': 'test-key'}):
            from handlers import HotkeyHandler
            from translator import TranslationService
            
            # Mock the OpenAI client
            with patch('translator.get_client') as mock_get_client:
                mock_client = MagicMock()
                mock_get_client.return_value = mock_client
                
                service = TranslationService()
                handler = HotkeyHandler(service)
                
                assert hasattr(handler, 'translate_and_replace')
                assert hasattr(handler, 'restart_program')
                assert handler.translation_service == service
                print("✓ HotkeyHandler structure correct")


if __name__ == "__main__":
    print("Running basic smoke tests...\n")
    
    try:
        test_config_imports()
        test_clipboard_imports()
        test_translator_imports()
        test_handlers_imports()
        test_main_imports()
        test_translation_service_structure()
        test_hotkey_handler_structure()
        
        print("\n✓ All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
