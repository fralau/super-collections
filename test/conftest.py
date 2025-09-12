import pytest
from rich import print

@pytest.fixture(autouse=True)
def announce_test(request):
    print(f"[green]\n\n🔧 Executing: {request.node.name}()[/green]")