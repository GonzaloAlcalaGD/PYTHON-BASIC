import argparse
import logging
import os
from multiprocessing import Pool
import sys
import json
import configparser
import uuid
import re
import time
import random
import pytest
from pathlib import Path

# Set up default values & global variables
config = configparser.ConfigParser()
config.read('default.ini')
default = config['default']
counter = 1


class ConsoleUtility:
    """
    Universal console utility that will generate our data for us. Format - only JSON.
    """

    def __init__(self, path: str, file_count: int, file_name: str, file_prefix: str, data_schema: str, data_lines: int,
                 clear_path: bool, multiprocessing: int):
        self.path = path
        self.file_count = file_count
        self.file_name = file_name
        self.file_prefix = file_prefix
        self.data_schema = data_schema
        self.data_lines = data_lines
        self.clear_path = clear_path
        self.multiprocessing = multiprocessing

    def isList(test_str):
        """
        Returns a bool value (True or False) if re finds a list
        """
        return (False, True)[bool(re.match(r'\[|\(|\]|\)', test_str))]

    def file_counter(self, file_number: int):
        """
        Logs to terminal the current file being generated
        """
        logging.info('Generating file............{}'.format(file_number))

    def show_config(self):
        """
        Logs to terminal current configuration provided
        """
        logging.info("Configuration:")
        logging.info("Path: {}".format(self.path))
        logging.info(
            "Number of files to generate: {}".format(self.file_count))
        logging.info("File name: {}".format(self.file_name))
        logging.info("File prefix: {}".format(self.file_prefix))
        logging.info("Data schema: {}".format(self.data_schema))
        logging.info("Data lines: {}".format(self.data_lines))
        logging.info("Clear path: {}".format(self.clear_path))
        logging.info("Number of CPUs: {}".format(
            self.multiprocessing))

    def check_args(self):
        """
        Checks if the arguments provided are correct, otherwise it returns a log error and exits.
        """
        if self.path == ".":
            self.path = os.getcwd()

        elif not os.path.exists(self.path):
            logging.error("Error, directory doesn't exist")
            sys.exit(1)

        elif self.file_count < 0:
            logging.error("Error, files_count should be greater than 0")
            sys.exit(1)

        elif self.multiprocessing < 0:
            logging.error('Error, multiprocessing should be greater than 0')
            sys.exit(1)

        elif self.multiprocessing > os.cpu_count():
            self.multiprocessing = os.cpu_count()

        return True

    def str_to_list(self, my_str: str):
        """
        Converts provided str to list
        """
        if my_str.find('[') != 1 and my_str.find(']') != -1:
            list_values = my_str[1:-1]
        return list_values.replace("'", '').replace(' ', '').split(',')

    def schema_str_to_dict(self, data_schema):
        """
        Returns a dict based on provided string dict schema
        """
        try:
            result_schema = json.loads(data_schema)
        except ValueError:
            logging.warning('Provided data schema is not valid json')
            sys.exit(1)
        return result_schema

    def has_numbers(self, my_list: list):
        """
        Returns a bool value (True or False) if number contains digit or not
        """
        flag = False
        for element in my_list:
            if element.isdigit():
                flag = True
            else:
                flag = False
        return flag

    def validate_schema(self, schema: dict):
        """
        Validates if schema provided by user has correct key's and values
        """
        print('-' * 100)
        logging.info("Validating key's and values...")
        print('-' * 100)
        for key, value in schema.items():

            # Get both left and right value
            left_value = value.split(':')[0]
            try:
                right_value = value.split(':')[1]
            except:
                pass

            # Check if left values are valid
            if left_value in ['timestamp', 'int', 'str']:

                # Check if the value is a valid timestamp
                if left_value.find('timestamp') != -1:
                    # Value has more attributes on the right side
                    if len(value.split(':')) > 1:
                        logging.warning(
                            'Timestamp does not support any values and it will be ignored \'{}\':\'{}\''.format(key,
                                                                                                                value))
                    else:
                        # Timestamp is valid
                        logging.info(
                            'Valid timestamp schema \'{}\':\'{}\''.format(key, left_value))

                # Check if the value is a valid string
                if left_value.find('str') != -1:
                    # Check if the rand type has a correct schema
                    if right_value.find('rand') != -1:  # Random string
                        if right_value.find('(') != -1 and right_value.find(')') != -1:
                            logging.error('Invalid rand schema \'{}\':\'{}\''.format(
                                key, left_value + ':' + right_value))
                            sys.exit(1)
                        else:
                            logging.info('Valid string schema for: \'{}\':\'{}:{}\''.format(
                                key, left_value, right_value))

                    # Check if the list type has a correct schema
                    if ConsoleUtility.isList(right_value):
                        logging.info(
                            'List schema found, transforming string schema to actual list...')
                        # Call a function to convert str to list
                        right_value = ConsoleUtility.str_to_list(right_value)
                        # Check if the list is valid
                        if ConsoleUtility.has_numbers(right_value):
                            logging.error(
                                'Invalid list schema str:list should not contain numbers \'{}\':\'{}:{}\''.format(
                                    key, left_value, right_value))
                            sys.exit(1)
                        else:
                            logging.info('Valid list schema \'{}\':\'{}:{}\''.format(
                                key, left_value, right_value))
                    elif isinstance(right_value, str) and right_value != '':
                        logging.info('Valid stand alone value string schema \'{}\':\'{}:{}\''.format(
                            key, left_value, right_value))

                    # Check if right value it's empty
                    if right_value == '':
                        logging.info('Valid empty schema, \'\' will replace it\'{}\':\'{}:{}\''.format(
                            key, left_value, ''))

                # Check if the value is a valid integer
                if left_value.find('int') != -1:

                    # Check if the rand type has a correct schema
                    if right_value.find('rand') != -1:
                        if right_value.find('(') and right_value.find(')') != -1:
                            logging.info('Valid integer rand(from, to) schema for \'{}\':\'{}\''.format(
                                key, left_value + ':' + right_value))
                        else:
                            logging.info('Valid integer schema for: \'{}\':\'{}:{}\''.format(
                                key, left_value, right_value))

                    # Check if the list type has a correct schema
                    if ConsoleUtility.isList(right_value):
                        logging.info(
                            'List schema found, transforming integer schema to actual list...')
                        # Call a function to convert str to list
                        right_value = ConsoleUtility.str_to_list(right_value)

                        # Check if the list is valid
                        if not ConsoleUtility.has_numbers(right_value):
                            logging.error(
                                'Invalid list schema int:list should not contain strings \'{}\':\'{}:{}\''.format(
                                    key, left_value, right_value))
                            sys.exit(1)
                        else:
                            logging.info('Valid list schema \'{}\':\'{}\':\'{}\''.format(
                                key, left_value, right_value))

                    # Check if stand alone integer is valid
                    try:
                        int(right_value)
                        logging.info('Valid stand alone integer schema \'{}\':\'{}:{}\''.format(
                            key, left_value, right_value))
                    except:
                        pass

                    # Check if right value it's empty
                    if right_value == '':
                        logging.info('Valid empty schema, None will replace it \'{}\':\'{}:{}\''.format(
                            key, left_value, None))

                return True
            return False

    def load_schema(self, path_to_schema: str):
        """
        Loads string with dict schema and returns dict
        """
        with open(path_to_schema, 'r') as f:
            data_schema = json.load(f)
        return data_schema

    def check_path_or_schema(self, path_to_schema):
        """
        Checks if the provided schema it's a string schema or a path to existing json file
        """
        try:
            with open(path_to_schema, 'r') as f:
                path_to_schema = json.load(f)
            logging.info('Working with json file schema')
        except:
            logging.info('Working with provided schema')
            return False
        return True

    def multiprocess_prefix_uuid(self):
        """
        Multiprocess json file generator with prefix uuid
        """
        print('-' * 100)
        prefix = str(uuid.uuid4())
        global counter
        with open(self.path + '/' + self.file_name + '_' + prefix + '.jsonl', 'w') as f:
            for j in range(1, self.data_lines + 1):
                data = ConsoleUtility.generate_jsonl_content(self, provided_schema=self.data_schema)
                print(data)
                json.dump(data, f, ensure_ascii=True)
                if j <= self.data_lines - 1:
                    f.write('\n')
            ConsoleUtility.file_counter(self, file_number=counter)
        counter += 1
        return 'Done generating {}'.format(self.file_count)

    def multiprocess_prefix_random(self):
        """
        Multiprocess json file generator with prefix random
        """
        print('-' * 100)
        prefix = str(random.randint(0, 10000000))
        global counter
        with open(self.path + '/' + self.file_name + '_' + prefix + '.jsonl', 'w') as f:
            for j in range(1, self.data_lines + 1):
                data = ConsoleUtility.generate_jsonl_content(self, provided_schema=self.data_schema)
                print(data)
                json.dump(data, f, ensure_ascii=True)
                if j <= self.data_lines - 1:
                    f.write('\n')
            ConsoleUtility.file_counter(self, file_number=counter)
        counter += 1
        return 'Done generating {}'.format(self.file_count)

    def multiprocess_prefix_count(self):
        """
        Multiprocess json file generator with prefix count
        """
        print('-' * 100)
        global counter
        with open(self.path + '/' + self.file_name + '_' + str(counter) + '.jsonl', 'w') as f:
            for j in range(1, self.data_lines + 1):
                data = ConsoleUtility.generate_jsonl_content(self, provided_schema=self.data_schema)
                print(data)
                json.dump(data, f, ensure_ascii=True)
                if j <= self.data_lines - 1:
                    f.write('\n')
            ConsoleUtility.file_counter(self, file_number=counter)
        counter += 1
        return 'Done generating {}'.format(self.file_count)

    def clear_path_and_files(self, path: str):
        """
        Clears directory path files if they match provided filename arguments provided by user input
        """
        for file in os.listdir(path):
            if file.find(self.file_name) != -1:
                os.remove(path + '/' + file)
        return logging.info('Done removing files that match current filename')

    def generate_jsonl_content(self, provided_schema: dict):
        """
        Generates json content for each data line.
        """
        random.seed(time.time())
        result = {}
        for key, value in provided_schema.items():
            # Get both left and right value
            try:
                left_value = value.split(':')[0]
                right_value = value.split(':')[1]
            except:
                pass
            # Transform the declarative values into actual values
            # Check timestamp types
            if left_value == 'timestamp':
                result[key] = str(time.time())

            # Check str types
            elif left_value == 'str':
                # str:rand
                if right_value == 'rand':
                    result[key] = str(uuid.uuid4())
                # str:['a','b','c']
                elif ConsoleUtility.isList(right_value) == True:
                    list_values = ConsoleUtility.str_to_list(right_value)
                    result[key] = random.choice(list_values)
                # str:'cat' stand alone value
                elif isinstance(right_value, str) and right_value != '':
                    result[key] = str(right_value.replace('\'', ''))
                # str:'' empty value
                elif right_value == '':
                    result[key] = ''

            # Check if only value it's a valid list
            elif ConsoleUtility.isList(left_value) == True:
                stand_alone_list_values = ConsoleUtility.str_to_list(self, my_str=left_value)
                result[key] = random.choice(stand_alone_list_values)

            # Check int types
            elif left_value == 'int':
                # int:rand
                if right_value.find('rand') != -1:
                    if right_value.find('rand(') != -1 and right_value.find(')') != -1:
                        both_values = right_value.split('(')
                        both_values = both_values[1].split(',')
                        l = int(both_values[0].replace('\'', ''))
                        r = int(both_values[1].replace(' ', '').replace(')', ''))
                        result[key] = random.randint(l, r)
                    else:
                        result[key] = random.randint(0, 10000)
                # int:[1,2,3]
                elif ConsoleUtility.isList(right_value):
                    result[key] = random.choice(right_value)
                # int:3 stand alone value
                elif isinstance(right_value, int) and right_value != '':
                    result[key] = right_value
                # int: empty value
                elif right_value == '':
                    result[key] = 'None'

        return result

    def generate_jsonl(self):
        """
        Generates json files for each prefix
        """
        # We generate the files
        if self.file_prefix == 'count':
            print('-' * 100)
            for i in range(1, self.file_count + 1):
                with open(self.path + '/' + str(self.file_name + '_' + str(i)) + '.jsonl', 'w') as f:
                    for j in range(1, self.data_lines + 1):
                        data = ConsoleUtility.generate_jsonl_content(self, provided_schema=self.data_schema)
                        print(data)
                        json.dump(data, f, ensure_ascii=True)
                        if j <= self.data_lines - 1:
                            f.write('\n')
                    ConsoleUtility.file_counter(self, file_number=i)
            return 'Done generating files'
        elif self.file_prefix == 'random':
            print('-' * 100)
            for i in range(1, self.file_count + 1):
                prefix = str(random.randint(0, 10000))
                with open(self.path + '/' + self.file_name + '_' + prefix + '.jsonl', 'w') as f:
                    for j in range(1, self.data_lines + 1):
                        data = ConsoleUtility.generate_jsonl_content(self, provided_schema=self.data_schema)
                        print(data)
                        json.dump(data, f, ensure_ascii=True)
                        if j <= self.data_lines - 1:
                            f.write('\n')
                    ConsoleUtility.file_counter(self, file_number=i)
            return 'Done generating files'
        else:
            print('-' * 100)
            for i in range(1, self.file_count + 1):
                prefix = str(uuid.uuid4())
                with open(self.path + '/' + self.file_name + '_' + prefix + '.jsonl', 'w') as f:
                    for j in range(1, self.data_lines + 1):
                        data = ConsoleUtility.generate_jsonl_content(self, provided_schema=self.data_schema)
                        print(data)
                        json.dump(data, f, ensure_ascii=True)
                        if j <= self.data_lines - 1:
                            f.write('\n')
                    ConsoleUtility.file_counter(self, file_number=i)
        return 'Done generating files'

    def multiprocess_generate_jsonl(self):
        """
        Generates json files using multiprocessing with provided prefix
        """
        if self.file_prefix == 'count':
            ConsoleUtility.multiprocess_prefix_count(self)
        elif self.file_prefix == 'random':
            pass
            ConsoleUtility.multiprocess_prefix_random(self)
        else:
            ConsoleUtility.multiprocess_prefix_uuid(self)


