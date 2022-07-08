"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    #>>>is_http_domain('http://wikipedia.org')
    True
    #>>>is_http_domain('https://ru.wikipedia.org/')
    True
    #>>>is_http_domain('griddynamics.com')
    False
"""
import re
import pytest


def is_http_domain(domain: str):
    urls = re.findall(r'^(http|https)://[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+', domain)
    if urls:
        return True
    else:
        return False


"""
write tests for is_http_domain function
"""

# Fixtures


@pytest.mark.parametrize('domains', ['http://wikipedia.org', 'https://ru.wikipedia.org/', 'griddynamics.com'])
def test_domains(domains):
    assert is_http_domain(domains) == True or is_http_domain(domains) == False





