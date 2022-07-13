
import pytest
from cli import ConsoleUtility

# Tests
# 1 Data types
@pytest.mark.parametrize("data_type, expected",
                         [("{\"date\": \"timestamp:\"}", True), ("{\"name\": \"str:'John'\"}", True),
                          ("{\"age\": \"int:rand(0,90)\"}", True), ("{\"id\": \"str:rand:\"}", True),
                          ("{\"salary\": \"float:rand\"}", False),
                          ("{\"badges\": \"list:['gold','silver','bronze']\"}", False),
                          ("{\"None\": \"NoneType:\"}", False), ("{\"Vacations\": \"bool:\"}", False)])
def test_data_types(data_type, expected):
    new_cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                             file_count=10, file_name='super_data', file_prefix='count', data_schema=data_type,
                             data_lines=10, clear_path=True, multiprocessing=1)
    new_schema = new_cli.schema_str_to_dict(data_type)
    assert new_cli.validate_schema(new_schema) == expected


# 2 Data schemas
@pytest.mark.parametrize("data_schema, expected", [(
                                                   "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}",
                                                   dict),
                                                   (
                                                   "{\"name\": \"str:'Gonzalo'\",\"last_name\": \"str:'Alcala'\",\"level\": \"['intern', 'junior', 'mid', 'senior']\",\"age\": \"int:rand(1, 90)\"}",
                                                   dict),
                                                   (
                                                   "{\"BusinessId\": \"str:rand\",\"BusinessCode\": \"int:rand\",\"Employees\": \"['Gonzalo', 'Gonzalo2', 'Gonzalo3', 'Gonzalo4']\",\"Networth\": \"int:rand\"}",
                                                   dict)])
def test_data_schemas(data_schema, expected, caplog):
    new_cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                             file_count=10, file_name='super_data', file_prefix='count', data_schema=data_schema,
                             data_lines=10, clear_path=True, multiprocessing=1)
    new_schema = new_cli.schema_str_to_dict(data_schema)
    assert type(new_schema) is expected


# 3 Fixtures using temp files
# 'Done generating files'
@pytest.fixture
def tmppath(tmpdir):
    return Path(tmpdir)


def test_temp_file_fixture(tmpdir, tmppath):
    p = tmpdir.mkdir("sub").join('temp_js.json')
    p.write(
        "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}")
    new_cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                             file_count=10, file_name='super_data', file_prefix='count', data_schema=p,
                             data_lines=10, clear_path=True, multiprocessing=1)
    data_schema = new_cli.load_schema(p)
    assert type(data_schema) is dict


# 4 Check clear path
def test_clear_path(caplog):
    caplog.set_level(logging.INFO)
    new_cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                             file_count=10, file_name='super_data', file_prefix='count',
                             data_schema="{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}",
                             data_lines=10, clear_path=True, multiprocessing=1)
    new_cli.clear_path_and_files(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output')
    assert 'Done removing files that match current filename' in caplog.text


# 5 Check saving files to ssd
@pytest.fixture
def tmppath(tmpdir):
    return Path(tmpdir)


def test_check_files(tmpdir, tmppath):
    p = tmpdir.mkdir("sub").join('temp_js.json')
    p.write(
        "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}")
    cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                         file_count=10, file_name='super_data', file_prefix='count',
                         data_schema="{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"
                         , data_lines=10, clear_path=True, multiprocessing=1)
    data_schema = cli.load_schema(p)
    cli.data_schema = data_schema
    cli.generate_jsonl(schema=data_schema)
    _, _, files = next(os.walk(cli.path))
    assert len(files) == cli.file_count


# 6 Check number of files generated if multiprocessing > 1
@pytest.fixture
def tmppath(tmpdir):
    return Path(tmpdir)


def test_check_files_multiprocessing(tmpdir, tmppath):
    p = tmpdir.mkdir("sub").join('temp_js.json')
    p.write(
        "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}")
    cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                         file_count=100, file_name='super_data_multi', file_prefix='count',
                         data_schema="{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"
                         , data_lines=100, clear_path=True, multiprocessing=2)
    data_schema = cli.load_schema(p)
    cli.data_schema = data_schema
    cli.generate_jsonl(schema=data_schema)
    _, _, files = next(os.walk(cli.path))
    assert len(files) == cli.file_count


# 7 Own test
# Parameterized test that ingest data schemas from schema is dict and writes correct number of files.
@pytest.mark.parametrize("data_schema, expected", [(
                                                   "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}",
                                                   dict),
                                                   (
                                                   "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}",
                                                   dict)])
def test_by_my_own(data_schema, expected):
    new_cli = ConsoleUtility(path='/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/capstone_project/output',
                             file_count=5, file_name='super_data', file_prefix='count', data_schema=data_schema,
                             data_lines=5, clear_path=True, multiprocessing=1)

    schema = new_cli.schema_str_to_dict(new_cli.data_schema)
    new_cli.data_schema = schema
    new_cli.validate_schema(new_cli.data_schema)
    new_cli.generate_jsonl(schema=new_cli.data_schema)
    _, _, files = next(os.walk(new_cli.path))
    assert type(new_cli.data_schema) is dict
    assert len(files) == new_cli.file_count