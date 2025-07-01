from server import openheidelberg
import sys

sys.path.append("server")

def test_openheidelberg_show_tasks():
    res = openheidelberg.show_tasks()
    print(res)
    assert type(res) == str

def test_openheidelberg_show_members():
    res = openheidelberg.show_members()
    print(res)
    assert type(res) == str

def test_openheidelberg_show_events():
    res = openheidelberg.show_events()
    print(res)
    assert type(res) == str