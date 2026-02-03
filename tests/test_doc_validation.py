import pytest
from mcp_moviepy.utils.doc_validation import ensure_doc_reference

def test_doc_reference_validation_success():
    @ensure_doc_reference
    def valid_function():
        """
        This function does something.
        Ref: html/some/path.html
        """
        pass
    
    # Should not raise any exception
    valid_function()

def test_doc_reference_validation_failure():
    with pytest.raises(ValueError, match="Docstring must contain a reference to 'html/'"):
        @ensure_doc_reference
        def invalid_function():
            """
            This function is missing a reference.
            """
            pass

def test_doc_reference_validation_no_docstring():
    with pytest.raises(ValueError, match="Function must have a docstring"):
        @ensure_doc_reference
        def no_docstring_function():
            pass