if __name__ == '__main__':
    # Set up argparse to handle command line arguments
    parser = argparse.ArgumentParser(prog="Console Utility",
                                     description="Console utility for generating test data based on the provided data schema.")
    parser.add_argument("--path_to_save_files", help="Path to save the generated files.")
    parser.add_argument("--files_count", help="How many json files to generate", type=int)
    parser.add_argument("--file_name", help="File name prefix", type=str)
    parser.add_argument("--file_prefix", help="File prefix", type=str, choices=['count', 'random', 'uuid'])
    parser.add_argument("--data_schema",
                        help="It’s a string with json schema. It could be loaded in two ways: \n1) With path to json file with schema \n2) with schema entered to command line.",
                        type=str)
    parser.add_argument("--data_lines", help="Count of lines for each file. ", type=int)
    parser.add_argument("--clear_path", help="Clear the path before generating files", action="store_true")
    parser.add_argument("--multiprocessing", help="The number of processes used to create files.", type=int)
    logging.basicConfig(level=logging.INFO)
    parser.set_defaults(**default)
    args = parser.parse_args()
    cli = ConsoleUtility(args.path_to_save_files, args.files_count, args.file_name, args.file_prefix, args.data_schema,
                         args.data_lines, args.clear_path, args.multiprocessing)
    if cli.check_args():
        # Check if user wants to use single process or multiprocess
        if args.clear_path:
            cli.clear_path_and_files(path=args.path_to_save_files)
        if cli.multiprocessing != 1:
            logging.info("Multiprocessing enabled with {} processes".format(cli.multiprocessing))
            if cli.check_path_or_schema(cli.data_schema):
                if os.path.exists(cli.data_schema):
                    logging.info('Loading data schema from file...')
                    async_results = []
                    schema = cli.load_schema(path_to_schema=args.data_schema)
                    cli.data_schema = schema
                    cli.show_config()
                    cli.validate_schema(schema)
                    pool = Pool(processes=cli.multiprocessing)
                    start = time.time()
                    print('Number of files to generate: {}'.format(cli.file_count))
                    for n_files in range(cli.file_count):
                        async_results.append(pool.apply_async(cli.multiprocess_generate_jsonl()))
                    pool.close()
                    pool.join()
                    end = time.time()
                    logging.info('Time to generate {} files: {}'.format(cli.file_count, end - start))
                else:
                    logging.error('Data schema file does not exist')
                    sys.exit(1)
            else:
                # We create a list to store async processes
                async_results = []
                # Load data schema
                schema = cli.schema_str_to_dict(cli.data_schema)
                cli.data_schema = schema
                # Show config
                cli.show_config()
                # Validate schema
                cli.validate_schema(schema)
                # Initialize multiprocessing
                pool = Pool(processes=cli.multiprocessing)
                start = time.time()
                print('Number of files to generate: {}'.format(cli.file_count))
                for n_files in range(cli.file_count):
                    async_results.append(pool.apply_async(cli.multiprocess_generate_jsonl()))
                pool.close()
                pool.join()
                end = time.time()
                logging.info('Time to generate {} files: {}'.format(cli.file_count, end - start))
        else:
            print('-' * 100)
            logging.info("Single process")
            print('-' * 100)
            if cli.check_path_or_schema(path_to_schema=args.data_schema):
                if os.path.exists(args.data_schema):
                    logging.info('Loading data schema from file...')
                    schema = cli.load_schema(path_to_schema=args.data_schema)
                    cli.data_schema = schema
                    cli.show_config()
                    cli.validate_schema(schema=schema)
                    start = time.time()
                    cli.generate_jsonl()
                    end = time.time()
                    logging.info('Time to generate {} files: {}'.format(cli.file_count, end - start))
                else:
                    logging.error('Data schema file does not exist')
                    sys.exit(1)
            else:
                schema = cli.schema_str_to_dict(cli.data_schema)
                cli.data_schema = schema
                cli.show_config()
                cli.validate_schema(cli.data_schema)
                start = time.time()
                cli.generate_jsonl()
                end = time.time()
                logging.info('Time to generate {} files: {}'.format(cli.file_count, end - start))
    else:
        logging.error("Error, check arguments")
        sys.exit(1)
    sys.exit(0)

