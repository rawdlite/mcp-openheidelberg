from server.workpackages import WorkpackageParser

def test_workpackage():
    """
    test_workpackage function tests the initialization of the WorkpackageParser
    class and verifies its basic properties. Specifically, it ensures that
    an object of WorkpackageParser is successfully created and its 'apikey'
    attribute is of type string.

    :return: None
    """
    wp = WorkpackageParser()
    assert wp
    assert type(wp.apikey) == str

def test_get_workpackages():
    wp = WorkpackageParser()
    workpackages = wp.get_workpackages()
    assert type(workpackages) == list

