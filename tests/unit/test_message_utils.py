from bambooai.messages import reg_ex


def test_extract_code_filters_blacklist():
    response = """```python
import subprocess
print('hi')
```"""
    code = reg_ex._extract_code(response, analyst="Data Analyst DF", provider="local")
    assert '# not allowed import subprocess' in code
    assert "print('hi')" in code


def test_extract_rank():
    text = "some <rank>3</rank> value"
    assert reg_ex._extract_rank(text) == '3'
